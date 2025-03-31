import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import subprocess
from PyPDF2 import PdfReader, PdfWriter

def abrir_carpeta_salida():
    path = carpeta_salida.get()
    if os.path.exists(path):
        subprocess.Popen(f'explorer "{path}"')

def aplicar_restricciones(carpeta_entrada, carpeta_salida, log_widget, barra_progreso):
    if not carpeta_entrada or not carpeta_salida:
        messagebox.showwarning("Faltan carpetas", "Selecciona ambas carpetas.")
        return

    os.makedirs(carpeta_salida, exist_ok=True)

    archivos = [f for f in os.listdir(carpeta_entrada) if f.endswith(".pdf")]
    total = len(archivos)

    if total == 0:
        messagebox.showinfo("Sin archivos", "No se encontraron archivos PDF.")
        return

    log_widget.insert(tk.END, f"🔐 Iniciando protección de {total} archivos...\n")
    log_widget.see(tk.END)

    barra_progreso["maximum"] = total
    barra_progreso["value"] = 0

    for idx, archivo in enumerate(archivos, 1):
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        ruta_salida = os.path.join(carpeta_salida, archivo)

        try:
            reader = PdfReader(ruta_entrada)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(
                user_password="",
                owner_password="zeta",
                permissions_flag=0
            )

            with open(ruta_salida, "wb") as f:
                writer.write(f)

            log_widget.insert(tk.END, f"✅ Protegido: {archivo}\n")
        except Exception as e:
            log_widget.insert(tk.END, f"❌ Error: {archivo} ({e})\n")

        barra_progreso["value"] = idx
        log_widget.see(tk.END)
        root.update_idletasks()

    log_widget.insert(tk.END, "\n🎉 Finalizado.\n")
    messagebox.showinfo("Completado", f"Se protegieron {total} archivos correctamente.")

# 🖼️ Interfaz
root = tk.Tk()
root.title("Banco Nacional de Bolivia S.A. - Organización y Métodos")
root.geometry("750x570")
root.resizable(False, False)

carpeta_entrada = tk.StringVar()
carpeta_salida = tk.StringVar()

def seleccionar_entrada():
    path = filedialog.askdirectory()
    if path:
        carpeta_entrada.set(path)

def seleccionar_salida():
    path = filedialog.askdirectory()
    if path:
        carpeta_salida.set(path)

# 🧭 Sección de entrada/salida
tk.Label(root, text="📥 Carpeta de entrada:").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=carpeta_entrada, width=90).pack(padx=10)
tk.Button(root, text="Seleccionar carpeta", command=seleccionar_entrada).pack(pady=5)

tk.Label(root, text="📤 Carpeta de salida:").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=carpeta_salida, width=90).pack(padx=10)
tk.Button(root, text="Seleccionar carpeta", command=seleccionar_salida).pack(pady=5)

# 🔘 Botón de ejecución
tk.Button(root, text="🔐 Aplicar restricciones", bg="#007ACC", fg="white", font=("Arial", 11, "bold"),
          command=lambda: aplicar_restricciones(carpeta_entrada.get(), carpeta_salida.get(), log_area, barra_progreso)).pack(pady=10)

# 📊 Barra de progreso
barra_progreso = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
barra_progreso.pack(pady=5)

# 📜 Área de log
log_area = scrolledtext.ScrolledText(root, width=90, height=15)
log_area.pack(padx=10, pady=10)

# 📂 Botón para abrir carpeta de salida
tk.Button(root, text="📂 Abrir carpeta de salida", command=abrir_carpeta_salida).pack(pady=5)

# 👤 Derechos de autor
tk.Label(root, text="© Eduardo Sergio Santivañez Dávalos", font=("Arial", 9, "italic"), fg="gray").pack(pady=10)

root.mainloop()

