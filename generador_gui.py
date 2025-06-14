import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# --- FUNCIONES DE GENERACION ---

def cuadrados_medios(semilla, cantidad):
    """Generador por el metodo de cuadrados medios.
    Returns:
        list: Lista de strings con los resultados de cada paso
    """
    resultados = []
    for _ in range(cantidad):
        cuadrado = semilla ** 2
        cuadrado_str = str(cuadrado).zfill(8)  # asegura 8 digitos, rellena con ceros si es necesario
        mitad = len(cuadrado_str) 
        nuevo = int(cuadrado_str[mitad - 2: mitad + 2])  # Extrae los 4 digitos centrales
        decimal = nuevo / 10000  # Convierte a decimal entre 0 y 1
        resultados.append(f"{semilla}^2 = {cuadrado} -> {nuevo} -> {decimal:.4f}")
        semilla = nuevo  # Actualiza la semilla para la siguiente iteracion
    return resultados

def productos_medios(x0, x1, cantidad):
    """Generador por el metodo de productos medios.
    x0 = semilla 1
    x1 = semilla 2
    Returns:
        list: Lista de strings con los resultados de cada paso
    """
    resultados = []
    for _ in range(cantidad):
        producto = x0 * x1
        producto_str = str(producto).zfill(8)  # asegura 8 digitos
        mitad = len(producto_str) // 2
        nuevo = int(producto_str[mitad - 2: mitad + 2])  # Extrae los 4 digitos centrales
        decimal = nuevo / 10000
        resultados.append(f"{x0} * {x1} = {producto} -> {nuevo} -> {decimal:.4f}")
        x0, x1 = x1, nuevo  # Actualiza las semillas para la siguiente iteracion
    return resultados

def multiplicador_constante(semilla, constante, cantidad):
    """Generador por el metodo del multiplicador constante.
    Args:
        semilla (int): numero inicial para generar la secuencia
        constante (int): Constante multiplicativa
        cantidad (int): Cantidad de numeros a generar
    Returns:
        list: Lista de strings con los resultados de cada paso
    """
    resultados = []
    for _ in range(cantidad):
        producto = semilla * constante
        producto_str = str(producto).zfill(8)  # Asegura 8 dígitos
        mitad = len(producto_str) // 2
        nuevo = int(producto_str[mitad - 2: mitad + 2])  # Extrae los 4 dígitos centrales
        decimal = nuevo / 10000
        resultados.append(f"{semilla} * {constante} = {producto} -> {nuevo} -> {decimal:.4f}")
        semilla = nuevo  # Actualiza la semilla para la siguiente iteración
    return resultados

# --- FUNCION PRINCIPAL DE EJECUCION ---
import subprocess
import sys

def ejecutar():
    """Obtiene los datos de la interfaz, ejecuta el metodo seleccionado y muestra los resultados."""
    metodo = metodo_var.get()  # Obtiene el metodo seleccionado del combobox
    try:
        cantidad = int(entry_cantidad.get())  # obtiene la cantidad de numeros a generar
        resultados = []
        numeros_generados = []
        
        # Ejecuta el metodo seleccionado con los parametros correspondientes
        if metodo == "Cuadrados Medios":
            if( (int(entry_semilla.get())) <10000 and (int(entry_semilla.get()) > 999)):
                semilla = int(entry_semilla.get())
                resultados = cuadrados_medios(semilla, cantidad)
                # Extrae solo los numeros decimales generados para las pruebas
                numeros_generados = [float(r.split("->")[-1].strip()) for r in resultados]
            else:
                messagebox.showerror("Error", "La semilla debe de tener 4 digitos")
                return
            
        elif metodo == "Productos Medios":
            x0 = int(entry_semilla.get())
            x1 = int(entry_extra.get())
            if(x0 < 10000 and x0 > 999 and x1 < 10000 and x1 > 999):       
                resultados = productos_medios(x0, x1, cantidad)
                numeros_generados = [float(r.split("->")[-1].strip()) for r in resultados]
            else:
                messagebox.showerror("Error", "Ambas semillas deben de tener 4 dígitos")
                return
        elif metodo == "Multiplicador Constante":
            semilla = int(entry_semilla.get())
            constante = int(entry_extra.get())
            if(semilla < 10000 and semilla > 999 and constante < 10000 and constante > 999):
                resultados = multiplicador_constante(semilla, constante, cantidad)
                numeros_generados = [float(r.split("->")[-1].strip()) for r in resultados]
            else:
                messagebox.showerror("Error", "Ambas, semilla y constante deben de tener 4 dígitos")
                return
        else:
            resultados = ["Selecciona un método válido."]
        
        # Limpia y muestra los resultados en el textbox
        text_resultado.delete(1.0, tk.END)
        for r in resultados:
            text_resultado.insert(tk.END, r + "\n")
            
        # Crea botón para abrir pruebas con los datos generados
        btn_pruebas = ttk.Button(
            btn_pruebas_frame,
            text="Realizar Pruebas con estos Datos",
            command=lambda: subprocess.Popen([sys.executable, "pruebas_ri.py", 
            ",".join(map(str, numeros_generados))]),
            style="TButton"
        )
        btn_pruebas.grid(row=0, column=0, sticky="ew", ipady=5)
        
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numericos válidos.")

