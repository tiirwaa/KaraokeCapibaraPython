import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def run_karaoke():
    root.destroy()
    import pygame
    from src.game import Game
    pygame.init()
    game = Game()
    game.run()

def run_color_picker():
    subprocess.run([sys.executable, 'utils/color_picker.py'])

def run_point_picker():
    subprocess.run([sys.executable, 'utils/point_picker.py'])

def run_png_to_bezier():
    subprocess.run([sys.executable, 'png_to_bezier_gui.py'])

root = tk.Tk()
root.title("Menú Principal - Capibara")
root.geometry("400x300")

tk.Label(root, text="Selecciona una opción:").pack(pady=10)

tk.Button(root, text="Reproducir karaoke capibara", command=run_karaoke).pack(pady=5)
tk.Button(root, text="Color Picker", command=run_color_picker).pack(pady=5)
tk.Button(root, text="Point Picker", command=run_point_picker).pack(pady=5)
tk.Button(root, text="Convertir dibujo PNG a SVG Beizer", command=run_png_to_bezier).pack(pady=5)

root.mainloop()