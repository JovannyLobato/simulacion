# Importamos librerías para pruebas estadísticas y gráficos
import customtkinter as ctk  # Interfaz moderna
from ttkthemes import ThemedTk  # Temas visuales
import tkinter as tk  # Librería base
from tkinter import ttk, messagebox  # Componentes adicionales
import statistics  # Para cálculos estadísticos
from scipy.stats import chisquare, norm, chi2  # Pruebas estadísticas
import math  # Funciones matemáticas
import subprocess  # Para ejecutar otros programas
import sys  # Interacción con el sistema
from PIL import Image, ImageTk  # Manejo de imágenes
import matplotlib.pyplot as plt  # Para gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integrar gráficos en tkinter
import numpy as np  # Cálculos numéricos

# Paleta de colores
PRIMARY = "#4361ee"  # Azul
PRIMARY_DARK = "#3a56d4"  # Azul oscuro
BACKGROUND = "#f0f2f5"  # Fondo gris claro
WHITE = "#ffffff"  # Blanco
TEXT = "#22223b"  # Texto oscuro
ACCENT = "#ffd60a"  # Amarillo

# Configuración visual
ctk.set_appearance_mode("light")  # Tema claro
ctk.set_default_color_theme("blue")  # Tema azul

# Clase principal para la interfaz de pruebas
class PruebasAleatoriedadApp(ctk.CTk):
    def __init__(self, datos=None):
        super().__init__()
        self.title("Pruebas de Aleatoriedad")
        self.geometry("1200x900")
        self.minsize(1000, 700)
        self.configure(fg_color=BACKGROUND)

        # Frame principal con scroll
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame = self.scrollable_frame

        # --- HEADER ---
        header = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        header.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(header, text="Pruebas de Aleatoriedad",
                     font=("Segoe UI Semibold", 36), text_color=PRIMARY_DARK).pack(pady=(20, 10))
        ctk.CTkLabel(header, text="Ingrese los datos para realizar las pruebas",
                     font=("Segoe UI", 20), text_color=TEXT).pack(pady=(0, 20))

        # --- DATOS DE ENTRADA ---
        entrada_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        entrada_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(entrada_frame, text="Datos de Entrada",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Campo para ingresar datos
        datos_row = ctk.CTkFrame(entrada_frame, fg_color=WHITE)
        datos_row.pack(pady=20, padx=40)
        ctk.CTkLabel(datos_row, text="Datos:",
                     font=("Segoe UI", 18), text_color=TEXT).grid(row=0, column=0, padx=20, pady=12, sticky="e")
        self.entry_datos = ctk.CTkEntry(datos_row, font=("Segoe UI", 18), width=600, height=45, corner_radius=10)
        self.entry_datos.grid(row=0, column=1, padx=20, pady=12, sticky="w")

        # Botón para abrir el generador
        ctk.CTkButton(entrada_frame, text="Abrir Generador",
                      font=("Segoe UI Semibold", 22), fg_color=ACCENT, hover_color="#e6bf00",
                      height=50, corner_radius=15, command=self.abrir_generador).pack(pady=20, padx=100, fill="x")

        # --- CONFIGURACIÓN ---
        config_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        config_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(config_frame, text="Configuración",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Frame para nivel de confianza e intervalos
        conf_row = ctk.CTkFrame(config_frame, fg_color=WHITE)
        conf_row.pack(pady=20, padx=40)

        # Nivel de confianza
        ctk.CTkLabel(conf_row, text="Nivel de Confianza:",
                     font=("Segoe UI", 18), text_color=TEXT).grid(row=0, column=0, padx=20, pady=12, sticky="e")
        self.nivel_confianza = tk.StringVar(value="95")
        confianza_box = ctk.CTkComboBox(
            conf_row, variable=self.nivel_confianza, values=["90", "95", "99"],
            font=("Segoe UI", 18), width=150, height=45, corner_radius=10,
            fg_color=WHITE, text_color=TEXT, dropdown_fg_color=WHITE
        )
        confianza_box.grid(row=0, column=1, padx=20, pady=12, sticky="w")

        # Número de intervalos
        ctk.CTkLabel(conf_row, text="Número de Intervalos:",
                     font=("Segoe UI", 18), text_color=TEXT).grid(row=1, column=0, padx=20, pady=12, sticky="e")
        self.entry_intervalos = ctk.CTkEntry(conf_row, font=("Segoe UI", 18), width=150, height=45, corner_radius=10)
        self.entry_intervalos.grid(row=1, column=1, padx=20, pady=12, sticky="w")
        self.entry_intervalos.insert(0, "10")

        # --- BOTONES DE ACCIÓN ---
        btns_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        btns_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(btns_frame, text="Pruebas Estadísticas",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Botones para realizar pruebas (sin el de estadísticas)
        btns_row = ctk.CTkFrame(btns_frame, fg_color=WHITE)
        btns_row.pack(pady=20, padx=40, fill="x")
        ctk.CTkButton(btns_row, text="Prueba de Medias",
                      font=("Segoe UI Semibold", 18), height=50, corner_radius=10,
                      fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                      command=self.calcular_prueba_medias).pack(side="left", padx=10, pady=10, fill="x", expand=True)
        ctk.CTkButton(btns_row, text="Prueba de Varianza",
                      font=("Segoe UI Semibold", 18), height=50, corner_radius=10,
                      fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                      command=self.calcular_varianza).pack(side="left", padx=10, pady=10, fill="x", expand=True)
        ctk.CTkButton(btns_row, text="Prueba de Uniformidad",
                      font=("Segoe UI Semibold", 18), height=50, corner_radius=10,
                      fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                      command=self.calcular_uniformidad).pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # --- RESULTADOS Y GRÁFICOS ---
        resultados_frame = ctk.CTkFrame(frame, fg_color=WHITE, corner_radius=20)
        resultados_frame.pack(pady=20, padx=40, fill="both", expand=True)
        ctk.CTkLabel(resultados_frame, text="Resultados y Gráficos",
                     font=("Segoe UI Semibold", 28), text_color=PRIMARY_DARK).pack(pady=(20, 10))

        # Área de texto para resultados
        self.text_resultado = ctk.CTkTextbox(
            resultados_frame, font=("Consolas", 16), fg_color=BACKGROUND,
            height=250, corner_radius=10, text_color=TEXT
        )
        self.text_resultado.pack(padx=20, pady=20, fill="both", expand=True)

        # Área para gráficos (ahora va debajo del textbox)
        self.graph_frame = ctk.CTkFrame(resultados_frame, fg_color=BACKGROUND, corner_radius=12)
        self.graph_frame.pack(padx=20, pady=(0, 20), fill="x")

        if datos:
            self.cargar_datos(datos)

    # --- FUNCIONES PRINCIPALES ---

    def validar_datos(self):
        datos_str = self.entry_datos.get()
        if not datos_str:
            return False, "No se ingresaron datos."
        try:
            datos = list(map(float, datos_str.split(",")))
            if len(datos) < 2:
                return False, "Se necesitan al menos 2 datos."
            if not all(0 <= x <= 1 for x in datos):
                return False, "Los datos deben estar entre 0 y 1."
            return True, datos
        except ValueError:
            return False, "Los datos deben ser números separados por comas."

    def cargar_datos(self, datos):
        datos_str = ",".join(map(str, datos))
        self.entry_datos.delete(0, tk.END)
        self.entry_datos.insert(0, datos_str)

    def abrir_generador(self):
        try:
            subprocess.Popen([sys.executable, "generador_gui.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el generador: {e}")

    def mostrar_grafico(self, datos, titulo, tipo="linea"):
        # Muestra el gráfico debajo del textbox de resultados
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(10, 4))
        if tipo == "linea":
            ax.plot(datos, 'b-', alpha=0.7, linewidth=2)
        elif tipo == "histograma":
            ax.hist(datos, bins=min(20, len(datos)), alpha=0.7, color=PRIMARY)
        elif tipo == "barras":
            x = np.arange(len(datos))
            ax.bar(x, datos, width=0.35, alpha=0.7, color=PRIMARY)
        ax.set_title(titulo, fontsize=16, pad=15, color=PRIMARY_DARK)
        ax.grid(True, alpha=0.3)
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def mostrar_resultado(self, texto):
        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert(tk.END, texto)
        self.text_resultado.see("1.0")

    def calcular_estadisticas(self):
        valido, resultado = self.validar_datos()
        if not valido:
            messagebox.showerror("Error", resultado)
            return
        datos = resultado
        media = statistics.mean(datos)
        varianza = statistics.variance(datos)
        desv_std = statistics.stdev(datos)
        minimo = min(datos)
        maximo = max(datos)
        
        resultado = (
            f"Estadísticas Básicas:\n"
            f"Media: {media:.6f}\n"
            f"Varianza: {varianza:.6f}\n"
            f"Desviación Estándar: {desv_std:.6f}\n"
            f"Mínimo: {minimo:.6f}\n"
            f"Máximo: {maximo:.6f}\n"
            f"Cantidad de datos: {len(datos)}"
        )
        self.mostrar_resultado(resultado)
        self.mostrar_grafico(datos, "Distribución de Datos")

    def calcular_prueba_medias(self):
        valido, resultado = self.validar_datos()
        if not valido:
            messagebox.showerror("Error", resultado)
            return
        datos = resultado
        confianza = float(self.nivel_confianza.get())
        alpha = (100 - confianza) / 100
        n = len(datos)
        media = statistics.mean(datos)
        
        z = norm.ppf(1 - alpha / 2)
        li = 0.5 - z * (1 / (math.sqrt(12 * n)))
        ls = 0.5 + z * (1 / (math.sqrt(12 * n)))
        
        pasa_prueba = li <= media <= ls
        
        resultado = (
            f"Prueba de Medias (Confianza: {confianza}%)\n"
            f"Media observada: {media:.6f}\n"
            f"Límite inferior: {li:.6f}\n"
            f"Límite superior: {ls:.6f}\n"
            f"Conclusión: {'Pasa la prueba' if pasa_prueba else 'No pasa la prueba'}"
        )
        self.mostrar_resultado(resultado)
        self.mostrar_grafico(datos, "Prueba de Medias", tipo="linea")

    def calcular_varianza(self):
        valido, resultado = self.validar_datos()
        if not valido:
            messagebox.showerror("Error", resultado)
            return
        datos = resultado
        confianza = float(self.nivel_confianza.get())
        alpha = (100 - confianza) / 100
        n = len(datos)
        media = statistics.mean(datos)
        varianza = statistics.variance(datos)
        suma = sum((x - media) ** 2 for x in datos)
        
        chi2_li = chi2.ppf(alpha / 2, df=n - 1)
        chi2_ls = chi2.ppf(1 - alpha / 2, df=n - 1)
        li = chi2_li / (12 * (n - 1))
        ls = chi2_ls / (12 * (n - 1))
        
        pasa_prueba = li <= varianza <= ls
        
        resultado = (
            f"Prueba de Varianza (Confianza: {confianza}%)\n"
            f"Varianza observada: {varianza:.8f}\n"
            f"Límite inferior: {li:.8f}\n"
            f"Límite superior: {ls:.8f}\n"
            f"Conclusión: {'Pasa la prueba' if pasa_prueba else 'No pasa la prueba'}"
        )
        self.mostrar_resultado(resultado)
        self.mostrar_grafico(datos, "Prueba de Varianza", tipo="histograma")

    def calcular_uniformidad(self):
        valido, resultado = self.validar_datos()
        if not valido:
            messagebox.showerror("Error", resultado)
            return
        datos = resultado
        confianza = float(self.nivel_confianza.get())
        alpha = (100 - confianza) / 100
        k = int(self.entry_intervalos.get())
        n = len(datos)
        esperado = n / k
        
        frec_obs = [0] * k
        for d in datos:
            idx = min(int(d * k), k - 1)
            frec_obs[idx] += 1
        
        chi2_valor, p = chisquare(f_obs=frec_obs, f_exp=[esperado] * k)
        chi2_tabla = chi2.ppf(1 - alpha, k - 1)
        pasa_prueba = chi2_valor <= chi2_tabla
        
        resultado = (
            f"Prueba de Uniformidad (Confianza: {confianza}%)\n"
            f"Chi-Cuadrada calculada: {chi2_valor:.4f}\n"
            f"Chi-Cuadrada teórica: {chi2_tabla:.4f}\n"
            f"Valor p: {p:.4f}\n"
            f"Conclusión: {'Pasa la prueba' if pasa_prueba else 'No pasa la prueba'}\n\n"
            f"Distribución de frecuencias:\n"
            f"{'Intervalo':<15} {'Observado':<12} {'Esperado':<12}\n"
        )
        for i in range(k):
            inf = i / k
            sup = (i + 1) / k
            resultado += f"[{inf:.1f}-{sup:.1f}){' ':<5} {frec_obs[i]:<12} {esperado:.1f}\n"
        
        self.mostrar_resultado(resultado)
        # Gráfico de barras debajo del textbox
        self.mostrar_grafico(frec_obs, "Distribución de Frecuencias", tipo="barras")

if __name__ == "__main__":
    datos = None
    if len(sys.argv) > 1:
        datos = sys.argv[1].split(",")
    app = PruebasAleatoriedadApp(datos)
    app.mainloop()