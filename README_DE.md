GGUF Merge Tool v9.2

Professionelles GUI + CLI Tool zum Herunterladen, Überprüfen und Zusammenführen von shardierten GGUF-Modellen von Hugging Face.
Inhaltsverzeichnis

    Funktionen

    Schnellstart

    Installation

    CLI-Nutzung

    GUI-Nutzung

    Konfiguration

    Anforderungen

    Fehlerbehebung

    Leistungstipps

    Technische Details

    Lizenz

    Danksagungen

    Unterstützung

Funktionen

Moderne GUI - Tkinter-basierte Oberfläche mit scrollbarer Dateiliste und Mausrad-Unterstützung

Intelligente Gruppierung - Automatische Gruppierung nach Quantisierungstyp (Q4_K_M, Q5_K_S, etc.)

Fortsetzbare Downloads - HTTP Range-Anfragen mit intelligentem Fallback-Schutz (200 vs 206 Behandlung)

Paralleler Download - Konfigurierbare Threads (automatische CPU-Kernererkennung)

Hash-Überprüfung - SHA256-Verifizierung mit HF LFS-Metadaten

Intelligente Zusammenführung - Verwendet llama-gguf-split von llama.cpp

CLI-Unterstützung - download- und merge-Subcommands für Automatisierung

Intelligente Erkennung - Findet llama-gguf-split automatisch an üblichen Orten

Pfad-Persistenz - Speichert den llama.cpp-Pfad zwischen Sitzungen

Wiederholungslogik - Automatische Wiederholung mit exponentiellem Backoff (3 Versuche)

Echtzeit-ETA - Zeigt Geschwindigkeit (MB/s) und geschätzte verbleibende Zeit

Mehrsprachig - Dokumentation in 6 Sprachen
Schnellstart
Windows

Abhängigkeiten installieren:
pip install huggingface_hub tqdm requests

llama-gguf-split herunterladen von: https://github.com/ggerganov/llama.cpp/releases

Tool ausführen:
python gguf_merge_tool.py
Linux / macOS

Abhängigkeiten installieren:
pip install huggingface_hub tqdm requests

Tool ausführen:
python3 gguf_merge_tool.py
Installation
Aus dem Quellcode (Empfohlen)

Repository klonen:
git clone https://github.com/yourusername/gguf-merge-tool.git
cd gguf-merge-tool

Abhängigkeiten installieren:
pip install -r requirements.txt

Tool ausführen:
python src/gguf_merge_tool.py
Von PyPI (Demnächst)

pip install gguf-merge-tool
gguf-merge-gui
Windows-Benutzer: Erforderliche Binärdatei

llama-gguf-split.exe von llama.cpp-Releases herunterladen
An einem der folgenden Orte platzieren:

    tools/llama-gguf-split.exe

    bin/llama-gguf-split.exe

    Oder Pfad in den GUI-Einstellungen angeben

CLI-Nutzung
Bestimmte Dateien herunterladen

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f Qwen3.5-122B-A10B-Q4_K_M-00001-of-00008.gguf Qwen3.5-122B-A10B-Q4_K_M-00002-of-00008.gguf
Vollständiges Repository herunterladen

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Mit Authentifizierung herunterladen (Privates Repository)

python src/gguf_merge_tool.py download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Teile zusammenführen

python src/gguf_merge_tool.py merge -d ./models -o ./models/merged_model.gguf -f
CLI-Argumentreferenz

Befehl: download
-d, --dir - Verzeichnis zum Speichern von Dateien - Erforderlich: Ja
-r, --repo - Hugging Face Repository-ID - Erforderlich: Ja
-b, --branch - Repository-Branch (Standard: main) - Erforderlich: Nein
-t, --token - HF-Zugriffstoken - Erforderlich: Nein
-f, --files - Liste der herunterzuladenden Dateien - Erforderlich: Nein

Befehl: merge
-d, --dir - Verzeichnis mit den Teilen - Erforderlich: Ja
-o, --output - Pfad der Ausgabedatei - Erforderlich: Nein
-f, --force - Vorhandene Datei überschreiben - Erforderlich: Nein
GUI-Nutzung
Schritt 1: Repository laden

Hugging Face Repository-ID eingeben (z.B. unsloth/Qwen3.5-122B-A10B-GGUF)
Branch eingeben (Standard: main)
HF-Token eingeben (für private Repositories erforderlich)
Auf "Laden" klicken
Schritt 2: Dateien auswählen

Dateien werden automatisch nach Quantisierungstyp gruppiert
Auf "Alle auswählen" klicken, um alle Dateien auszuwählen
Oder einzelne Dateien mit Kontrollkästchen auswählen
Schritt 3: Herunterladen

Auf "Herunterladen" oder "Alle herunterladen" klicken
Fortschritt in Echtzeit verfolgen:

    Fortschrittsbalken zeigt Prozentsatz

    Statusleiste zeigt: [1/4] datei.gguf: 45% | 4.5 MB/s | ETA: 2h 15m

