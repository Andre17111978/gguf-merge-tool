#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gguf-merge-tool",
    version="9.2.0",
    author="Ваше Имя",
    author_email="your.email@example.com",
    description="Professional tool for downloading, verifying and merging sharded GGUF models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ваш_логин/gguf-merge-tool",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
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
        ],
    },
)