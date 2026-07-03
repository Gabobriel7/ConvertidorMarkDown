import os
import tkinter as tk
from tkinter import filedialog
from markitdown import MarkItDown

CARPETA_DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados_markdown")

EXTENSIONES_SOPORTADAS = (
    ".pdf",
    ".docx", ".doc",
    ".pptx", ".ppt",
    ".xlsx", ".xls", ".csv",
    ".html", ".htm",
    ".xml", ".json",
    ".txt",
    ".jpg", ".jpeg", ".png",
    ".epub",
)


class AplicacionConversor:
    """
    Ventana de escritorio (Tkinter) para convertir documentos a Markdown.

    Agrupa en un solo lugar los datos de la app (la lista de archivos que el
    usuario eligió) y las acciones que disparan los botones (seleccionar,
    convertir y abrir la carpeta de resultados). Reutiliza la librería
    MarkItDown para hacer la conversión real.
    """

    def __init__(self, ventana):
        self.ventana = ventana
        self.archivos_elegidos = []
        self.carpeta_destino = CARPETA_DESTINO
        self.md = MarkItDown()

        ventana.title("Convertidor de Documentos a Markdown")
        ventana.geometry("560x600")
        ventana.minsize(480, 540)

        tk.Label(ventana, text="Convertidor a Markdown", font=("Segoe UI", 16, "bold")).pack(pady=(16, 4))
        tk.Label(ventana, text="Selecciona documentos y conviértelos a .md").pack(pady=(0, 12))

        tk.Button(ventana, text="Seleccionar archivos", command=self.seleccionar_archivos).pack()

        tk.Label(ventana, text="Archivos seleccionados:").pack(anchor="w", padx=16, pady=(12, 2))
        self.lista_archivos = tk.Listbox(ventana, height=6)
        self.lista_archivos.pack(fill="x", padx=16)

        tk.Button(ventana, text="Elegir carpeta de salida", command=self.elegir_carpeta_salida).pack(pady=(12, 2))
        self.etiqueta_salida = tk.Label(ventana, text=f"Guardando en: {self.carpeta_destino}", fg="gray", wraplength=520)
        self.etiqueta_salida.pack(padx=16)

        tk.Button(ventana, text="Convertir a Markdown", command=self.convertir).pack(pady=12)

        tk.Label(ventana, text="Registro:").pack(anchor="w", padx=16)
        self.registro = tk.Text(ventana, height=8, state="disabled", wrap="word")
        self.registro.pack(fill="both", expand=True, padx=16, pady=(2, 8))

        tk.Button(ventana, text="Abrir carpeta de resultados", command=self.abrir_carpeta_resultados).pack(pady=(0, 16))

    def escribir_en_registro(self, mensaje):
        """
        Inputs: mensaje (texto) a mostrar en el área de registro.
        Return: None.
        Qué hace: agrega una línea al área de registro y baja el scroll para que
                  siempre se vea lo último. El widget está bloqueado para el
                  usuario, así que se habilita solo mientras se escribe.
        """
        self.registro.configure(state="normal")
        self.registro.insert("end", mensaje + "\n")
        self.registro.see("end")
        self.registro.configure(state="disabled")
        self.ventana.update_idletasks()

    def seleccionar_archivos(self):
        """
        Inputs: ninguno; abre el explorador de archivos de Windows.
        Return: None.
        Qué hace: pide al usuario uno o más archivos, guarda la selección y la
                  muestra en la lista. Solo ofrece los formatos soportados.
        """
        patrones = " ".join(f"*{ext}" for ext in EXTENSIONES_SOPORTADAS)
        elegidos = filedialog.askopenfilenames(
            title="Elige los documentos a convertir",
            filetypes=[("Documentos soportados", patrones), ("Todos los archivos", "*.*")],
        )

        if not elegidos:
            return

        self.archivos_elegidos = list(elegidos)
        self.lista_archivos.delete(0, "end")
        for ruta in self.archivos_elegidos:
            self.lista_archivos.insert("end", os.path.basename(ruta))

        self.escribir_en_registro(f"Seleccionados {len(self.archivos_elegidos)} archivo(s).")

    def elegir_carpeta_salida(self):
        """
        Inputs: ninguno; abre el selector de carpetas de Windows.
        Return: None.
        Qué hace: pide al usuario una carpeta donde guardar los .md. Si elige
                  una, la guarda como carpeta de destino y actualiza la etiqueta;
                  si cancela, se mantiene la carpeta anterior.
        """
        elegida = filedialog.askdirectory(title="Elige dónde guardar los archivos .md")

        if not elegida:
            return

        self.carpeta_destino = elegida
        self.etiqueta_salida.configure(text=f"Guardando en: {self.carpeta_destino}")
        self.escribir_en_registro(f"Carpeta de salida: {self.carpeta_destino}")

    def convertir(self):
        """
        Inputs: ninguno; usa la lista de archivos ya elegidos.
        Return: None.
        Qué hace: convierte cada archivo elegido a Markdown y lo guarda en la
                  carpeta de resultados. Si un archivo falla, atrapa el error y
                  sigue con los demás. Informa el avance y un resumen final.
        """
        if not self.archivos_elegidos:
            self.escribir_en_registro("Primero selecciona al menos un archivo.")
            return

        os.makedirs(self.carpeta_destino, exist_ok=True)
        exitosos = 0
        fallidos = 0

        for ruta in self.archivos_elegidos:
            nombre_base = os.path.splitext(os.path.basename(ruta))[0]
            ruta_destino = os.path.join(self.carpeta_destino, f"{nombre_base}.md")
            self.escribir_en_registro(f"Procesando: {os.path.basename(ruta)}...")

            try:
                resultado = self.md.convert(ruta)
                with open(ruta_destino, "w", encoding="utf-8") as archivo_salida:
                    archivo_salida.write(resultado.text_content)
                self.escribir_en_registro(f"   Convertido: {nombre_base}.md")
                exitosos += 1
            except Exception as e:
                self.escribir_en_registro(f"   Error: {e}")
                fallidos += 1

        self.escribir_en_registro(f"Listo. Exitosos: {exitosos} | Fallidos: {fallidos}")

    def abrir_carpeta_resultados(self):
        """
        Inputs: ninguno.
        Return: None.
        Qué hace: abre la carpeta de resultados en el explorador de Windows. Si
                  todavía no existe, la crea antes para no fallar.
        """
        os.makedirs(self.carpeta_destino, exist_ok=True)
        os.startfile(self.carpeta_destino)


if __name__ == "__main__":
    ventana = tk.Tk()
    AplicacionConversor(ventana)
    ventana.mainloop()
