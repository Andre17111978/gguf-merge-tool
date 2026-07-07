GGUF Merge Tool v9.2

Herramienta profesional GUI + CLI para descargar, verificar y fusionar modelos GGUF fragmentados de Hugging Face.
Tabla de Contenidos

    Características

    Inicio Rápido

    Instalación

    Uso de CLI

    Uso de GUI

    Configuración

    Requisitos

    Solución de Problemas

    Consejos de Rendimiento

    Detalles Técnicos

    Licencia

    Agradecimientos

    Soporte

Características

GUI Moderna - Interfaz basada en Tkinter con lista de archivos desplazable y soporte para rueda del mouse

Agrupación Inteligente - Archivos agrupados automáticamente por tipo de cuantización (Q4_K_M, Q5_K_S, etc.)

Descarga Reanudable - Solicitudes HTTP Range con protección inteligente contra fallos (manejo 200 vs 206)

Descarga Paralela - Hilos configurables (detección automática de núcleos de CPU)

Verificación de Hash - Verificación SHA256 usando metadatos HF LFS

Fusión Inteligente - Usa llama-gguf-split de llama.cpp

Soporte CLI - Subcomandos download y merge para automatización

Detección Inteligente - Encuentra automáticamente llama-gguf-split en ubicaciones comunes

Persistencia de Ruta - Guarda la ruta de llama.cpp entre sesiones

Lógica de Reintentos - Reintentos automáticos con retroceso exponencial (3 intentos)

ETA en Tiempo Real - Muestra velocidad (MB/s) y tiempo restante estimado

Multilenguaje - Documentación en 6 idiomas
Inicio Rápido
Windows

Instalar dependencias:
pip install huggingface_hub tqdm requests

Descargar llama-gguf-split desde: https://github.com/ggerganov/llama.cpp/releases

Ejecutar la herramienta:
python gguf_merge_tool.py
Linux / macOS

Instalar dependencias:
pip install huggingface_hub tqdm requests

Ejecutar la herramienta:
python3 gguf_merge_tool.py
Instalación
Desde el código fuente (Recomendado)

Clonar el repositorio:
git clone https://github.com/yourusername/gguf-merge-tool.git
cd gguf-merge-tool

Instalar dependencias:
pip install -r requirements.txt

Ejecutar la herramienta:
python src/gguf_merge_tool.py
Desde PyPI (Próximamente)

pip install gguf-merge-tool
gguf-merge-gui
Usuarios de Windows: Binario Requerido

Descargar llama-gguf-split.exe desde las versiones de llama.cpp
Colocar en una de estas ubicaciones:

    tools/llama-gguf-split.exe

    bin/llama-gguf-split.exe

    O especificar la ruta en la configuración de GUI

Uso de CLI
Descargar Archivos Específicos

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f Qwen3.5-122B-A10B-Q4_K_M-00001-of-00008.gguf Qwen3.5-122B-A10B-Q4_K_M-00002-of-00008.gguf
Descargar Repositorio Completo

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Descargar con Autenticación (Repositorio Privado)

python src/gguf_merge_tool.py download -r tu-usuario/tu-modelo-privado -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Fusionar Partes

python src/gguf_merge_tool.py merge -d ./models -o ./models/merged_model.gguf -f
Referencia de Argumentos CLI

Comando: download
-d, --dir - Directorio para guardar archivos - Requerido: Sí
-r, --repo - ID del repositorio de Hugging Face - Requerido: Sí
-b, --branch - Rama del repositorio (por defecto: main) - Requerido: No
-t, --token - Token de acceso HF - Requerido: No
-f, --files - Lista de archivos para descargar - Requerido: No

Comando: merge
-d, --dir - Directorio con las partes - Requerido: Sí
-o, --output - Ruta del archivo de salida - Requerido: No
-f, --force - Sobrescribir archivo existente - Requerido: No
Uso de GUI
Paso 1: Cargar Repositorio

Ingresar ID del repositorio de Hugging Face (ej: unsloth/Qwen3.5-122B-A10B-GGUF)
Ingresar rama (por defecto: main)
Ingresar token de HF (requerido para repositorios privados)
Hacer clic en el botón "Cargar"
Paso 2: Seleccionar Archivos

Los archivos se agrupan automáticamente por tipo de cuantización
Hacer clic en "Seleccionar todo" para seleccionar todos los archivos
O seleccionar archivos individuales con casillas de verificación
Paso 3: Descargar

Hacer clic en "Descargar" o "Descargar todo"
Monitorear el progreso en tiempo real:

    Barra de progreso muestra porcentaje

    Barra de estado muestra: [1/4] archivo.gguf: 45% | 4.5 MB/s | ETA: 2h 15m

