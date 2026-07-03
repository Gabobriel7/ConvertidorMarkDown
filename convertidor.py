import os
from markitdown import MarkItDown

CARPETA_ORIGEN = "documentos"
CARPETA_DESTINO = "resultados_markdown"

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
    """
    Inputs:
        Ninguno por parámetro. Usa la carpeta CARPETA_ORIGEN ('documentos') del
        directorio actual, que debe contener uno o más archivos soportados
        (ver EXTENSIONES_SOPORTADAS: PDF, Word, Excel, PowerPoint, HTML, etc.).

    Return:
        None. El resultado son efectos en el disco: crea la carpeta
        CARPETA_DESTINO ('resultados_markdown') si no existe y escribe dentro
        un archivo .md por cada documento convertido.

    Qué hace:
        Busca los documentos soportados en la carpeta de entrada, los convierte a
        Markdown con la librería MarkItDown de Microsoft y guarda cada resultado.
        Si un archivo falla, atrapa el error y continúa con los demás. Muestra el
        avance en pantalla y un resumen final con exitosos y fallidos.
    """
    md = MarkItDown()

    os.makedirs(CARPETA_DESTINO, exist_ok=True)

    if not os.path.exists(CARPETA_ORIGEN):
        print(f"Error: la carpeta '{CARPETA_ORIGEN}' no existe en este directorio.")
        print("Créala y coloca dentro tus documentos para convertir.")
        return

    archivos = os.listdir(CARPETA_ORIGEN)
    documentos = [f for f in archivos if f.lower().endswith(EXTENSIONES_SOPORTADAS)]

    if not documentos:
        print(f"No se encontraron documentos soportados dentro de '{CARPETA_ORIGEN}'.")
        print(f"Formatos aceptados: {', '.join(EXTENSIONES_SOPORTADAS)}")
        return

    print(f"Se encontraron {len(documentos)} documento(s) para convertir.\n")

    exitosos = 0
    fallidos = 0

    for nombre_archivo in documentos:
        ruta_origen = os.path.join(CARPETA_ORIGEN, nombre_archivo)
        nombre_base = os.path.splitext(nombre_archivo)[0]
        ruta_destino = os.path.join(CARPETA_DESTINO, f"{nombre_base}.md")

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

    print("=" * 40)
    print("¡Proceso de conversión finalizado!")
    print(f"  Exitosos: {exitosos}")
    print(f"  Fallidos: {fallidos}")
    print(f"  Resultados en la carpeta: '{CARPETA_DESTINO}'")


if __name__ == "__main__":
    transformar_documentos()
