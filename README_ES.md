GGUF Merge Tool v10.0
https://badge.fury.io/py/gguf-merge-tool.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg

Herramienta profesional con GUI + CLI para descargar, verificar y fusionar modelos GGUF fragmentados desde Hugging Face.

✨ Novedades en la Versión 10.0
Función	Descripción
Barras de progreso corregidas	El progreso se muestra de forma fluida y correcta durante la verificación de hashes y la fusión
Carga de archivos locales	Botón "Local" que permite seleccionar una carpeta con archivos GGUF en el disco y trabajar con ellos sin descargar
Historial de repositorios	Lista desplegable en el campo de entrada del repositorio — guarda las últimas 10 consultas
🚀 Características Principales
Descarga de archivos GGUF desde Hugging Face con soporte para reanudar (resume).

Verificación de integridad (SHA-256) de los archivos descargados.

Fusión de partes (splits) en un único archivo GGUF usando llama-gguf-split.

Agrupación de archivos por cuantización y nombre base.

Descarga multiproceso (detección automática del número de núcleos).

ETA real y velocidad (MB/s) durante la descarga.

Modo CLI para automatización.

Guardado del token y la ruta de llama.cpp entre sesiones.

📦 Instalación
Desde PyPI (recomendado)
bash
pip install gguf-merge-tool
Después de la instalación, dos comandos están disponibles:

gguf-merge-gui — inicia la interfaz gráfica

gguf-merge — inicia el modo CLI

Desde el código fuente
bash
git clone https://github.com/Andre17111978/gguf-merge-tool.git
cd gguf-merge-tool
pip install -r requirements.txt
python gguf_merge_tool.py
🖥️ Uso (GUI)
bash
gguf-merge-gui
# o
python gguf_merge_tool.py
Interfaz paso a paso:
Campo	Descripción
Repositorio	Ingrese el ID del repositorio en Hugging Face (ej. unsloth/Qwen3.5-122B-A10B-GGUF).
El historial guarda automáticamente las últimas 10 consultas.
Rama	Normalmente main.
Token	Opcional, para repositorios privados (formato: hf_xxxxxxxxxxxxxxxxxx).
Carpeta de descarga	Dónde guardar los archivos.
Ruta de llama.cpp	Especifique la carpeta que contiene llama-gguf-split (necesario para la fusión).
Archivos	Lista de archivos GGUF con casillas de verificación, agrupados automáticamente por cuantización.
Botones de control:
Botón	Función
Cargar	Obtener la lista de archivos del repositorio.
Local	Seleccionar una carpeta con archivos GGUF en el disco.
Seleccionar todo / Descargar todo	Operaciones masivas.
Descargar	Descargar los archivos seleccionados.
Verificar	Comprobar hashes SHA-256.
Fusionar	Combinar las partes seleccionadas.
⌨️ Uso (CLI)
Descargar archivos específicos
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f model-00001-of-00003.gguf model-00002-of-00003.gguf
Descargar todo el repositorio
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Descargar con token (repositorio privado)
bash
gguf-merge download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Fusionar partes
bash
gguf-merge merge -d ./models -o ./models/merged_model.gguf -f
Argumentos CLI
Comando download:

Argumento	Descripción
-d, --dir	Carpeta de guardado (obligatorio)
-r, --repo	ID del repositorio (obligatorio)
-b, --branch	Rama (predeterminado: main)
-t, --token	Token de Hugging Face
-f, --files	Lista de archivos para descargar
Comando merge:

Argumento	Descripción
-d, --dir	Carpeta con las partes (obligatorio)
-o, --output	Ruta del archivo de salida
-f, --force	Sobrescribir archivo existente
⚙️ Requisitos
Python >= 3.8

Dependencias (se instalan automáticamente):
huggingface_hub >= 0.20.0

tqdm >= 4.60.0

requests >= 2.28.0

gguf >= 0.1.0 (opcional, para leer metadatos)

Herramienta adicional necesaria:
llama-gguf-split (descargar desde llama.cpp releases)

🛠️ Solución de problemas
llama-gguf-split no encontrado
Descargar desde llama.cpp releases

Colocar en la carpeta tools/ o especificar la ruta en la configuración de la GUI

HTTP 401/403 (No autorizado/Prohibido)
Ingresar un token válido de Hugging Face

Asegurarse de que el token tenga acceso al repositorio

Espacio en disco insuficiente
Liberar espacio o cambiar la carpeta de descarga

Se puede modificar DISK_SPACE_MARGIN en el código (predeterminado: 1.1 = 10 % de margen)

La GUI no se inicia en Linux
bash
sudo apt-get install python3-tk  # Debian/Ubuntu
brew install python-tk           # macOS
📝 Licencia
Distribuido bajo la Licencia MIT. Consulte el archivo LICENSE para más detalles.

🙏 Agradecimientos
llama.cpp — por la utilidad de fusión

Hugging Face — por alojar los modelos

A la comunidad — por las pruebas e ideas

⭐ Apoyar el Proyecto
¡Si esta herramienta le resulta útil, dele una estrella en GitHub!

Hecho con ❤️ para la comunidad de IA