Paso 4: Verificar (Opcional pero Recomendado)

Hacer clic en el botón "Verificar"
La herramienta valida los hashes SHA256 contra los metadatos de HF
Muestra mensaje de éxito si todos los hashes coinciden
Paso 5: Fusionar (Opcional)

Seleccionar al menos 2 partes (casillas de verificación)
Hacer clic en el botón "Fusionar"
La herramienta ejecuta llama-gguf-split --merge
El archivo de salida se guarda con el nombre base correcto
Configuración
Ruta de llama.cpp

En GUI, localizar "Ruta a llama.cpp":
Hacer clic en "Buscar" para detección automáticaO hacer clic en "Examinar" para seleccionar manualmente
La ruta se guarda en llama_path.txt para persistencia
Configuración de Hilos

Ajustar la constante JOBS en el código (por defecto: min(4, os.cpu_count() or 2)):
En gguf_merge_tool.py
JOBS = min(4, os.cpu_count() or 2) - Cambiar este valor
Margen de Espacio en Disco

Cambiar DISK_SPACE_MARGIN (por defecto: 1.1 = 10% extra):
DISK_SPACE_MARGIN = 1.1
Tamaño de Bloque de Descarga

Cambiar CHUNK_SIZE (por defecto: 1 MB):
CHUNK_SIZE = 1024 * 1024
Requisitos

Python >= 3.8
huggingface_hub >= 0.20.0
tqdm >= 4.60.0
requests >= 2.28.0
gguf >= 0.1.0 (opcional, para lectura de metadatos)
llama-gguf-split (de llama.cpp)
Verificar Instalación

python -c "import huggingface_hub, tqdm, requests; print('Todas las dependencias instaladas')"
Solución de Problemas
llama-gguf-split no encontrado

Descargar desde las versiones de llama.cpp
Colocar en la carpeta tools/ o especificar ruta en GUI
HTTP 401 Unauthorized o HTTP 403 Forbidden

Ingresar su token de Hugging Face
Asegurarse de que el token tenga acceso de lectura al repositorio
Formato del token: hf_xxxxxxxxxxxxxxxxxx
Espacio insuficiente en disco

Liberar espacio en disco (se necesita 10% extra para fusionar)
Cambiar el directorio de descarga a otra unidad
Usar DISK_SPACE_MARGIN para ajustar el margen
Descarga atascada en 0%

Verificar la conexión a internet
Verificar que el token sea correcto
Verificar si el repositorio es privado
Verificar si el repositorio existe
Archivo corrupto después de reanudar

La herramienta tiene protección integrada contra fallos de Range
Si el servidor no soporta Range (devuelve 200 en lugar de 206), comienza la descarga desde cero
Esto es intencional para prevenir la corrupción de archivos
GUI no se inicia

Verificar que Tkinter esté instalado (generalmente incluido con Python)
En Linux: sudo apt-get install python3-tk
En macOS: brew install python-tk
Consejos de Rendimiento

Muchos archivos pequeños - Mantener hilos por defecto (4)
Pocos archivos grandes - Aumentar hilos a 8
Red lenta - Reducir hilos a 2
NVMe SSD rápido - Mantener por defecto o aumentar
Interrupciones de red - La herramienta maneja la reanudación automáticamente
Detalles Técnicos
Flujo de Descarga

Obtener lista de archivos del repositorio HF con tamaños y hashes
Usuario selecciona archivos para descargar
Verificar espacio en disco - abortar si es insuficiente
Descarga paralela con Reanudación (solicitudes Range)
Manejo inteligente de fallos de Range (200 vs 206)
Progreso en tiempo real con cálculo de velocidad
Verificación SHA256 después de la descarga
Fusión a través de llama-gguf-split
Cálculo de ETA

ETA = (Total Bytes - Bytes Descargados) / Velocidad Actual
Cuantizaciones Soportadas

F16, F32, Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, Q3_K_M, Q3_K_S, Q2_K, IQ4_XS, IQ3_XS, IQ2_XS, IQ1_S
Licencia

Licencia MIT - ver archivo LICENSE para más detalles.
Agradecimientos

llama.cpp por la utilidad de fusión
Hugging Face por el alojamiento de modelos
Python Tkinter por la GUI
Soporte

Problemas: GitHub Issues
Discusiones: GitHub Discussions
Dale una Estrella a este Proyecto

Si encuentras útil esta herramienta, ¡dale una estrella en GitHub!

Hecho con ❤️ para la comunidad de IA