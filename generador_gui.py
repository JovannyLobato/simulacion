# Importamos las librerías necesarias para la interfaz gráfica y cálculos
import customtkinter as ctk  # Para una interfaz moderna
from ttkthemes import ThemedTk  # Para temas visuales
import tkinter as tk  # Librería base para interfaces
from tkinter import ttk, messagebox  # Componentes adicionales de tkinter
from PIL import Image, ImageTk  # Para manejar imágenes
import os  # Para operaciones con el sistema operativo
import re  # Para expresiones regulares
import subprocess  # Para ejecutar otros programas
import sys  # Para interactuar con el sistema

# Definimos colores modernos para la interfaz
PRIMARY = "#4361ee"  # Color principal (azul)
PRIMARY_DARK = "#3a56d4"  # Azul oscuro
BACKGROUND = "#f0f2f5"  # Fondo gris claro
WHITE = "#ffffff"  # Blanco
TEXT = "#22223b"  # Texto oscuro
ACCENT = "#ffd60a"  # Color de acento (amarillo)

# Configuramos el modo visual de la aplicación
ctk.set_appearance_mode("light")  # Tema claro
ctk.set_default_color_theme("blue")  # Tema azul

# --- FUNCIONES DE GENERACIÓN ---

# Función para validar que los datos ingresados sean correctos
def validar_entrada(valor, tipo="entero", campo="semilla"):
    """Valida que la entrada sea un número válido y esté dentro del rango correcto."""
    if not valor.strip():  # Si está vacío
        return False, "El campo no puede estar vacío"
    
    try:
        if tipo == "entero":  # Validar números enteros
            num = int(valor)
            if num <= 0:  # Debe ser positivo
                return False, "El número debe ser positivo"
            if campo == "semilla":  # Semilla debe tener 4 dígitos
                if num < 1000 or num > 9999:
                    return False, "La semilla debe ser un número de 4 dígitos (1000-9999)"
            return True, num  # Retorna el número si es válido
        else:  # Validar números decimales
            num = float(valor)
            if num <= 0 or num >= 1:  # Debe estar entre 0 y 1
                return False, "El número debe estar entre 0 y 1"
            return True, num
    except ValueError:  # Si no es un número
        return False, "Debe ingresar un número válido"

# Función para obtener los 4 dígitos centrales de un número
def obtener_digitos_centrales(numero):
    """Extrae los 4 dígitos del centro de un número."""
    num_str = str(numero)  # Convierte el número a texto
    if len(num_str) % 2 != 0:  # Si es impar, añade un cero al inicio
        num_str = "0" + num_str
    mitad = len(num_str) // 2  # Calcula la mitad
    centrales = num_str[mitad - 2: mitad + 2]  # Extrae los 4 dígitos centrales
    return int(centrales)  # Devuelve los dígitos como número

# Generador de números pseudoaleatorios usando el método de Cuadrados Medios
def cuadrados_medios(semilla, cantidad):
    """Generador por el metodo de cuadrados medios.
    Returns:
        list: Lista de strings con los resultados de cada paso
    """
    resultados = []
    for _ in range(cantidad):
        cuadrado = semilla ** 2
        cuadrado_str = str(cuadrado)
        if len(cuadrado_str) % 2 != 0:
            cuadrado_str = "0" + cuadrado_str
        
        mitad = len(cuadrado_str) //2
        nuevo = int(cuadrado_str[mitad - 2: mitad + 2])  # Extrae los 4 digitos centrales
        decimal = nuevo / 10000  # Convierte a decimal entre 0 y 1

        resultados.append(f"{semilla}^2 = {cuadrado} -> {nuevo} -> {decimal:.4f}")
        semilla = nuevo  # Actualiza la semilla
    return resultados

# Similar a cuadrados_medios, pero multiplica dos semillas en lugar de elevar al cuadrado
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

# Generador que multiplica la semilla por una constante fija
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
        producto_str = str(producto)
        mitad = len(producto_str) // 2
        nuevo = int(producto_str[mitad - 2: mitad + 2])  # Extrae los 4 dígitos centrales
        decimal = nuevo / 10000
        resultados.append(f"{semilla} * {constante} = {producto} -> {nuevo} -> {decimal:.4f}")
        semilla = nuevo  # Actualiza la semilla para la siguiente iteración
    return resultados