# --- ACTUALIZA LOS CAMPOS SEGUN EL METODO SELECCIONADO ---
def actualizar_campos(*args):
    """Muestra u oculta los campos según el metodo seleccionado."""
    metodo = metodo_var.get()  # Obtiene el método seleccionado
    
    # oculta todos los campos extra inicialmente
    label_extra.grid_remove()
    entry_extra.grid_remove()
    # label_cantidad.grid_remove()
    # entry_cantidad.grid_remove()
    btn.grid_remove()

    # Configura los campos segun el metodo seleccionado
    if metodo == "Cuadrados Medios":
        label_semilla.config(text="Semilla:")
        label_cantidad.grid(row=3, column=0, sticky="e", pady=4)
        entry_cantidad.grid(row=3, column=1, sticky="ew", pady=4)
        btn.grid(row=4, column=0, columnspan=2, pady=18, sticky="ew")
    elif metodo == "Productos Medios":
        label_semilla.config(text="Semilla 1:")
        label_extra.config(text="Semilla 2:")
        label_extra.grid(row=3, column=0, sticky="e", pady=4)
        entry_extra.grid(row=3, column=1, sticky="ew", pady=4)
        label_cantidad.grid(row=4, column=0, sticky="e", pady=4)
        entry_cantidad.grid(row=4, column=1, sticky="ew", pady=4)
        btn.grid(row=5, column=0, columnspan=2, pady=18, sticky="ew")
    elif metodo == "Multiplicador Constante":
        label_semilla.config(text="Semilla:")
        label_extra.config(text="Constante:")
        label_extra.grid(row=3, column=0, sticky="e", pady=4)
        entry_extra.grid(row=3, column=1, sticky="ew", pady=4)
        label_cantidad.grid(row=4, column=0, sticky="e", pady=4)
        entry_cantidad.grid(row=4, column=1, sticky="ew", pady=4)
        btn.grid(row=5, column=0, columnspan=2, pady=18, sticky="ew")

# --- CONFIGURACION DE LA INTERFAZ ---
root = tk.Tk()
root.title("Generador de Numeros Pseudoaleatorios")
root.geometry("900x800")
root.minsize(600, 500)
root.resizable(True, True)
root.configure(bg="#f0f2f5")

# Configurar el grid principal
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame principal
main_frame = ttk.Frame(root, style="TFrame")
main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
main_frame.grid_rowconfigure(4, weight=1)  # La fila de resultados se expandirá
main_frame.grid_columnconfigure(0, weight=1)

# Establecer estilo moderno
style = ttk.Style()
style.theme_use("clam")

# Configurar colores y estilos para los widgets
style.configure("TFrame", background="#f0f2f5")
style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 11))
style.configure("TButton", 
                font=("Segoe UI", 11, "bold"), 
                padding=10,
                background="#4361ee",
                foreground="white",
                borderwidth=0,
                focusthickness=3,
                focuscolor="#4361ee")
style.map("TButton",
          background=[("active", "#3a56d4"), ("pressed", "#2d44b3")],
          relief=[("pressed", "flat"), ("!pressed", "flat")])
style.configure("TCombobox", 
                font=("Segoe UI", 11),
                padding=8,
                selectbackground="#4361ee",
                fieldbackground="white",
                borderwidth=1,
                relief="solid")
style.configure("TEntry", 
                font=("Segoe UI", 11),
                padding=8,
                fieldbackground="white",
                borderwidth=1,
                relief="solid")
style.configure("TLabelframe", 
                background="#f0f2f5",
                font=("Segoe UI", 11, "bold"),
                borderwidth=2,
                relief="solid")
