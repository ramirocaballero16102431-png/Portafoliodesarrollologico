import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ------------------- Configuración del servidor MySQL -------------------
HOST = "10.73.96.77"
USER = "root"
PASSWORD = "Thor3124cash$$"
DATABASE = "chinoscafe"

# Carpeta donde se guardarán las facturas
INVOICE_DIR = os.path.join(os.path.expanduser("~"), "ChinosCafe_Facturas")
os.makedirs(INVOICE_DIR, exist_ok=True)

# ------------------- Función para conectar a la BD -------------------
def conectar():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        autocommit=False
    )

# ------------------- LOGIN -------------------
def login():
    usuario = entry_usuario.get()
    clave = entry_clave.get()

    try:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=%s AND clave=%s", (usuario, clave))
        dato = cursor.fetchone()

        if dato:
            global usuario_id
            usuario_id = dato[0]
            ventana_login.destroy()
            abrir_pos()
        else:
            messagebox.showerror("Error", "Usuario o clave incorrectos")

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror("Error BD", str(e))

# ------------------- PROVEEDORES -------------------
def ventana_proveedores():
    win = tk.Toplevel()
    win.title("Gestión de Proveedores - Chino's Café")
    win.geometry("650x450")

    tk.Label(win, text="Nombre del proveedor:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Teléfono:").pack()
    entry_tel = tk.Entry(win)
    entry_tel.pack()

    tk.Label(win, text="Dirección:").pack()
    entry_dir = tk.Entry(win)
    entry_dir.pack()

    def guardar_proveedor():
        nombre = entry_nombre.get()
        tel = entry_tel.get()
        direc = entry_dir.get()

        if not nombre:
            messagebox.showwarning("Faltan datos", "Debe ingresar un nombre.")
            return

        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO proveedores (nombre, telefono, direccion) VALUES (%s, %s, %s)",
                (nombre, tel, direc)
            )
            db.commit()
            cursor.close()
            db.close()

            messagebox.showinfo("Éxito", "Proveedor guardado.")

            entry_nombre.delete(0, tk.END)
            entry_tel.delete(0, tk.END)
            entry_dir.delete(0, tk.END)

            cargar_proveedores()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Guardar Proveedor", bg="blue", fg="white", command=guardar_proveedor).pack(pady=10)

    # TABLA
    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    columnas = ("ID", "Nombre", "Teléfono", "Dirección")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
    tabla.pack(fill="both", expand=True)

    def cargar_proveedores():
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, telefono, direccion FROM proveedores")
        data = cursor.fetchall()
        tabla.delete(*tabla.get_children())
        for row in data:
            tabla.insert("", tk.END, values=row)
        cursor.close()
        db.close()

    cargar_proveedores()

# ------------------- CONTACTOS -------------------
def ventana_contactos():
    win = tk.Toplevel()
    win.title("Gestión de Contactos - Chino's Café")
    win.geometry("650x450")

    tk.Label(win, text="Nombre completo:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Correo electrónico:").pack()
    entry_correo = tk.Entry(win)
    entry_correo.pack()

    tk.Label(win, text="Mensaje:").pack()
    entry_mensaje = tk.Text(win, height=5)
    entry_mensaje.pack()

    def guardar_contacto():
        nombre = entry_nombre.get().strip()
        correo = entry_correo.get().strip()
        mensaje = entry_mensaje.get("1.0", tk.END).strip()

        if not nombre or not correo or not mensaje:
            messagebox.showwarning("Faltan datos", "Debe completar los campos obligatorios.")
            return

        try:
            db = conectar()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO contactos (nombre, correo, mensaje, fecha) VALUES (%s, %s, %s, NOW())",
                (nombre, correo, mensaje)
            )
            db.commit()
            cursor.close()
            db.close()

            messagebox.showinfo("Éxito", "Contacto guardado correctamente.")

            entry_nombre.delete(0, tk.END)
            entry_correo.delete(0, tk.END)
            entry_mensaje.delete("1.0", tk.END)

            cargar_contactos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Guardar Contacto", bg="blue", fg="white", command=guardar_contacto).pack(pady=10)

    # TABLA DE CONTACTOS
    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    columnas = ("ID", "Nombre", "Correo", "Mensaje", "Fecha")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
    tabla.pack(fill="both", expand=True)

    def cargar_contactos():
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, correo, mensaje, fecha FROM contactos ORDER BY fecha DESC")
        data = cursor.fetchall()
        tabla.delete(*tabla.get_children())
        for row in data:
            tabla.insert("", tk.END, values=row)
        cursor.close()
        db.close()

    cargar_contactos()

# ------------------- POS (VENTA) -------------------
carrito = []

def cargar_productos():
    try:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        db.close()
        return productos
    except Exception as e:
        print("Error cargar_productos:", e)
        return []

