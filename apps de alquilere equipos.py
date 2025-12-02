import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# --- Conexión con la base de datos (ajusta user/password si hace falta) ---
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Thor3124cash$",
    database="alquiler_equipos"
)

# Usaremos cursores locales en cada función para evitar confusión
# --- Crear tablas si no existen ---
with conexion.cursor() as cur:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS equipos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        tipo VARCHAR(50),
        estado VARCHAR(20) DEFAULT 'Disponible'
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alquileres (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cliente VARCHAR(100),
        equipo_id INT,
        hora_entrada DATETIME,
        hora_salida DATETIME,
        costo DECIMAL(10,2),
        FOREIGN KEY (equipo_id) REFERENCES equipos(id)
    )
    """)
conexion.commit()

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Sistema de Alquiler de Equipos")
ventana.geometry("850x600")
ventana.configure(bg="#ECEFF1")

# --- Widgets ---
tk.Label(ventana, text="Cliente:", bg="#ECEFF1").place(x=30, y=30)
entrada_cliente = tk.Entry(ventana, width=30)
entrada_cliente.place(x=100, y=30)

tk.Label(ventana, text="Equipo:", bg="#ECEFF1").place(x=30, y=70)
combo_equipos = ttk.Combobox(ventana, width=50, state="readonly")
combo_equipos.place(x=100, y=70)

tk.Label(ventana, text="Horas de uso:", bg="#ECEFF1").place(x=30, y=110)
entrada_horas = tk.Entry(ventana, width=10)
entrada_horas.place(x=130, y=110)

tk.Label(ventana, text="Costo por hora ($):", bg="#ECEFF1").place(x=30, y=150)
entrada_costo_hora = tk.Entry(ventana, width=10)
entrada_costo_hora.insert(0, "5")  # Valor por defecto
entrada_costo_hora.place(x=160, y=150)

# --- Tabla de registros de alquileres ---
tree = ttk.Treeview(ventana, columns=("ID", "Cliente", "Equipo", "Entrada", "Salida", "Costo"), show="headings")
for col in ("ID", "Cliente", "Equipo", "Entrada", "Salida", "Costo"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.place(x=30, y=250, width=780, height=300)

# --- Funciones ---
def actualizar_equipos_disponibles():
    """Carga la lista de equipos disponibles en el combobox."""
    with conexion.cursor() as cur:
        cur.execute("SELECT nombre FROM equipos WHERE estado='Disponible' ORDER BY nombre")
        rows = cur.fetchall()
    equipos = [r[0] for r in rows]
    combo_equipos["values"] = equipos
    if equipos:
        combo_equipos.current(0)
    else:
        combo_equipos.set('')

def actualizar_lista():
    """Carga los registros de alquileres en la tabla."""
    with conexion.cursor() as cur:
        cur.execute("""
            SELECT a.id, a.cliente, e.nombre, a.hora_entrada, a.hora_salida, a.costo
            FROM alquileres a
            JOIN equipos e ON a.equipo_id = e.id
            ORDER BY a.hora_entrada DESC
        """)
        registros = cur.fetchall()
    tree.delete(*tree.get_children())
    for fila in registros:
        # formatear datetimes para mostrar bonito
        entrada = fila[3].strftime("%Y-%m-%d %H:%M:%S") if fila[3] else ""
        salida = fila[4].strftime("%Y-%m-%d %H:%M:%S") if fila[4] else ""
        tree.insert("", "end", values=(fila[0], fila[1], fila[2], entrada, salida, float(fila[5]) if fila[5] is not None else 0.0))
    actualizar_equipos_disponibles()

def alquilar_equipo():
    """Registra un nuevo alquiler si el equipo está disponible (verifica en BD)."""
    cliente = entrada_cliente.get().strip()
    equipo_nombre = combo_equipos.get().strip()
    horas_txt = entrada_horas.get().strip()
    costo_hora_txt = entrada_costo_hora.get().strip()

    if not cliente or not equipo_nombre or not horas_txt or not costo_hora_txt:
        messagebox.showwarning("Error", "Complete todos los campos.")
        return

    try:
        horas = float(horas_txt)
        costo_hora = float(costo_hora_txt)
        if horas <= 0 or costo_hora < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Horas y costo por hora deben ser números válidos.")
        return

    with conexion.cursor() as cur:
        # obtener id y estado actual del equipo
        cur.execute("SELECT id, estado FROM equipos WHERE nombre=%s", (equipo_nombre,))
        row = cur.fetchone()
        if not row:
            messagebox.showerror("Error", "Equipo no encontrado.")
            return
        equipo_id, estado_actual = row

        if estado_actual == "Ocupado":
            messagebox.showinfo("Aviso", f"El equipo '{equipo_nombre}' ya está ocupado.")
            actualizar_equipos_disponibles()
            return

        # Re-verificar inmediatamente por si otro proceso lo ocupó
        cur.execute("SELECT estado FROM equipos WHERE id=%s FOR UPDATE", (equipo_id,))
        estado_check = cur.fetchone()[0]
        if estado_check == "Ocupado":
            messagebox.showinfo("Aviso", f"El equipo '{equipo_nombre}' acaba de ser alquilado por otro cliente.")
            return

        hora_entrada = datetime.now()
        hora_salida = hora_entrada + timedelta(hours=horas)
        costo_total = round(horas * costo_hora, 2)

        # Insertar alquiler y actualizar estado
        cur.execute("""
            INSERT INTO alquileres (cliente, equipo_id, hora_entrada, hora_salida, costo)
            VALUES (%s, %s, %s, %s, %s)
        """, (cliente, equipo_id, hora_entrada, hora_salida, costo_total))
        cur.execute("UPDATE equipos SET estado='Ocupado' WHERE id=%s", (equipo_id,))
    conexion.commit()

    messagebox.showinfo("Éxito", f"Equipo '{equipo_nombre}' alquilado a {cliente}.\nCosto total: ${costo_total:.2f}")
    generar_factura_para(cliente, equipo_nombre, horas, costo_total)
    # limpiar campos mínimos
    entrada_cliente.delete(0, tk.END)
    entrada_horas.delete(0, tk.END)
    actualizar_lista()

def eliminar_registro():
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Aviso", "Seleccione un registro para eliminar.")
        return

    item = tree.item(seleccionado[0])
    id_alquiler = item["values"][0]
    equipo_nombre = item["values"][2]

    with conexion.cursor() as cur:
        cur.execute("SELECT id FROM equipos WHERE nombre=%s", (equipo_nombre,))
        row = cur.fetchone()
        equipo_id = row[0] if row else None

        cur.execute("DELETE FROM alquileres WHERE id=%s", (id_alquiler,))
        if equipo_id:
            cur.execute("UPDATE equipos SET estado='Disponible' WHERE id=%s", (equipo_id,))
    conexion.commit()
    actualizar_lista()
    messagebox.showinfo("Eliminado", "Registro eliminado y equipo disponible nuevamente.")

def generar_factura_para(cliente, equipo, horas, costo):
    """Genera automáticamente y abre un PDF de factura."""
    archivo = f"factura_{cliente.replace(' ', '_')}_{int(datetime.now().timestamp())}.pdf"
    c = canvas.Canvas(archivo, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "FACTURA DE ALQUILER - Empresa XYZ")
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Cliente: {cliente}")
    c.drawString(50, 680, f"Equipo: {equipo}")
    c.drawString(50, 660, f"Horas alquiladas: {horas}")
    c.drawString(50, 640, f"Costo total: ${costo:.2f}")
    c.drawString(50, 620, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(50, 610, 550, 610)
    c.drawString(50, 590, "Gracias por su preferencia.")
    c.save()
    try:
        os.startfile(archivo)  # Windows: abre el PDF
    except Exception:
        pass  # en otros S.O. no hace nada

# --- Botones ---
tk.Button(ventana, text="Alquilar equipo", command=alquilar_equipo, bg="#2196F3", fg="white").place(x=350, y=30)
tk.Button(ventana, text="Eliminar registro", command=eliminar_registro, bg="#F44336", fg="white").place(x=480, y=30)
tk.Button(ventana, text="Actualizar lista", command=actualizar_lista, bg="#4CAF50", fg="white").place(x=630, y=30)
tk.Button(ventana, text="Generar factura (seleccionado)", command=lambda: (
    (messagebox.showwarning("Aviso", "Seleccione un registro.") if not tree.selection() else generar_factura_para(
        tree.item(tree.selection()[0])["values"][1],
        tree.item(tree.selection()[0])["values"][2],
        0,
        tree.item(tree.selection()[0])["values"][5]
    ))
), bg="#FFC107", fg="black").place(x=760, y=30)

# --- Inicialización ---
actualizar_lista()

ventana.mainloop()
