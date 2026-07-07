#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from pathlib import Path

def get_version():
    version_file = Path(__file__).parent / "gguf_merge_tool.py"
    if not version_file.exists():
        return "10.0.1"
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("VERSION"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "10.0.1"

setup(
    name="gguf-merge-tool",
    version=get_version(),
    author="Andre",
    author_email="satarangel@gmail.com",
    description="Professional GUI + CLI tool for downloading, verifying and merging sharded GGUF models",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/Andre17111978/gguf-merge-tool",
    py_modules=["gguf_merge_tool"],
    python_requires=">=3.8",
    install_requires=[
        "huggingface_hub>=0.20.0",
        "tqdm>=4.60.0",
        "requests>=2.28.0",
        "gguf>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "gguf-merge=gguf_merge_tool:cli_mode",
            "gguf-merge-gui=gguf_merge_tool:main_gui",
        ],
    },
)