def agregar_al_carrito():
    try:
        item = combo_productos.get()
        cantidad = int(entry_cantidad.get())

        if cantidad <= 0:
            messagebox.showwarning("Error", "La cantidad debe ser mayor a 0")
            return

        parts = item.split(" | ")
        prod_id = int(parts[0])
        nombre = parts[1]
        precio = float(parts[2])
        stock = int(parts[3]) if len(parts) > 3 else None

        subtotal = cantidad * precio

        carrito.append([prod_id, nombre, cantidad, precio, subtotal])
        actualizar_tabla()
        entry_cantidad.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def actualizar_tabla():
    tabla.delete(*tabla.get_children())
    total = 0

    for item in carrito:
        tabla.insert("", tk.END, values=item)
        total += item[4]

    label_total.config(text=f"Total: ${total:.2f}")

def generar_factura_pdf(venta_id, numero_factura, usuario_nombre, items, total):
    fecha_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"factura_{numero_factura}_{fecha_str}.pdf"
    filepath = os.path.join(INVOICE_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    ancho, alto = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, alto - 50, "Chino's Café - Factura")
    c.setFont("Helvetica", 10)
    c.drawString(50, alto - 70, f"Factura: {numero_factura}")
    c.drawString(50, alto - 85, f"Venta ID: {venta_id}")
    c.drawString(50, alto - 100, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, alto - 115, f"Cajero: {usuario_nombre}")

    y = alto - 150
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Cant")
    c.drawString(100, y, "Descripción")
    c.drawString(350, y, "P. Unit")
    c.drawString(420, y, "Subtotal")
    c.setFont("Helvetica", 10)
    y -= 15

    for it in items:
        c.drawString(50, y, str(it[2]))
        c.drawString(100, y, it[1])
        c.drawRightString(400, y, f"{it[3]:.2f}")
        c.drawRightString(500, y, f"{it[4]:.2f}")
        y -= 15

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 10, f"TOTAL: ${total:.2f}")
    c.save()
    return filepath

def procesar_venta():
    if not carrito:
        messagebox.showwarning("Error", "El carrito está vacío")
        return

    total = sum([item[4] for item in carrito])

    try:
        db = conectar()
        cursor = db.cursor()

        for item in carrito:
            prod_id = item[0]
            qty = item[2]
            cursor.execute("SELECT stock, nombre FROM productos WHERE id=%s", (prod_id,))
            row = cursor.fetchone()

            if row[0] < qty:
                raise Exception(f"Stock insuficiente para {row[1]}.")

        cursor.execute(
            "INSERT INTO ventas (fecha, total, usuario_id) VALUES (%s, %s, %s)",
            (datetime.now(), total, usuario_id)
        )
        venta_id = cursor.lastrowid

        for item in carrito:
            cursor.execute(
                """INSERT INTO detalle_ventas 
                (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)""",
                (venta_id, item[0], item[2], item[3], item[4])
            )
            cursor.execute(
                "UPDATE productos SET stock = stock - %s WHERE id = %s",
                (item[2], item[0])
            )

        numero_factura = f"{venta_id:06d}"

        cursor.execute("SELECT nombre FROM usuarios WHERE id=%s", (usuario_id,))
        usuario_nombre = cursor.fetchone()[0]

        pdf_path = generar_factura_pdf(venta_id, numero_factura, usuario_nombre, carrito, total)

        cursor.execute(
            "INSERT INTO facturas (venta_id, numero_factura, archivo_pdf) VALUES (%s, %s, %s)",
            (venta_id, numero_factura, pdf_path)
        )

        db.commit()

        messagebox.showinfo("Éxito", f"Venta registrada.\nFactura: {pdf_path}")
        carrito.clear()
        actualizar_tabla()

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", str(e))

# ------------------- INTERFAZ POS -------------------
def abrir_pos():
    global combo_productos, entry_cantidad, tabla, label_total

    ventana = tk.Tk()
    ventana.title("POS - Chino's Café")
    ventana.geometry("750x550")

    # BOTONES
    tk.Button(ventana, text="Proveedores", bg="purple", fg="white",
              command=ventana_proveedores).pack(pady=10)

    tk.Button(ventana, text="Contactos", bg="orange", fg="white",
              command=ventana_contactos).pack(pady=5)

    productos = cargar_productos()
    lista_formato = [f"{p[0]} | {p[1]} | {p[2]} | {p[3]}" for p in productos]

    tk.Label(ventana, text="Producto:").pack()
    combo_productos = ttk.Combobox(ventana, values=lista_formato, width=80)
    combo_productos.pack()

    tk.Label(ventana, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()

    tk.Button(ventana, text="Agregar al carrito", command=agregar_al_carrito).pack(pady=5)

    columnas = ("ID", "Nombre", "Cantidad", "Precio", "Subtotal")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)

    tabla.pack(fill="both", expand=True)

    label_total = tk.Label(ventana, text="Total: $0.00", font=("Arial", 14))
    label_total.pack(pady=10)

    tk.Button(ventana, text="Procesar Venta", bg="green", fg="white",
              command=procesar_venta).pack(pady=10)

    ventana.mainloop()

# ------------------- LOGIN -------------------
ventana_login = tk.Tk()
ventana_login.title("Login POS")
ventana_login.geometry("300x220")

tk.Label(ventana_login, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Clave:").pack(pady=5)
entry_clave = tk.Entry(ventana_login, show="*")
entry_clave.pack()

tk.Button(ventana_login, text="Ingresar", command=login).pack(pady=15)

ventana_login.mainloop()
