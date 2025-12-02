import tkinter as tk
from tkinter import messagebox

def convertir_hora():
    hora_24 = entrada_hora.get().strip()

    # Verificar que tenga 5 caracteres (formato hh:mm)
    if len(hora_24) != 5 or hora_24[2] != ':':
        messagebox.showerror("Error", "La hora debe tener el formato hh:mm (5 caracteres).")
        return

    try:
        horas = int(hora_24[:2])
        minutos = int(hora_24[3:])
        
        if not (0 <= horas < 24 and 0 <= minutos < 60):
            raise ValueError

        # Convertir a formato 12 horas
        sufijo = "am"
        if horas >= 12:
            sufijo = "pm"
        if horas == 0:
            horas = 12
        elif horas > 12:
            horas -= 12

        # Formatear minutos con dos cifras
        hora_12 = f"{horas}:{minutos:02d} {sufijo}"
        resultado_label.config(text=f"Hora en formato 12: {hora_12}")

    except ValueError:
        messagebox.showerror("Error", "Entrada no válida. Usa el formato hh:mm con valores válidos.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Conversor de hora 24h a 12h")
ventana.geometry("350x200")

# Etiquetas y campo de entrada
tk.Label(ventana, text="Introduce la hora (hh:mm):").pack(pady=10)
entrada_hora = tk.Entry(ventana, width=10, justify="center")
entrada_hora.pack()

# Botón para convertir
tk.Button(ventana, text="Convertir", command=convertir_hora).pack(pady=10)

# Resultado
resultado_label = tk.Label(ventana, text="", font=("Arial", 12))
resultado_label.pack(pady=10)

ventana.mainloop()
