GGUF Merge Tool v10.0
https://badge.fury.io/py/gguf-merge-tool.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg

Professional GUI + CLI tool for downloading, verifying and merging sharded GGUF models from Hugging Face.

✨ What's New in Version 10.0
Feature	Description
Fixed Status Bars	Progress displays smoothly and correctly during hash verification and merging operations
Local File Loading	"Local" button allows you to select a folder with GGUF files on disk and work with them without downloading
Repository History	Dropdown list in the repository input field — saves the last 10 queries
🚀 Key Features
Download GGUF files from Hugging Face with resume support.

Integrity verification (SHA-256) of downloaded files.

Merge parts (splits) into a single GGUF file using llama-gguf-split.

Group files by quantization and base name.

Multithreaded downloading (auto-detects number of cores).

Real ETA and speed (MB/s) during download.

CLI mode for automation.

Persistent token and llama.cpp path across sessions.

📦 Installation
From PyPI (recommended)
bash
pip install gguf-merge-tool
After installation, two commands are available:

gguf-merge-gui — launch the graphical interface

gguf-merge — launch CLI mode

From Source
bash
git clone https://github.com/Andre17111978/gguf-merge-tool.git
cd gguf-merge-tool
pip install -r requirements.txt
python gguf_merge_tool.py
🖥️ Usage (GUI)
bash
gguf-merge-gui
# or
python gguf_merge_tool.py
Step-by-step Interface:
Field	Description
Repository	Enter the Hugging Face repository ID (e.g., unsloth/Qwen3.5-122B-A10B-GGUF).
History automatically saves the last 10 queries.
Branch	Usually main.
Token	Optional, for private repositories (format: hf_xxxxxxxxxxxxxxxxxx).
Download Folder	Where to save files.
llama.cpp Path	Specify the folder containing llama-gguf-split (required for merging).
Files	List of GGUF files with checkboxes, automatically grouped by quantization.
Control Buttons:
Button	Function
Load	Fetch the list of files from the repository.
Local	Select a folder with GGUF files on disk.
Select All / Download All	Mass operations.
Download	Download selected files.
Verify	Check SHA-256 hashes.
Merge	Combine selected parts.
⌨️ Usage (CLI)
Download Specific Files
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f model-00001-of-00003.gguf model-00002-of-00003.gguf
Download Entire Repository
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Download with Token (Private Repository)
bash
gguf-merge download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Merge Parts
bash
gguf-merge merge -d ./models -o ./models/merged_model.gguf -f
CLI Arguments
Command download:

Argument	Description
-d, --dir	Save folder (required)
-r, --repo	Repository ID (required)
-b, --branch	Branch (default: main)
-t, --token	Hugging Face token
-f, --files	List of files to download
Command merge:

Argument	Description
-d, --dir	Folder with parts (required)
-o, --output	Output file path
-f, --force	Overwrite existing file
⚙️ Requirements
Python >= 3.8

Dependencies (installed automatically):
huggingface_hub >= 0.20.0

tqdm >= 4.60.0

requests >= 2.28.0

gguf >= 0.1.0 (optional, for reading metadata)

Additional Tool Required:
llama-gguf-split (download from llama.cpp releases)

🛠️ Troubleshooting
llama-gguf-split Not Found
Download from llama.cpp releases

Place it in the tools/ folder or specify the path in GUI settings

HTTP 401/403 (Unauthorized/Forbidden)
Enter a valid Hugging Face token

Ensure the token has access to the repository

Insufficient Disk Space
Free up space or change the download folder

You can modify DISK_SPACE_MARGIN in the code (default: 1.1 = 10% buffer)

GUI Doesn't Start on Linux
bash
sudo apt-get install python3-tk  # Debian/Ubuntu
brew install python-tk           # macOS
📝 License
Distributed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments
llama.cpp for the merge utility

Hugging Face for hosting models

The community for testing and ideas

⭐ Support the Project
If you find this tool useful, please star it on GitHub!

Made with ❤️ for the AI community

