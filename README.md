# Convertidor de Documentos a Markdown

Convierte múltiples documentos (PDF, Word, Excel, PowerPoint, HTML y más) a formato
Markdown (`.md`) de forma local y automática.

Está pensado para preparar documentos antes de enviárselos a una IA (LLM) como Claude:
el Markdown es compacto y fácil de entender para los modelos, lo que ayuda a gastar menos
tokens y a respetar los límites de archivos.

## Características

- Convierte muchos formatos, no solo PDF (usa la librería
  [MarkItDown](https://github.com/microsoft/markitdown) de Microsoft).
- Procesa todos los archivos de una carpeta de una sola vez.
- Muestra el avance en tiempo real y un resumen final.
- Avisa antes de sobrescribir resultados anteriores.

### Formatos soportados
PDF, Word (`.docx`, `.doc`), PowerPoint (`.pptx`, `.ppt`), Excel (`.xlsx`, `.xls`, `.csv`),
HTML, XML, JSON, TXT, imágenes (`.jpg`, `.png`) y EPUB.

## Requisitos

- Python 3.10 o superior.
- Un editor de código (opcional, como VS Code).

## Instalación

1. Clona o descarga este repositorio.
2. (Recomendado) Crea un entorno virtual:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # En Windows
   # source venv/bin/activate   # En macOS / Linux
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Cómo usar

1. Coloca tus documentos dentro de la carpeta `documentos/`.
2. Ejecuta el script:

   ```bash
   python convertidor.py
   ```

3. Los archivos `.md` aparecerán en la carpeta `resultados_markdown/`, listos para copiar
   a tu IA de preferencia.

## Estructura del proyecto

```
convertidor-markdown/
├── documentos/            <-- Coloca aquí tus archivos a convertir
├── resultados_markdown/   <-- Aquí aparecen los .md convertidos
├── convertidor.py         <-- El script principal
├── requirements.txt       <-- Dependencias del proyecto
├── .gitignore             <-- Archivos que Git debe ignorar
└── README.md              <-- Este archivo
```

## Licencia

Proyecto de uso libre con fines educativos y personales.
