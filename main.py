import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import tkfontawesome as tfa

def run_karaoke():
    root.destroy()
    import pygame
    from src.game import Game
    pygame.init()
    game = Game()
    game.run()

def run_color_picker():
    root.withdraw()
    subprocess.run([sys.executable, 'utils/color_picker.py'])
    root.deiconify()

def run_point_picker():
    root.withdraw()
    subprocess.run([sys.executable, 'utils/point_picker.py'])
    root.deiconify()

def run_png_to_bezier():
    root.withdraw()
    subprocess.run([sys.executable, 'png_to_bezier_gui.py'])
    root.deiconify()

def run_recreate_pngs():
    messagebox.showinfo("Advertencia", 'Copia el archivo salida_bezier.svg generado por la herramienta "PNG TO BEZIER" a la carpeta res/svg/salida_bezier.svg antes de iniciar')
    root.withdraw()
    subprocess.run([sys.executable, 'recreate_pngs.py'])
    root.deiconify()

root = tk.Tk()
root.title("Menú Principal - KaraokeCapibaraPython")
width = 600
height = 500
root.resizable(False, False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")
root.configure(bg='#e8f5e8')  # Light green background

# Icons using tkfontawesome
icon_karaoke = tfa.icon_to_image("music", fill="white", scale_to_width=20)
icon_color = tfa.icon_to_image("palette", fill="white", scale_to_width=20)
icon_point = tfa.icon_to_image("crosshairs", fill="black", scale_to_width=20)
icon_convert = tfa.icon_to_image("file-image", fill="white", scale_to_width=20)
icon_recreate = tfa.icon_to_image("video", fill="white", scale_to_width=20)

# Main frame
frame = tk.Frame(root, bg='#e8f5e8', padx=30, pady=30)
frame.pack(expand=True, fill='both')

tk.Label(frame, text="Selecciona una opción:", font=('Arial', 16, 'bold'), bg='#e8f5e8').pack(pady=10)

# Buttons with icons
buttons = [
    ("Reproducir karaoke capibara", run_karaoke, '#4CAF50', 'white', icon_karaoke),
    ("1 - Convertir dibujo PNG a SVG Beizer", run_png_to_bezier, '#9C27B0', 'white', icon_convert),
    ("2 - Color Picker", run_color_picker, '#2196F3', 'white', icon_color),
    ("3 - Point Picker", run_point_picker, '#FF9800', 'black', icon_point),
    ("4 - SVG a Frames PNG", run_recreate_pngs, '#FF5722', 'white', icon_recreate)
]

for text, command, bg_color, fg_color, icon in buttons:
    btn = tk.Button(frame, text=text, command=command, bg=bg_color, fg=fg_color, font=('Arial', 14, 'bold'), height=3, relief='raised', bd=2, image=icon, compound="left", padx=20, pady=20)
    btn.image = icon  # Keep reference
    btn.pack(pady=10, fill='x', padx=20)

root.mainloop()