# --- INTERFAZ GRÁFICA ---
class GeneradorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Números Pseudoaleatorios")
        self.geometry("1000x800")
        self.minsize(800, 600)
        self.configure(fg_color=BACKGROUND)

        # Frame principal con scroll
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame = self.scrollable_frame

        # Configuración del tema
        try:
            from ttkthemes import ThemedStyle
            themed = ThemedStyle(self)
            themed.set_theme("arc")
        except Exception:
            pass

        # --- HEADER ---
        header = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        header.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(header, text="Generador de Números Pseudoaleatorios",
                     font=("Segoe UI Semibold", 36), text_color=PRIMARY_DARK).pack(pady=(20, 10))
        ctk.CTkLabel(header, text="Seleccione un método y configure los parámetros",
                     font=("Segoe UI", 20), text_color=TEXT).pack(pady=(0, 20))

        # --- CONFIGURACIÓN DEL MÉTODO ---
        config_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        config_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(config_frame, text="Selección del Método",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Dropdown para seleccionar el método
        self.metodo_var = ctk.StringVar(value="Cuadrados Medios")
        self.combo = ctk.CTkComboBox(
            config_frame,
            variable=self.metodo_var,
            values=["Cuadrados Medios", "Productos Medios", "Multiplicador Constante"],
            font=("Segoe UI", 18),
            width=400,
            height=45,
            corner_radius=10,
            fg_color=WHITE,
            text_color=TEXT,
            dropdown_fg_color=WHITE
        )
        self.combo.pack(pady=20)
        self.combo.bind("<<ComboboxSelected>>", self.actualizar_campos)

        # --- PARÁMETROS DE ENTRADA ---
        entrada_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        entrada_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(entrada_frame, text="Parámetros",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Frame para los campos
        campos_frame = ctk.CTkFrame(entrada_frame, fg_color=WHITE)
        campos_frame.pack(pady=20, padx=40)

        # Campos para semilla, extra y cantidad
        self.label_semilla = ctk.CTkLabel(campos_frame, text="Semilla:",
                                          font=("Segoe UI", 18), text_color=TEXT)
        self.label_semilla.grid(row=0, column=0, padx=20, pady=12, sticky="e")
        self.entry_semilla = ctk.CTkEntry(campos_frame, font=("Segoe UI", 18),
                                          width=350, height=45, corner_radius=10)
        self.entry_semilla.grid(row=0, column=1, padx=20, pady=12, sticky="w")

        self.label_extra = ctk.CTkLabel(campos_frame, text="Extra:",
                                        font=("Segoe UI", 18), text_color=TEXT)
        self.label_extra.grid(row=1, column=0, padx=20, pady=12, sticky="e")
        self.entry_extra = ctk.CTkEntry(campos_frame, font=("Segoe UI", 18),
                                        width=350, height=45, corner_radius=10)
        self.entry_extra.grid(row=1, column=1, padx=20, pady=12, sticky="w")

        self.label_cantidad = ctk.CTkLabel(campos_frame, text="Cantidad:",
                                           font=("Segoe UI", 18), text_color=TEXT)
        self.label_cantidad.grid(row=2, column=0, padx=20, pady=12, sticky="e")
        self.entry_cantidad = ctk.CTkEntry(campos_frame, font=("Segoe UI", 18),
                                           width=350, height=45, corner_radius=10)
        self.entry_cantidad.grid(row=2, column=1, padx=20, pady=12, sticky="w")

        # --- BOTÓN PRINCIPAL ---
        self.btn_generar = ctk.CTkButton(
            frame,
            text="Generar Números",
            font=("Segoe UI Semibold", 22),
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            height=50,
            corner_radius=15,
            command=self.ejecutar
        )
        self.btn_generar.pack(pady=30, padx=100, fill="x")

        # --- RESULTADOS ---
        resultados_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        resultados_frame.pack(pady=20, padx=40, fill="both", expand=True)
        ctk.CTkLabel(resultados_frame, text="Resultados",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Área de texto para mostrar resultados
        self.text_resultado = ctk.CTkTextbox(
            resultados_frame,
            font=("Consolas", 16),
            fg_color=BACKGROUND,
            height=250,
            corner_radius=10,
            text_color=TEXT
        )
        self.text_resultado.pack(padx=20, pady=20, fill="both", expand=True)

        # Botón para ir a pruebas de aleatoriedad
        self.btn_ir_pruebas = ctk.CTkButton(
            frame,
            text="Ir a Pruebas de Aleatoriedad",
            font=("Segoe UI Semibold", 22),
            fg_color=ACCENT,
            hover_color="#e6bf00",
            height=50,
            corner_radius=15,
            command=self.abrir_pruebas
        )
        self.btn_ir_pruebas.pack(pady=30, padx=100, fill="x")

        self.numeros_generados = []
        self.actualizar_campos()

    def actualizar_campos(self, event=None):
        metodo = self.metodo_var.get()
        if metodo == "Cuadrados Medios":
            self.label_semilla.configure(text="Semilla:")
            self.label_extra.grid_remove()
            self.entry_extra.grid_remove()
        elif metodo == "Productos Medios":
            self.label_semilla.configure(text="Semilla 1:")
            self.label_extra.configure(text="Semilla 2:")
            self.label_extra.grid(row=1, column=0, padx=20, pady=12, sticky="e")
            self.entry_extra.grid(row=1, column=1, padx=20, pady=12, sticky="w")
        elif metodo == "Multiplicador Constante":
            self.label_semilla.configure(text="Semilla:")
            self.label_extra.configure(text="Constante:")
            self.label_extra.grid(row=1, column=0, padx=20, pady=12, sticky="e")
            self.entry_extra.grid(row=1, column=1, padx=20, pady=12, sticky="w")

    def abrir_pruebas(self):
        if self.numeros_generados:
            datos_str = ",".join(map(str, self.numeros_generados))
            subprocess.Popen([sys.executable, "pruebas_ri.py", datos_str])
        else:
            messagebox.showinfo("Sin datos", "Primero genera los números para realizar pruebas.")

    def ejecutar(self):
        metodo = self.metodo_var.get()
        cantidad_valida, cantidad_resultado = validar_entrada(self.entry_cantidad.get(), campo="cantidad")
        if not cantidad_valida:
            messagebox.showerror("Error", f"Error en cantidad: {cantidad_resultado}")
            return
        cantidad = cantidad_resultado
        if cantidad > 1000:
            if not messagebox.askyesno("Advertencia", "La cantidad es muy grande. ¿Continuar?"):
                return
        try:
            resultados = []
            numeros_generados = []
            if metodo == "Cuadrados Medios":
                semilla_valida, semilla_resultado = validar_entrada(self.entry_semilla.get(), campo="semilla")
                if not semilla_valida:
                    messagebox.showerror("Error", f"Error en semilla: {semilla_resultado}")
                    return
                semilla = semilla_resultado
                resultados = cuadrados_medios(semilla, cantidad)
                numeros_generados = [float(r.split("->")[-1].strip()) for r in resultados]
            elif metodo == "Productos Medios":
                semilla1_valida, semilla1_resultado = validar_entrada(self.entry_semilla.get(), campo="semilla")
                semilla2_valida, semilla2_resultado = validar_entrada(self.entry_extra.get(), campo="semilla")
                if not semilla1_valida or not semilla2_valida:
                    messagebox.showerror("Error", "Error en las semillas")
                    return
                resultados = productos_medios(semilla1_resultado, semilla2_resultado, cantidad)
                numeros_generados = [float(r.split("->")[-1].strip()) for r in resultados]
            elif metodo == "Multiplicador Constante":
                semilla_valida, semilla_resultado = validar_entrada(self.entry_semilla.get(), campo="semilla")
                constante_valida, constante_resultado = validar_entrada(self.entry_extra.get(), tipo="entero")
                if not semilla_valida or not constante_valida:
                    messagebox.showerror("Error", "Error en los parámetros")
                    return
                resultados = multiplicador_constante(semilla_resultado, constante_resultado, cantidad)
                numeros_generados = [float(r.split("->")[-1].strip()) for r in resultados]
            self.text_resultado.delete(1.0, tk.END)
            for r in resultados:
                self.text_resultado.insert(tk.END, r + "\n")
            if numeros_generados:
                media = sum(numeros_generados) / len(numeros_generados)
                varianza = sum((x - media) ** 2 for x in numeros_generados) / len(numeros_generados)
                self.text_resultado.insert(tk.END, f"\nEstadísticas:\nMedia: {media:.4f}\nVarianza: {varianza:.4f}\n")
            self.numeros_generados = numeros_generados
            
            # Crear botón para realizar pruebas
            for widget in self.btn_ir_pruebas.winfo_children():
                widget.destroy()
            btn_pruebas = ctk.CTkButton(
                self.btn_ir_pruebas,
                text="Realizar Pruebas con estos Datos",
                font=("Segoe UI Semibold", 22),
                fg_color=ACCENT,
                hover_color="#e6bf00",
                height=50,
                corner_radius=15,
                command=lambda: subprocess.Popen([sys.executable, "pruebas_ri.py", ",".join(map(str, numeros_generados))])
            )
            btn_pruebas.pack(fill="x", ipady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    app = GeneradorApp()
    app.mainloop()