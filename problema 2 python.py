import tkinter as tk
from tkinter import messagebox

def calcular_totales():
    try:
        # Leer entradas
        ventas_cola = int(entrada_cola_ventas.get())
        precio_cola = float(entrada_cola_precio.get())

        ventas_naranja = int(entrada_naranja_ventas.get())
        precio_naranja = float(entrada_naranja_precio.get())

        ventas_limon = int(entrada_limon_ventas.get())
        precio_limon = float(entrada_limon_precio.get())

        # Validar límites
        if any(v > 5000000 for v in [ventas_cola, ventas_naranja, ventas_limon]):
            messagebox.showerror("Error", "La cantidad vendida no puede superar 5,000,000 unidades.")
            return

        # Calcular totales
        total_cola = ventas_cola * precio_cola
        total_naranja = ventas_naranja * precio_naranja
        total_limon = ventas_limon * precio_limon
        total_general = total_cola + total_naranja + total_limon

        # Mostrar resultados con 2 decimales
        resultado_text.delete("1.0", tk.END)
        resultado_text.insert(tk.END, "Producto\tVentas\tPrecio\tTotal\n")
        resultado_text.insert(tk.END, "------------------------------------\n")
        resultado_text.insert(tk.END, f"Cola\t{ventas_cola}\t{precio_cola:.2f}\t{total_cola:.2f}\n")
        resultado_text.insert(tk.END, f"Naranja\t{ventas_naranja}\t{precio_naranja:.2f}\t{total_naranja:.2f}\n")
        resultado_text.insert(tk.END, f"Limon\t{ventas_limon}\t{precio_limon:.2f}\t{total_limon:.2f}\n")
        resultado_text.insert(tk.END, "------------------------------------\n")
        resultado_text.insert(tk.END, f"TOTAL\t\t\t{total_general:.2f}\n")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

# Ventana principal
ventana = tk.Tk()
ventana.title("Informe de Ventas de Refrescos")
ventana.geometry("480x420")

# Sección de Cola
tk.Label(ventana, text="Cola").grid(row=0, column=0, padx=10, pady=5)
tk.Label(ventana, text="Ventas:").grid(row=0, column=1)
entrada_cola_ventas = tk.Entry(ventana, width=10)
entrada_cola_ventas.grid(row=0, column=2)
tk.Label(ventana, text="Precio:").grid(row=0, column=3)
entrada_cola_precio = tk.Entry(ventana, width=10)
entrada_cola_precio.grid(row=0, column=4)

# Sección de Naranja
tk.Label(ventana, text="Naranja").grid(row=1, column=0, padx=10, pady=5)
tk.Label(ventana, text="Ventas:").grid(row=1, column=1)
entrada_naranja_ventas = tk.Entry(ventana, width=10)
entrada_naranja_ventas.grid(row=1, column=2)
tk.Label(ventana, text="Precio:").grid(row=1, column=3)
entrada_naranja_precio = tk.Entry(ventana, width=10)
entrada_naranja_precio.grid(row=1, column=4)

# Sección de Limón
tk.Label(ventana, text="Limón").grid(row=2, column=0, padx=10, pady=5)
tk.Label(ventana, text="Ventas:").grid(row=2, column=1)
entrada_limon_ventas = tk.Entry(ventana, width=10)
entrada_limon_ventas.grid(row=2, column=2)
tk.Label(ventana, text="Precio:").grid(row=2, column=3)
entrada_limon_precio = tk.Entry(ventana, width=10)
entrada_limon_precio.grid(row=2, column=4)

# Botón para calcular
tk.Button(ventana, text="Calcular Totales", command=calcular_totales).grid(row=3, column=0, columnspan=5, pady=10)

# Cuadro de resultados
resultado_text = tk.Text(ventana, height=10, width=55)
resultado_text.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

ventana.mainloop()