style.configure("TLabelframe.Label", 
                background="#f0f2f5",
                font=("Segoe UI", 11, "bold"),
                foreground="#2b2d42")

# Encabezado con título y subtítulo
header_frame = ttk.Frame(main_frame, style="TFrame")
header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
header_frame.grid_columnconfigure(0, weight=1)

title_label = tk.Label(
    header_frame,
    text="Generador de Números Pseudoaleatorios",
    font=("Segoe UI", 24, "bold"),
    bg="#f0f2f5",
    fg="#2b2d42"
)
title_label.grid(row=0, column=0)

subtitle_label = tk.Label(
    header_frame,
    text="Seleccione un método y complete los parámetros requeridos",
    font=("Segoe UI", 12),
    bg="#f0f2f5",
    fg="#6c757d"
)
subtitle_label.grid(row=1, column=0, pady=(5, 0))

# Variable del método seleccionado
metodo_var = tk.StringVar(value="Cuadrados Medios")
metodo_var.trace("w", actualizar_campos)

# Frame para el método
method_frame = ttk.LabelFrame(main_frame, text="Configuración del Método", padding="15 10", style="TFrame")
method_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
method_frame.grid_columnconfigure(1, weight=1)

# Selector de método
ttk.Label(method_frame, text="Método de generación:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=8)
metodos = ["Cuadrados Medios", "Productos Medios", "Multiplicador Constante"]
combo = ttk.Combobox(
    method_frame, 
    textvariable=metodo_var, 
    values=metodos, 
    state="readonly",
    font=("Segoe UI", 11)
)
combo.grid(row=0, column=1, padx=(20, 0), sticky="ew", pady=8)

# Campos de entrada
input_frame = ttk.LabelFrame(main_frame, text="Parámetros de Entrada", padding="15 10", style="TFrame")
input_frame.grid(row=2, column=0, sticky="ew", pady=10)
input_frame.grid_columnconfigure(1, weight=1)

# Campo para la primera semilla
label_semilla = ttk.Label(input_frame, text="Semilla:", font=("Segoe UI", 11))
label_semilla.grid(row=0, column=0, sticky="e", pady=10, padx=(0, 20))
entry_semilla = ttk.Entry(input_frame, font=("Segoe UI", 11))
entry_semilla.grid(row=0, column=1, sticky="ew", pady=10)

# Campo extra
label_extra = ttk.Label(input_frame, text="Extra:", font=("Segoe UI", 11))
entry_extra = ttk.Entry(input_frame, font=("Segoe UI", 11))

# Campo para la cantidad
label_cantidad = ttk.Label(input_frame, text="Cantidad:", font=("Segoe UI", 11))
entry_cantidad = ttk.Entry(input_frame, font=("Segoe UI", 11))
label_cantidad.grid(row=4, column=0, sticky="e", pady=4)
entry_cantidad.grid(row=4, column=1, sticky="ew", pady=4)

# Botón para ejecutar
btn_frame = ttk.Frame(main_frame, style="TFrame")
btn_frame.grid(row=3, column=0, sticky="ew", pady=(15, 0))
btn_frame.grid_columnconfigure(0, weight=1)

btn = ttk.Button(
    btn_frame, 
    text="Generar Números", 
    command=ejecutar,
    style="TButton"
)
btn.grid(row=0, column=0, sticky="ew", ipady=10)

# Área de resultados
result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="15 10", style="TFrame")
result_frame.grid(row=4, column=0, sticky="nsew", pady=(15, 0))
result_frame.grid_rowconfigure(1, weight=1)  # La fila del textbox se expandir
result_frame.grid_columnconfigure(0, weight=1)

# Frame para el botón de pruebas
btn_pruebas_frame = ttk.Frame(result_frame, style="TFrame")
btn_pruebas_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
btn_pruebas_frame.grid_columnconfigure(0, weight=1)

# Textbox de resultados
text_resultado = tk.Text(
    result_frame, 
    font=("Consolas", 11),
    bg="white",
    bd=2,
    relief="solid",
    padx=20,
    pady=20,
    wrap="word",
    height=20  # Altura mínima
)
text_resultado.grid(row=1, column=0, sticky="nsew")

# Scrollbar para el textbox
text_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=text_resultado.yview)
text_scrollbar.grid(row=1, column=1, sticky="ns")
text_resultado.configure(yscrollcommand=text_scrollbar.set)

# Centrar la ventana
root.eval('tk::PlaceWindow . center')

# Iniciar la aplicacion
root.mainloop()
