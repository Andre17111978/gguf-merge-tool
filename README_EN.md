GGUF Merge Tool v9.2

Professional GUI + CLI tool for downloading, verifying and merging sharded GGUF models from Hugging Face.
Table of Contents

    Features

    Quick Start

    Installation

    CLI Usage

    GUI Usage

    Configuration

    Requirements

    Troubleshooting

    Performance Tips

    Technical Details

    License

    Acknowledgments

    Support

Features

Modern GUI - Tkinter-based interface with scrollable file list and mouse wheel support

Smart Grouping - Files automatically grouped by quantization type (Q4_K_M, Q5_K_S, etc.)

Resume Downloads - HTTP Range requests with smart fallback protection (200 vs 206 handling)

Parallel Downloading - Configurable threads (auto-detects CPU cores)

Hash Verification - SHA256 verification using HF LFS metadata

Smart Merge - Uses llama-gguf-split from llama.cpp

CLI Support - download and merge subcommands for automation

Smart Detection - Automatically finds llama-gguf-split in common locations

Path Persistence - Saves llama.cpp path between sessions

Retry Logic - Automatic retry with exponential backoff (3 attempts)

Real-time ETA - Shows speed (MB/s) and estimated time remaining

Multi-language - English, Russian, Chinese, Spanish, German, Japanese documentation
Quick Start
Windows

Install dependencies:
pip install huggingface_hub tqdm requests

Download llama-gguf-split from: https://github.com/ggerganov/llama.cpp/releases

Run the tool:
python gguf_merge_tool.py
Linux / macOS

Install dependencies:
pip install huggingface_hub tqdm requests

Run the tool:
python3 gguf_merge_tool.py
Installation
From Source (Recommended)

Clone the repository:
git clone https://github.com/yourusername/gguf-merge-tool.git
cd gguf-merge-tool

Install dependencies:
pip install -r requirements.txt

Run the tool:
python src/gguf_merge_tool.py
From PyPI (Coming Soon)

pip install gguf-merge-tool
gguf-merge-gui
Windows Users: Required Binary

Download llama-gguf-split.exe from llama.cpp releases
Place it in one of these locations:

    tools/llama-gguf-split.exe

    bin/llama-gguf-split.exe

    Or specify the path in GUI settings

CLI Usage
Download Specific Files

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f Qwen3.5-122B-A10B-Q4_K_M-00001-of-00008.gguf Qwen3.5-122B-A10B-Q4_K_M-00002-of-00008.gguf
Download Entire Repository

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Download with Authentication (Private Repo)

python src/gguf_merge_tool.py download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Merge Parts

python src/gguf_merge_tool.py merge -d ./models -o ./models/merged_model.gguf -f
CLI Arguments Reference

Command: download
-d, --dir - Directory to save files - Required: Yes
-r, --repo - Hugging Face repository ID - Required: Yes
-b, --branch - Repository branch (default: main) - Required: No
-t, --token - HF access token - Required: No
-f, --files - List of files to download - Required: No

Command: merge
-d, --dir - Directory with parts - Required: Yes
-o, --output - Output file path - Required: No
-f, --force - Overwrite existing file - Required: No
GUI Usage
Step 1: Load Repository

Enter Hugging Face repo ID (e.g., unsloth/Qwen3.5-122B-A10B-GGUF)
Enter branch (default: main)
Enter your HF token (required for private repos)
Click "Load" button
Step 2: Select Files

Files are automatically grouped by quantization type
Click "Select All" to select all files
Or select individual files with checkboxes
Step 3: Download

Click "Download" or "Download All"
Monitor progress in real-time:

    Progress bar shows percentage

    Status bar shows: [1/4] filename.gguf: 45% | 4.5 MB/s | ETA: 2h 15m

Step 4: Verify (Optional but Recommended)

Click "Verify" button
Tool validates SHA256 hashes against HF metadata
Shows success message if all hashes match
Step 5: Merge (Optional)

Select at least 2 parts (checkboxes)
Click "Merge" button
Tool calls llama-gguf-split --merge
Output file is saved with correct base name
Configuration
llama.cpp Path

In GUI, locate "Path to llama.cpp":
Click "Find" for auto-detection
Or click "Browse" to select manually
Path is saved to llama_path.txt for persistence
Thread Settings

Adjust JOBS constant in code (default: min(4, os.cpu_count() or 2)):
In gguf_merge_tool.py
JOBS = min(4, os.cpu_count() or 2) - Change this value
Disk Space Margin

Change DISK_SPACE_MARGIN (default: 1.1 = 10% extra):
DISK_SPACE_MARGIN = 1.1
Download Chunk Size

Change CHUNK_SIZE (default: 1 MB):
CHUNK_SIZE = 1024 * 1024
Requirements

Python >= 3.8
huggingface_hub >= 0.20.0
tqdm >= 4.60.0
requests >= 2.28.0
gguf >= 0.1.0 (optional, for metadata reading)
llama-gguf-split (from llama.cpp)
Verify Installation

python -c "import huggingface_hub, tqdm, requests; print('All dependencies installed')"
Troubleshooting
llama-gguf-split not found

Download from llama.cpp releases
Place in tools/ folder or specify path in GUI
HTTP 401 Unauthorized or HTTP 403 Forbidden

Enter your Hugging Face token
Ensure token has read access to the repository
Token format: hf_xxxxxxxxxxxxxxxxxx
Insufficient disk space

Free up disk space (need 10% extra for merge)
Change download directory to another drive
Use DISK_SPACE_MARGIN to adjust buffer
Download stuck at 0%

Check internet connection
Verify token is correct
Check if repository is private
Check if repository exists
File corrupted after resume

Tool has built-in Range fallback protection
If server doesn't support Range (returns 200 instead of 206), it starts download from scratch
This is intentional to prevent file corruption
GUI doesn't start

Check Tkinter is installed (usually included with Python)
On Linux: sudo apt-get install python3-tk
On macOS: brew install python-tk
Performance Tips

Many small files - Keep default threads (4)
Few large files - Increase threads to 8
Slow network - Reduce threads to 2
Fast NVMe SSD - Keep default or increase
Network interruptions - Tool handles resume automatically
Technical Details
Download Flow

Parse HF repo to get file list with sizes and hashes
User selects files to start download
Check disk space - abort if insufficient
Parallel download with Resume (Range requests)
Smart Range fallback (200 vs 206 handling)
Real-time progress with speed calculation
SHA256 verification after download
Merge via llama-gguf-split
ETA Calculation

ETA = (Total Bytes - Downloaded Bytes) / Current Speed
Supported Quantizations

F16, F32, Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, Q3_K_M, Q3_K_S, Q2_K, IQ4_XS, IQ3_XS, IQ2_XS, IQ1_S
License

MIT License - see LICENSE file for details.
Acknowledgments

llama.cpp for the merge utility
Hugging Face for the model hosting
Python Tkinter for GUI
Support

Issues: GitHub Issues
Discussions: GitHub Discussions
Star This Project

If you find this tool useful, please give it a star on GitHub!

Made with ❤️ for the AI community