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

class PNGToBezierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG to Bezier Converter")
        self.root.geometry("400x200")

        self.png_path = None
        self.output_folder = None

        # Botón para seleccionar PNG
        self.select_png_button = tk.Button(root, text="Seleccionar PNG", command=self.select_png)
        self.select_png_button.pack(pady=10)

        # Label para mostrar el PNG seleccionado
        self.png_label = tk.Label(root, text="Ningún PNG seleccionado")
        self.png_label.pack()

        # Botón para seleccionar carpeta de salida
        self.select_folder_button = tk.Button(root, text="Seleccionar Carpeta de Salida", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        # Label para mostrar la carpeta seleccionada
        self.folder_label = tk.Label(root, text="Ninguna carpeta seleccionada")
        self.folder_label.pack()

        # Botón para procesar
        self.process_button = tk.Button(root, text="Procesar", command=self.process, state=tk.DISABLED)
        self.process_button.pack(pady=10)

    def select_png(self):
        self.png_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if self.png_path:
            self.png_label.config(text=f"Seleccionado: {os.path.basename(self.png_path)}")
            self.check_enable_process()

    def select_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.folder_label.config(text=f"Carpeta: {self.output_folder}")
            self.check_enable_process()

    def check_enable_process(self):
        if self.png_path and self.output_folder:
            self.process_button.config(state=tk.NORMAL)
        else:
            self.process_button.config(state=tk.DISABLED)

    def process(self):
        try:
            # Paso 1: Convertir PNG a SVG lineal
            temp_svg = "temp_dibujo_bezier.svg"
            convertir_png_a_svg_lineal(self.png_path, temp_svg)

            # Paso 2: Convertir SVG lineal a Bezier
            final_svg = os.path.join(self.output_folder, "salida_bezier.svg")
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