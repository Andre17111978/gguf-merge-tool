# GGUF Merge Tool v10.0

[![PyPI version](https://badge.fury.io/py/gguf-merge-tool.svg)](https://pypi.org/project/gguf-merge-tool/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Professional GUI + CLI tool for downloading, verifying and merging sharded GGUF models from Hugging Face.**

---

## ✨ Новое в версии 10.0

| Фича | Описание |
|------|----------|
| **Исправлены статусбары** | При проверке хэшей и склейке прогресс отображается плавно и корректно |
| **Загрузка локальных файлов** | Кнопка "Локальные" позволяет выбрать папку с GGUF-файлами на диске и работать с ними без скачивания |
| **История репозиториев** | Выпадающий список в поле ввода репозитория — сохраняются последние 10 запросов |

---

## 🚀 Основные возможности

- **Скачивание** GGUF-файлов с Hugging Face с поддержкой докачки (resume).
- **Проверка целостности** (SHA-256) загруженных файлов.
- **Склейка** частей (сплитов) в один GGUF-файл с помощью `llama-gguf-split`.
- **Группировка** файлов по квантованию и базовому имени.
- **Многопоточное** скачивание (автоопределение числа ядер).
- **Реальный ETA** и скорость (MB/s) во время загрузки.
- **CLI-режим** для автоматизации.
- **Сохранение** токена и пути к `llama.cpp` между сессиями.

---

## 📦 Установка

### Из PyPI (рекомендуемый способ)

```bash
pip install gguf-merge-tool
После установки доступны две команды:

gguf-merge-gui — запуск графического интерфейса

gguf-merge — запуск CLI-режима

Из исходников
bash
git clone https://github.com/Andre17111978/gguf-merge-tool.git
cd gguf-merge-tool
pip install -r requirements.txt
python gguf_merge_tool.py
🖥️ Использование (GUI)
bash
gguf-merge-gui
# или
python gguf_merge_tool.py
Интерфейс по шагам:
Репозиторий — введите ID репозитория на Hugging Face (например, unsloth/Qwen3.5-122B-A10B-GGUF).
История автоматически сохраняет последние 10 запросов.

Ветка — обычно main.

Токен — опционально, для приватных репозиториев (формат: hf_xxxxxxxxxxxxxxxxxx).

Папка скачивания — куда сохранять файлы.

Путь к llama.cpp — укажите папку, где находится llama-gguf-split (нужно для склейки).

Файлы — список GGUF-файлов с чекбоксами, автоматически сгруппированных по квантованию.

Кнопки управления:

Загрузить — получить список файлов из репозитория.

Локальные — выбрать папку с GGUF-файлами на диске.

Выбрать всё / Скачать всё — массовые операции.

Скачать — загрузка выбранных файлов.

Проверить — проверка SHA-256.

Склеить — объединить выбранные части.

⌨️ Использование (CLI)
Скачивание конкретных файлов
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f model-00001-of-00003.gguf model-00002-of-00003.gguf
Скачивание всего репозитория
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
Скачивание с токеном (приватный репозиторий)
bash
gguf-merge download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
Склейка частей
bash
gguf-merge merge -d ./models -o ./models/merged_model.gguf -f
Аргументы CLI
Команда download:

-d, --dir — папка для сохранения (обязательно)

-r, --repo — ID репозитория (обязательно)

-b, --branch — ветка (по умолчанию: main)

-t, --token — токен Hugging Face

-f, --files — список файлов для скачивания

Команда merge:

-d, --dir — папка с частями (обязательно)

-o, --output — путь к выходному файлу

-f, --force — перезаписать существующий файл

⚙️ Требования
Python >= 3.8

Зависимости (устанавливаются автоматически):

huggingface_hub >= 0.20.0

tqdm >= 4.60.0

requests >= 2.28.0

gguf >= 0.1.0 (опционально, для чтения метаданных)

llama-gguf-split (скачать с llama.cpp releases)

🛠️ Устранение проблем
llama-gguf-split не найден
Скачайте с llama.cpp releases

Поместите в папку tools/ или укажите путь в настройках GUI

HTTP 401/403 (Unauthorized/Forbidden)
Введите корректный токен Hugging Face

Убедитесь, что токен имеет доступ к репозиторию

Недостаточно места на диске
Освободите место или смените папку скачивания

В коде можно изменить DISK_SPACE_MARGIN (по умолчанию 1.1 = 10% запаса)

GUI не запускается на Linux
bash
sudo apt-get install python3-tk  # Debian/Ubuntu
brew install python-tk           # macOS
📝 Лицензия
Распространяется под лицензией MIT. Подробности в файле LICENSE.

🙏 Благодарности
llama.cpp за утилиту склейки

Hugging Face за хостинг моделей

Сообществу за тестирование и идеи

⭐ Поддержка проекта
Если инструмент оказался полезным, поставьте звезду на GitHub!

Сделано с ❤️ для AI-сообщества