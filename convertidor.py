import os
from markitdown import MarkItDown

"""
CONVERTIDOR DE DOCUMENTOS A MARKDOWN
------------------------------------

¿Qué hace?
    Busca todos los documentos soportados dentro de la carpeta de entrada,
    los convierte a Markdown (.md) usando la librería MarkItDown de Microsoft,
    y guarda el resultado en la carpeta de salida.

    Ideal para preparar documentos antes de enviárselos a una IA (LLM) como
    Claude: el Markdown es compacto y fácil de entender para los modelos,
    lo que ayuda a gastar menos tokens.

Entradas:
    - Carpeta 'documentos' con uno o más archivos soportados
      (PDF, Word, Excel, PowerPoint, HTML, CSV, imágenes, etc.).

Salidas:
    - Carpeta 'resultados_markdown' con un archivo .md por cada documento.
    - No devuelve nada: trabaja escribiendo archivos en el disco.
"""

# Carpetas de trabajo (cámbialas aquí si quieres otros nombres)
CARPETA_ORIGEN = "documentos"
CARPETA_DESTINO = "resultados_markdown"

# Formatos que MarkItDown puede convertir. Añade o quita según necesites.
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


def transformar_documentos():
    md = MarkItDown()

    # Crea la carpeta de salida si no existe
    os.makedirs(CARPETA_DESTINO, exist_ok=True)

    # Verifica que exista la carpeta de entrada
    if not os.path.exists(CARPETA_ORIGEN):
        print(f"Error: la carpeta '{CARPETA_ORIGEN}' no existe en este directorio.")
        print(f"Créala y coloca dentro tus documentos para convertir.")
        return

    # Filtra solo los archivos con extensión soportada
    archivos = os.listdir(CARPETA_ORIGEN)
    documentos = [f for f in archivos if f.lower().endswith(EXTENSIONES_SOPORTADAS)]

    if not documentos:
        print(f"No se encontraron documentos soportados dentro de '{CARPETA_ORIGEN}'.")
        print(f"Formatos aceptados: {', '.join(EXTENSIONES_SOPORTADAS)}")
        return

    print(f"Se encontraron {len(documentos)} documento(s) para convertir.\n")

    # Contadores para el resumen final
    exitosos = 0
    fallidos = 0

    for nombre_archivo in documentos:
        ruta_origen = os.path.join(CARPETA_ORIGEN, nombre_archivo)
        nombre_base = os.path.splitext(nombre_archivo)[0]
        ruta_destino = os.path.join(CARPETA_DESTINO, f"{nombre_base}.md")

        # Avisa si el resultado ya existía (lo va a sobrescribir)
        if os.path.exists(ruta_destino):
            print(f"Aviso: '{nombre_base}.md' ya existía y se reemplazará.")

        print(f"Procesando: {nombre_archivo}...")

        try:
            resultado = md.convert(ruta_origen)

            with open(ruta_destino, "w", encoding="utf-8") as archivo_salida:
                archivo_salida.write(resultado.text_content)

            print(f"  -> Convertido con éxito: {nombre_base}.md\n")
            exitosos += 1

        except Exception as e:
            print(f"  -> Error al convertir {nombre_archivo}: {e}\n")
            fallidos += 1

    # Resumen final
    print("=" * 40)
    print("¡Proceso de conversión finalizado!")
    print(f"  Exitosos: {exitosos}")
    print(f"  Fallidos: {fallidos}")
    print(f"  Resultados en la carpeta: '{CARPETA_DESTINO}'")


if __name__ == "__main__":
    transformar_documentos()