Schritt 4: Überprüfen (Optional aber Empfohlen)

Auf "Überprüfen" klicken
Tool validiert SHA256-Hashes gegen HF-Metadaten
Zeigt Erfolgsmeldung, wenn alle Hashes übereinstimmen
Schritt 5: Zusammenführen (Optional)

Mindestens 2 Teile auswählen (Kontrollkästchen)
Auf "Zusammenführen" klicken
Tool führt llama-gguf-split --merge aus
Ausgabedatei wird mit korrektem Basisnamen gespeichert
Konfiguration
llama.cpp-Pfad

In der GUI "Pfad zu llama.cpp" finden:
Auf "Suchen" für automatische Erkennung klicken
Oder auf "Durchsuchen" für manuelle Auswahl klicken
Pfad wird in llama_path.txt für Persistenz gespeichert
Thread-Einstellungen

JOBS-Konstante im Code anpassen (Standard: min(4, os.cpu_count() or 2)):
In gguf_merge_tool.py
JOBS = min(4, os.cpu_count() or 2) - Diesen Wert ändern
Festplattenplatz-Puffer

DISK_SPACE_MARGIN ändern (Standard: 1.1 = 10% Puffer):
DISK_SPACE_MARGIN = 1.1
Download-Chunk-Größe

CHUNK_SIZE ändern (Standard: 1 MB):
CHUNK_SIZE = 1024 * 1024
Anforderungen

Python >= 3.8
huggingface_hub >= 0.20.0
tqdm >= 4.60.0
requests >= 2.28.0
gguf >= 0.1.0 (optional, zum Lesen von Metadaten)
llama-gguf-split (von llama.cpp)
Installation überprüfen

python -c "import huggingface_hub, tqdm, requests; print('Alle Abhängigkeiten installiert')"
Fehlerbehebung
llama-gguf-split nicht gefunden

Von llama.cpp-Releases herunterladen
In tools/-Ordner platzieren oder Pfad in GUI angeben
HTTP 401 Unauthorized oder HTTP 403 Forbidden

Hugging Face Token eingeben
Sicherstellen, dass das Token Lesezugriff auf das Repository hat
Token-Format: hf_xxxxxxxxxxxxxxxxxx
Nicht genügend Festplattenspeicher

Festplattenspeicher freigeben (10% Puffer für Zusammenführung benötigt)
Download-Verzeichnis auf ein anderes Laufwerk ändern
DISK_SPACE_MARGIN zum Anpassen des Puffers verwenden
Download bleibt bei 0% hängen

Internetverbindung prüfen
Token auf Richtigkeit prüfen
Prüfen, ob Repository privat ist
Prüfen, ob Repository existiert
Datei nach Fortsetzung beschädigt

Tool hat integrierten Range-Fallback-Schutz
Wenn Server Range nicht unterstützt (200 statt 206 zurückgibt), beginnt Download von vorne
Dies ist beabsichtigt, um Dateibeschädigung zu verhindern
GUI startet nicht

Prüfen, ob Tkinter installiert ist (normalerweise in Python enthalten)
Unter Linux: sudo apt-get install python3-tk
Unter macOS: brew install python-tk
Leistungstipps

Viele kleine Dateien - Standard-Threads beibehalten (4)
Wenige große Dateien - Threads auf 8 erhöhen
Langsames Netzwerk - Threads auf 2 reduzieren
Schnelle NVMe SSD - Standard beibehalten oder erhöhen
Netzwerkunterbrechungen - Tool setzt Download automatisch fort
Technische Details
Download-Ablauf

HF-Repository nach Dateiliste mit Größen und Hashes durchsuchen
Benutzer wählt Dateien für den Download aus
Festplattenspeicher prüfen - abbrechen, wenn unzureichend
Paralleler Download mit Fortsetzung (Range-Anfragen)
Intelligenter Range-Fallback (200 vs 206 Behandlung)
Echtzeit-Fortschritt mit Geschwindigkeitsberechnung
SHA256-Überprüfung nach dem Download
Zusammenführung über llama-gguf-split
ETA-Berechnung

ETA = (Gesamtbytes - Heruntergeladene Bytes) / Aktuelle Geschwindigkeit
Unterstützte Quantisierungen

F16, F32, Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, Q3_K_M, Q3_K_S, Q2_K, IQ4_XS, IQ3_XS, IQ2_XS, IQ1_S
Lizenz

MIT-Lizenz - siehe LICENSE-Datei für Details.
Danksagungen

llama.cpp für das Zusammenführungs-Tool
Hugging Face für das Modell-Hosting
Python Tkinter für die GUI
Unterstützung

Probleme: GitHub Issues
Diskussionen: GitHub Discussions
Geben Sie diesem Projekt einen Stern

Wenn Sie dieses Tool nützlich finden, geben Sie ihm einen Stern auf GitHub!

Mit ❤️ für die KI-Community gemacht