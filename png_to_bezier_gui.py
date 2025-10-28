import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import cv2
import numpy as np
from svgpathtools import svg2paths, wsvg, Path, CubicBezier
import math
from utils.convertir_png_a_svg_lineal import convertir_png_a_svg_lineal
from utils.convert_svg_to_bezier import convert_svg
import tkfontawesome as tfa
class PNGToBezierGUI:
    """
    Esta clase crea un diálogo gráfico para convertir imágenes PNG en curvas de Bézier a través de SVG.
    
    Realiza dos pasos principales:
    1. Convierte el PNG seleccionado en un SVG lineal utilizando la función convertir_png_a_svg_lineal.
    2. Convierte el SVG lineal en curvas de Bézier utilizando la función convert_svg.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("KaraokeCapibaraPython PNG to Bezier Converter")
        width = 500
        height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg='#e8f5e8')  # Light green background

        # Icons using tkfontawesome
        self.icon_png = tfa.icon_to_image("file-image", fill="white", scale_to_width=20)
        self.icon_folder = tfa.icon_to_image("folder", fill="white", scale_to_width=20)
        self.icon_process = tfa.icon_to_image("play", fill="white", scale_to_width=20)

        # Main frame
        self.frame = tk.Frame(root, bg='#e8f5e8', padx=30, pady=30)
        self.frame.pack(expand=True, fill='both')

        self.info_label = tk.Label(self.frame, text="Esta aplicación convierte imágenes PNG en curvas de Bézier a través de SVG.\n\nRealiza dos pasos:\n1. Convierte el PNG seleccionado en un SVG lineal.\n2. Convierte el SVG lineal en curvas de Bézier.\n\nLas curvas de Bézier son curvas matemáticas definidas por puntos de control que permiten crear formas suaves y escalables, ideales para gráficos vectoriales.", justify=tk.LEFT, wraplength=380, bg='#e8f5e8', font=('Arial', 10))
        self.info_label.pack(pady=10)

        self.png_path = None

        # Botón para seleccionar PNG
        self.select_png_button = tk.Button(self.frame, text="Seleccionar PNG", command=self.select_png, bg='#2196F3', fg='white', font=('Arial', 12, 'bold'), height=3, relief='raised', bd=2, image=self.icon_png, compound="left", padx=20, pady=20)
        self.select_png_button.pack(pady=10, fill='x')

        # Label para mostrar el PNG seleccionado
        self.png_label = tk.Label(self.frame, text="Ningún PNG seleccionado", bg='#e8f5e8', font=('Arial', 10))
        self.png_label.pack()

        # Botón para procesar
        self.process_button = tk.Button(self.frame, text="Procesar", command=self.process, state=tk.DISABLED, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), height=3, relief='raised', bd=2, image=self.icon_process, compound="left", padx=20, pady=20)
        self.process_button.pack(pady=10, fill='x')

    def select_png(self):
        self.png_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if self.png_path:
            self.png_label.config(text=f"Seleccionado: {os.path.basename(self.png_path)}")
            self.check_enable_process()

    def check_enable_process(self):
        if self.png_path:
            self.process_button.config(state=tk.NORMAL)
        else:
            self.process_button.config(state=tk.DISABLED)

    def process(self):
        try:
            # Paso 1: Convertir PNG a SVG lineal
            temp_svg = "temp_lineal.svg"
            convertir_png_a_svg_lineal(self.png_path, temp_svg)

            # Paso 2: Convertir SVG lineal a Bezier
            os.makedirs("res/svg", exist_ok=True)
            final_svg = "res/svg/salida_bezier.svg"
            convert_svg(temp_svg, final_svg)

            # Limpiar temp
            if os.path.exists(temp_svg):
                os.remove(temp_svg)

            messagebox.showinfo("Éxito", f"Conversión completada. Archivo guardado en {final_svg}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PNGToBezierGUI(root)
    root.mainloop()