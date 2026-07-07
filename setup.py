#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Функция для чтения версии из основного файла
def get_version():
    with open("gguf_merge_tool.py", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("VERSION"):
                return line.split("=")[1].strip().strip('"')
    return "10.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gguf-merge-tool",
    version=get_version(),  # Автоматически берет 10.0 из кода
    author="Andre",
    author_email="satarangel@gmail.com",
    description="Professional GUI + CLI tool for downloading, verifying and merging sharded GGUF models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Andre17111978/gguf-merge-tool",
    packages=find_packages(),  # Упрощаем, если файл в корне
    py_modules=["gguf_merge_tool"],  # Основной модуль
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)