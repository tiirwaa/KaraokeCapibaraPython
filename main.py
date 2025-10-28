import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import tkfontawesome as tfa
import threading
import tkinter.ttk as ttk
import os

# Global variables for subprocess result
result = None
done = False

def show_message(title, message, is_error=False):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("700x500")
    dialog.resizable(True, True)
    if is_error:
        dialog.configure(bg='#ffebee')  # Light red for error
    else:
        dialog.configure(bg='#e8f5e8')  # Light green for success
    
    text = tk.Text(dialog, wrap=tk.WORD, bg=dialog.cget('bg'))
    scrollbar = tk.Scrollbar(dialog, command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text.insert(tk.END, message)
    text.config(state=tk.DISABLED)
    
    btn = tk.Button(dialog, text="Cerrar", command=dialog.destroy)
    btn.pack(pady=10)
    
    # Center the dialog
    dialog.update_idletasks()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (dialog_width // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog_height // 2)
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

def run_subprocess():
    global result, done
    result = subprocess.run([sys.executable, 'recreate_pngs.py'], capture_output=True, text=True)
    done = True

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
    proceed = messagebox.askyesno("Confirmación", 'Asegúrate de que los pasos 1 al 3 estén completados antes de proceder.\n\n¿Deseas continuar?')
    if not proceed:
        return
    # Disable buttons
    for btn in button_widgets:
        btn.config(state='disabled')
    # Show and start progress
    progress.pack(pady=10, fill='x', padx=20)
    progress.start()
    # Reset flags
    global result, done
    result = None
    done = False
    # Start thread
    thread = threading.Thread(target=run_subprocess)
    thread.start()
    # Check periodically
    check_done()

def check_done():
    if done:
        # Stop and hide progress
        progress.stop()
        progress.pack_forget()
        # Enable buttons
        for btn in button_widgets:
            btn.config(state='normal')
        # Show message
        if result.returncode == 0:
            show_message("Éxito", "Proceso completado exitosamente.\n\n" + result.stdout.strip())
            # Open the folder in explorer
            folder_path = os.path.abspath("media\\images\\animar_svg_manim")
            subprocess.run(["explorer.exe", folder_path])
        else:
            show_message("Error", "Ocurrió un error durante el proceso.\n\n" + result.stderr.strip(), is_error=True)
    else:
        root.after(100, check_done)  # Check again in 100ms

root = tk.Tk()
root.title("Menú Principal - KaraokeCapibaraPython")
width = 600
height = 550
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

button_widgets = []
for text, command, bg_color, fg_color, icon in buttons:
    btn = tk.Button(frame, text=text, command=command, bg=bg_color, fg=fg_color, font=('Arial', 14, 'bold'), height=3, relief='raised', bd=2, image=icon, compound="left", padx=20, pady=20)
    btn.image = icon  # Keep reference
    btn.pack(pady=10, fill='x', padx=20)
    button_widgets.append(btn)

# Progress bar
progress = ttk.Progressbar(frame, mode='indeterminate')
# Not packed initially

root.mainloop()