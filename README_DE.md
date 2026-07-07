GGUF Merge Tool v10.0
https://badge.fury.io/py/gguf-merge-tool.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg

Professionelles GUI + CLI-Tool zum Herunterladen, Überprüfen und Zusammenführen von shardierten GGUF-Modellen von Hugging Face.

✨ Neu in Version 10.0
Funktion	Beschreibung
Behobene Fortschrittsbalken	Fortschrittsanzeige während Hash-Überprüfung und Zusammenführung läuft jetzt flüssig und korrekt
Lokale Dateien laden	"Lokal"-Button ermöglicht die Auswahl eines Ordners mit GGUF-Dateien auf der Festplatte – ohne Download
Repository-Verlauf	Dropdown-Liste im Repository-Eingabefeld – speichert die letzten 10 Anfragen
🚀 Hauptfunktionen
Herunterladen von GGUF-Dateien von Hugging Face mit Fortsetzungsunterstützung (Resume).

Integritätsprüfung (SHA-256) der heruntergeladenen Dateien.

Zusammenführen von Teilen (Splits) in eine einzelne GGUF-Datei mit llama-gguf-split.

Gruppierung von Dateien nach Quantisierung und Basisnamen.

Multithreaded-Herunterladen (automatische Erkennung der CPU-Kerne).

Echte ETA und Geschwindigkeit (MB/s) während des Downloads.

CLI-Modus für Automatisierung.

Speicherung von Token und llama.cpp-Pfad über Sitzungen hinweg.

📦 Installation
Von PyPI (empfohlen)
bash
pip install gguf-merge-tool
Nach der Installation stehen zwei Befehle zur Verfügung:

gguf-merge-gui – Startet die grafische Oberfläche

gguf-merge – Startet den CLI-Modus

Aus dem Quellcode
bash
git clone https://github.com/Andre17111978/gguf-merge-tool.git
cd gguf-merge-tool
pip install -r requirements.txt
python gguf_merge_tool.py
🖥️ Verwendung (GUI)
bash
gguf-merge-gui
# oder
python gguf_merge_tool.py
Schritt-für-Schritt-Oberfläche:
Feld	Beschreibung
Repository	Hugging Face Repository-ID eingeben (z.B. unsloth/Qwen3.5-122B-A10B-GGUF).
Der Verlauf speichert automatisch die letzten 10 Anfragen.
Branch	Normalerweise main.
Token	Optional, für private Repositories (Format: hf_xxxxxxxxxxxxxxxxxx).
Download-Ordner	Wo die Dateien gespeichert werden sollen.
llama.cpp-Pfad	Ordner mit llama-gguf-split angeben (für Zusammenführung erforderlich).
Dateien	Liste der GGUF-Dateien mit Checkboxen, automatisch nach Quantisierung gruppiert.
Steuerungsbuttons:
Button	Funktion
Laden	Dateiliste vom Repository abrufen.
Lokal	Ordner mit GGUF-Dateien auf der Festplatte auswählen.
Alle auswählen / Alle herunterladen	Massenoperationen.
Herunterladen	Ausgewählte Dateien herunterladen.
Überprüfen	SHA-256-Hashes prüfen.
Zusammenführen	Ausgewählte Teile kombinieren.
⌨️ Verwendung (CLI)
Bestimmte Dateien herunterladen
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f model-00001-of-00003.gguf model-00002-of-00003.gguf
Komplettes Repository herunterladen
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Mit Token herunterladen (privates Repository)
bash
gguf-merge download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Teile zusammenführen
bash
gguf-merge merge -d ./models -o ./models/merged_model.gguf -f
CLI-Argumente
Befehl download:

Argument	Beschreibung
-d, --dir	Speicherordner (erforderlich)
-r, --repo	Repository-ID (erforderlich)
-b, --branch	Branch (Standard: main)
-t, --token	Hugging Face-Token
-f, --files	Liste der herunterzuladenden Dateien
Befehl merge:

Argument	Beschreibung
-d, --dir	Ordner mit den Teilen (erforderlich)
-o, --output	Pfad zur Ausgabedatei
-f, --force	Vorhandene Datei überschreiben
⚙️ Systemanforderungen
Python >= 3.8

Abhängigkeiten (werden automatisch installiert):
huggingface_hub >= 0.20.0

tqdm >= 4.60.0

requests >= 2.28.0

gguf >= 0.1.0 (optional, zum Lesen von Metadaten)

Zusätzlich benötigtes Tool:
llama-gguf-split (von den llama.cpp-Releases herunterladen)

🛠️ Fehlerbehebung
llama-gguf-split nicht gefunden
Von den llama.cpp-Releases herunterladen

In den tools/-Ordner legen oder den Pfad in den GUI-Einstellungen angeben

HTTP 401/403 (Unauthorized/Forbidden)
Gültiges Hugging Face-Token eingeben

Sicherstellen, dass das Token Zugriff auf das Repository hat

Nicht genügend Speicherplatz
Speicherplatz freigeben oder Download-Ordner wechseln

DISK_SPACE_MARGIN im Code anpassen (Standard: 1.1 = 10 % Puffer)

GUI startet unter Linux nicht
bash
sudo apt-get install python3-tk  # Debian/Ubuntu
brew install python-tk           # macOS
📝 Lizenz
Vertrieben unter der MIT-Lizenz. Details finden Sie in der LICENSE-Datei.

🙏 Danksagungen
llama.cpp – für das Zusammenführungstool

Hugging Face – für das Hosting der Modelle

Der Community – für Tests und Ideen

⭐ Projekt unterstützen
Wenn Sie dieses Tool nützlich finden, geben Sie ihm bitte einen Stern auf GitHub!

Mit ❤️ für die KI-Community gemacht