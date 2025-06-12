import tkinter as tk
from tkinter import ttk, messagebox
import statistics
from scipy.stats import chisquare, norm, chi2
import math
import subprocess
import sys
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PruebasAleatoriedadApp:
    def __init__(self, root, datos=None):
        """Inicializa la aplicación de pruebas de aleatoriedad.
        Args:
            root: Ventana principal de Tkinter
            datos (list, optional): Datos numéricos para analizar. Defaults to None.
        """
        self.root = root
        self.root.title("Pruebas de Aleatoriedad")
        self.root.geometry("1100x950")
        self.root.minsize(700, 600)
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f2f5")

        # Crear canvas principal con scrollbar
        self.canvas = tk.Canvas(self.root, bg="#f0f2f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # Configurar el canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Empaquetar el canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Crear frame principal dentro del canvas
        self.main_frame = ttk.Frame(self.canvas, style="TFrame")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configurar el grid principal
        self.main_frame.grid_rowconfigure(4, weight=1)  # La fila de resultados se expandirá
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar el evento de redimensionamiento
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Configurar el scroll con la rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.setup_styles()
        self.create_widgets()
        if datos:
            self.cargar_datos(datos)

    def setup_styles(self):
        """Configura los estilos visuales de los widgets."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configuración de estilos modernos
        self.style.configure("TFrame", background="#f0f2f5")
        self.style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 11))
        self.style.configure("TButton", 
                           font=("Segoe UI", 11, "bold"), 
                           padding=10,
                           background="#4361ee",
                           foreground="white",
                           borderwidth=0,
                           focusthickness=3,
                           focuscolor="#4361ee")
        self.style.map("TButton",
                      background=[("active", "#3a56d4"), ("pressed", "#2d44b3")],
                      relief=[("pressed", "flat"), ("!pressed", "flat")])
        self.style.configure("TEntry", 
                           font=("Segoe UI", 11),
                           padding=8,
                           fieldbackground="white",
                           borderwidth=1,
                           relief="solid")
        self.style.configure("TRadiobutton", 
                           background="#f0f2f5", 
                           font=("Segoe UI", 11))
        self.style.configure("TLabelframe", 
                           background="#f0f2f5",
                           font=("Segoe UI", 11, "bold"),
                           borderwidth=2,
                           relief="solid")
        self.style.configure("TLabelframe.Label", 
                           background="#f0f2f5",
                           font=("Segoe UI", 11, "bold"),
                           foreground="#2b2d42")

    def create_widgets(self):
        """Crea y organiza todos los widgets de la interfaz."""
        self.create_header()
        self.create_input_section()
        self.create_config_section()
        self.create_buttons_section()
        self.create_results_section()

    def create_header(self):
        """Crea el encabezado con título y subtítulo."""
        header_frame = ttk.Frame(self.main_frame, style="TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(header_frame, text="Pruebas de Aleatoriedad", 
                font=("Segoe UI", 24, "bold"), bg="#f0f2f5", fg="#2b2d42").grid(row=0, column=0)
        tk.Label(header_frame, text="Ingrese los datos para realizar las pruebas estadísticas", 
                font=("Segoe UI", 12), bg="#f0f2f5", fg="#6c757d").grid(row=1, column=0, pady=(5, 0))

    def create_input_section(self):
        """Crea la sección de entrada de datos."""
        input_frame = ttk.LabelFrame(self.main_frame, text="Datos de Entrada", padding="15 10", style="TFrame")
        input_frame.grid(row=1, column=0, sticky="ew", pady=10)
        input_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Datos (separados por comas):", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=10)
        self.entry_datos = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.entry_datos.grid(row=0, column=1, sticky="ew", pady=10, padx=5)
        
        btn_generador = ttk.Button(input_frame, text="Abrir Generador", 
                                 command=self.abrir_generador, style="TButton")
        btn_generador.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

    def create_config_section(self):
        """Crea la sección de configuración de pruebas."""
        config_frame = ttk.LabelFrame(self.main_frame, text="Configuración", padding="15 10", style="TFrame")
        config_frame.grid(row=2, column=0, sticky="ew", pady=10)
        config_frame.grid_columnconfigure(3, weight=1)
        
        # Nivel de confianza
        ttk.Label(config_frame, text="Nivel de confianza:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=10)
        self.nivel_confianza = tk.StringVar(value="95")
        ttk.Radiobutton(config_frame, text="90%", variable=self.nivel_confianza, value="90").grid(row=0, column=1, sticky="w", padx=15)
        ttk.Radiobutton(config_frame, text="95%", variable=self.nivel_confianza, value="95").grid(row=0, column=2, sticky="w", padx=15)
        ttk.Radiobutton(config_frame, text="99%", variable=self.nivel_confianza, value="99").grid(row=0, column=3, sticky="w", padx=15)
        
        # Número de intervalos
        ttk.Label(config_frame, text="Número de intervalos (uniformidad):", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_intervalos = ttk.Entry(config_frame, width=20, font=("Segoe UI", 11))
        self.entry_intervalos.grid(row=1, column=1, sticky="w", pady=10, padx=5)
        self.entry_intervalos.insert(0, "10")
        
        # Límites manuales
        ttk.Label(config_frame, text="Límite inferior (opcional):", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=10)
        self.entry_li = ttk.Entry(config_frame, width=20, font=("Segoe UI", 11))
        self.entry_li.grid(row=2, column=1, sticky="w", pady=10, padx=5)
        
        ttk.Label(config_frame, text="Límite superior (opcional):", font=("Segoe UI", 11)).grid(row=2, column=2, sticky="w", pady=10)
        self.entry_ls = ttk.Entry(config_frame, width=20, font=("Segoe UI", 11))
        self.entry_ls.grid(row=2, column=3, sticky="w", pady=10, padx=5)

    def create_buttons_section(self):
        """Crea los botones para realizar las diferentes pruebas."""
        buttons_frame = ttk.Frame(self.main_frame, style="TFrame")
        buttons_frame.grid(row=3, column=0, sticky="ew", pady=15)
        buttons_frame.grid_columnconfigure(3, weight=1)
        
        ttk.Button(buttons_frame, text="Calcular Estadísticas", 
                  command=self.calcular_estadisticas, style="TButton").grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(buttons_frame, text="Prueba de Medias", 
                  command=self.calcular_prueba_medias, style="TButton").grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(buttons_frame, text="Prueba de Varianza", 
                  command=self.calcular_varianza, style="TButton").grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(buttons_frame, text="Prueba de Uniformidad", 
                  command=self.calcular_uniformidad, style="TButton").grid(row=0, column=3, padx=5, sticky="ew")

    def create_results_section(self):
        """Crea el área de resultados con un textbox grande."""
        result_frame = ttk.LabelFrame(self.main_frame, text="Resultados", padding="15 10", style="TFrame")
        result_frame.grid(row=4, column=0, sticky="nsew", pady=10)
        result_frame.grid_rowconfigure(1, weight=1)  # La fila del textbox se expandirá
        result_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para el gráfico
        self.graph_frame = ttk.Frame(result_frame, style="TFrame")
        self.graph_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.graph_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para el textbox y sus scrollbars
        text_frame = ttk.Frame(result_frame, style="TFrame")
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Textbox de resultados
        self.text_resultado = tk.Text(
            text_frame,
            font=("Consolas", 11),
            bg="white",
            bd=2,
            relief="solid",
            padx=20,
            pady=20,
            wrap="none",  # Desactivar el wrap para permitir scroll horizontal
            height=20,    # Altura mínima
            width=80      # Ancho mínimo
        )
        self.text_resultado.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar vertical
        v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_resultado.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Scrollbar horizontal
        h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=self.text_resultado.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configurar los scrollbars
        self.text_resultado.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )

    def cargar_datos(self, datos):
        """Carga datos en el campo de entrada.
        Args:
            datos (list or str): Datos a cargar
        """
        if isinstance(datos, (list, tuple)):
            datos_str = ",".join(map(str, datos))
        else:
            datos_str = str(datos)
        self.entry_datos.delete(0, tk.END)
        self.entry_datos.insert(0, datos_str)

    def abrir_generador(self):
        """Abre el generador de números pseudoaleatorios."""
        try:
            subprocess.Popen([sys.executable, "generador_gui.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el generador: {e}")

    def mostrar_grafico(self, datos, titulo):
        """Muestra un gráfico de los datos en el frame de gráficos."""
        # Limpia el frame de gráficos
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        # Crea la figura y el gráfico
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(datos, 'b-', alpha=0.7, linewidth=2)
        ax.set_title(titulo, fontsize=12, pad=15)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#f0f2f5')
        
        # Integra el gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def calcular_estadisticas(self):
        """Calcula y muestra estadísticas básicas de los datos."""
        try:
            datos = self.obtener_datos()
            media = statistics.mean(datos)
            varianza = statistics.variance(datos)
            resultado = f"Media: {media:.4f}\nVarianza: {varianza:.4f}"
            self.mostrar_resultado(resultado)
            self.mostrar_grafico(datos, "Distribución de Datos")
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def calcular_prueba_medias(self):
        """Realiza la prueba de medias para verificar si la media está dentro del rango esperado."""
        try:
            datos = self.obtener_datos()
            confianza = float(self.nivel_confianza.get())
            alpha = (100 - confianza) / 100
            n = len(datos)
            media = statistics.mean(datos)
            
            li_manual = self.entry_li.get()
            ls_manual = self.entry_ls.get()
            if li_manual and ls_manual:
                li = float(li_manual)
                ls = float(ls_manual)
                fuente_limites = "especificados manualmente"
            else:
                z = norm.ppf(1 - alpha / 2)
                li = 0.5 - z * (1 / (math.sqrt(12 * n)))
                ls = 0.5 + z * (1 / (math.sqrt(12 * n)))
                fuente_limites = "calculados automáticamente"
            
            resultado = (f"Prueba de Medias (Nivel de confianza: {confianza}%)\n"
                        f"Media observada: {media:.6f}\n"
                        f"Límite inferior ({fuente_limites}): {li:.6f}\n"
                        f"Límite superior ({fuente_limites}): {ls:.6f}\n"
                        f"Conclusión: {'Pasa la prueba' if li <= media <= ls else 'No pasa la prueba'}")
            self.mostrar_resultado(resultado)
            self.mostrar_grafico(datos, "Prueba de Medias")
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def calcular_varianza(self):
        """Realiza la prueba de varianza para verificar si la varianza es consistente."""
        try:
            datos = self.obtener_datos()
            confianza = float(self.nivel_confianza.get())
            alpha = (100 - confianza) / 100
            n = len(datos)
            media = statistics.mean(datos)
            
            suma = sum((x - media) ** 2 for x in datos)
            varianza = suma
            
            chi2_li = chi2.ppf(alpha / 2, df=n - 1)
            chi2_ls = chi2.ppf(1 - alpha / 2, df=n - 1)
            
            li = chi2_li / (12 * (n - 1))
            ls = chi2_ls / (12 * (n - 1))
            
            resultado = (f"Prueba de Varianza (Nivel de confianza: {confianza}%)\n"
                        f"Varianza observada: {varianza:.8f}\n"
                        f"Límite inferior: {li:.8f}\n"
                        f"Límite superior: {ls:.8f}\n"
                        f"Conclusión: {'Pasa la prueba' if li <= varianza <= ls else 'No pasa la prueba'}")
            self.mostrar_resultado(resultado)
            self.mostrar_grafico(datos, "Prueba de Varianza")
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def calcular_uniformidad(self):
        """Realiza la prueba chi-cuadrada para verificar uniformidad de los datos."""
        try:
            datos = self.obtener_datos()
            confianza = float(self.nivel_confianza.get())
            alpha = (100 - confianza) / 100
            k = int(self.entry_intervalos.get()) if self.entry_intervalos.get() else 10
            n = len(datos)
            esperado = n / k
            
            frec_obs = [0] * k
            for d in datos:
                idx = min(int(d * k), k - 1)
                frec_obs[idx] += 1
            
            frec_esp = [esperado] * k
            
            chi2_valor, p = chisquare(f_obs=frec_obs, f_exp=frec_esp)
            chi2_tabla = chi2.ppf(1 - alpha, k - 1)
            
            resultado = (
                f"Prueba de Uniformidad (Nivel de confianza: {confianza}%)\n"
                f"Chi-Cuadrada calculada: {chi2_valor:.4f}\n"
                f"Chi-Cuadrada teórica: {chi2_tabla:.4f}\n"
                f"Valor p: {p:.4f}\n"
                f"Conclusión: {'Pasa la prueba' if chi2_valor <= chi2_tabla else 'No pasa la prueba'}\n\n"
                f"Distribución de frecuencias por intervalo:\n"
            )
            
            # Formatear la tabla de frecuencias
            resultado += f"{'Intervalo':<15} {'Observado':<12} {'Esperado':<12}\n"
            resultado += "-" * 40 + "\n"
            
            for i in range(k):
                inf = i / k
                sup = (i + 1) / k
                resultado += f"[{inf:.1f}-{sup:.1f}){' ':<5} {frec_obs[i]:<12} {esperado:.1f}\n"
            
            self.mostrar_resultado(resultado)
            
            # Gráfico de barras para la prueba de uniformidad
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(range(k), frec_obs, alpha=0.7, label='Observado', color='#4361ee')
            ax.axhline(y=esperado, color='#dc3545', linestyle='--', label='Esperado', linewidth=2)
            ax.set_title("Distribución de Frecuencias", fontsize=12, pad=15)
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('#f0f2f5')
            
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def obtener_datos(self):
        """Obtiene y valida los datos ingresados por el usuario.
        Returns:
            list: Lista de números flotantes
        Raises:
            ValueError: Si no hay datos o son inválidos
        """
        datos_str = self.entry_datos.get()
        if not datos_str:
            raise ValueError("No se ingresaron datos.")
        datos = list(map(float, datos_str.split(",")))
        if len(datos) < 2:
            raise ValueError("Se necesitan al menos 2 datos.")
        return datos

    def mostrar_resultado(self, texto):
        """Muestra texto en el área de resultados.
        Args:
            texto (str): Texto a mostrar
        """
        self.text_resultado.delete(1.0, tk.END)
        
        # Formatear el texto para mejor legibilidad
        lineas = texto.split('\n')
        for linea in lineas:
            # Si la línea contiene ":", la dividimos para mejor alineación
            if ':' in linea:
                partes = linea.split(':', 1)
                self.text_resultado.insert(tk.END, f"{partes[0]:<30}: {partes[1].strip()}\n")
            else:
                self.text_resultado.insert(tk.END, linea + '\n')
        
        # Mover al inicio
        self.text_resultado.see("1.0")

    def on_frame_configure(self, event=None):
        """Actualiza el área de scroll cuando el frame cambia de tamaño."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Ajusta el ancho del frame interno cuando el canvas cambia de tamaño."""
        # Obtener el nuevo ancho del canvas
        canvas_width = event.width
        # Actualizar el ancho del frame interno
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _on_mousewheel(self, event):
        """Maneja el evento de la rueda del mouse para el scroll."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def main(datos=None):
    """Función principal que inicia la aplicación.
    Args:
        datos (list, optional): Datos para cargar inicialmente. Defaults to None.
    """
    root = tk.Tk()
    app = PruebasAleatoriedadApp(root, datos)
    root.mainloop()

if __name__ == "__main__":
    # Si se ejecuta directamente, verifica si se pasaron datos como argumento
    datos = None
    if len(sys.argv) > 1:
        datos = sys.argv[1].split(",")
    main(datos)