#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GGUF Merge Tool v9.2 - Production Ready с защитой от Range Fallback"""

import os,sys,re,threading,subprocess,shutil,hashlib,logging,time,webbrowser,argparse
from pathlib import Path
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import filedialog,messagebox,ttk

# === ЗАВИСИМОСТИ ===
import requests

try:
    import gguf; HAS_GGUF=True
except ImportError: HAS_GGUF=False

try:
    from tqdm import tqdm; HAS_TQDM=True
except ImportError: HAS_TQDM=False

try:
    from huggingface_hub import HfApi, hf_hub_url, snapshot_download; HF_AVAILABLE=True
except ImportError: HF_AVAILABLE=False

# === КОНСТАНТЫ ===
JOBS = min(4, os.cpu_count() or 2)
VERSION = "9.2"
CHUNK_SIZE = 1024 * 1024
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 60
DISK_SPACE_MARGIN = 1.1
MAX_RETRIES = 3
RETRY_DELAY = 2
C = {'dwd': 'N:/AI/AI_GPT/TXT_Models', 'llama_path': ''}

_QUANT_LIST = [
    'F16','F32','Q8_0','Q6_K','Q5_K_M','Q5_K_S','Q4_K_M','Q4_K_S',
    'Q3_K_M','Q3_K_S','Q2_K','IQ4_XS','IQ3_XS','IQ2_XS','IQ1_S'
]
QUANT_PATTERN = re.compile(
    r'(?<=[-_.])(' + '|'.join(re.escape(q) for q in _QUANT_LIST) + r')(?=[-_.]|$)',
    re.IGNORECASE
)

logging.basicConfig(filename='gguf.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

# === УТИЛИТЫ ===
def format_size(size):
    if not size or size <= 0: return "?"
    for u in ['KB','MB','GB','TB']:
        if size < 1024: return f"{size:.2f} {u}"
        size /= 1024
    return f"{size:.2f} TB"

@lru_cache(maxsize=None)
def find_executable(name, base_dir=None):
    if path := shutil.which(name): return path
    paths_to_check = []
    if base_dir and Path(base_dir).exists():
        base = Path(base_dir)
        paths_to_check = [
            base, base/'bin', base/'Scripts', base/'tools',
            base/'installer_files'/'env'/'Scripts',
            base/'installer_files'/'env'/'bin',
            base/'installer_files'/'conda'/'Scripts',
            base/'installer_files'/'conda'/'bin',
            base/'installer_files'/'env'/'Lib'/'site-packages'/'llama_cpp_binaries'/'bin',
            base/'installer_files'/'env'/'Lib'/'site-packages'/'ik_llama_cpp_binaries'/'bin',
            base/'venv'/'Scripts', base/'venv'/'bin',
            base/'env'/'Scripts', base/'env'/'bin',
            base/'build'/'bin', base/'build'/'Release',
        ]
    else:
        paths_to_check = [
            Path.cwd()/'tools', Path.cwd()/'bin', Path.cwd()/'Scripts',
            Path.home()/'llama.cpp'/'bin',
            Path.home()/'llama.cpp'/'build'/'bin',
        ]
    if C.get('llama_path'):
        p = Path(C['llama_path'])
        if p.exists():
            paths_to_check.append(p)
            paths_to_check.extend([p/'bin', p/'Scripts'])
    candidates = [name, f"{name}.exe"] if sys.platform == 'win32' else [name]
    for path in paths_to_check:
        if not path.exists(): continue
        for n in candidates:
            if (exe := path / n).exists():
                return str(exe)
    return None

def find_llama_path(base_dir=None):
    if exe := find_executable('llama-gguf-split', base_dir):
        return str(Path(exe).parent)
    return ''

def invalidate_cache():
    find_executable.cache_clear()

def get_gguf_meta(file_path):
    if HAS_GGUF:
        try:
            reader = gguf.GGUFReader(file_path)
            return reader.metadata.get('general.name', file_path.stem) if reader.metadata else file_path.stem
        except: pass
    return file_path.stem

def detect_quantization(filename):
    if m := QUANT_PATTERN.search(filename): return m.group(1)
    return None

def remove_quantization(filename):
    return QUANT_PATTERN.sub('', filename)

def group_files(files):
    groups = {}
    for f in files:
        name = f.rfilename
        quant = detect_quantization(name)
        base = remove_quantization(name)
        base = re.sub(r'[-_][0-9a-f]+[-_of]+[-0-9]+|[-_](split|part|segment)[-_a-z0-9]+', '', base, flags=re.IGNORECASE)
        key = f"{base}|{quant}" if quant else base
        groups.setdefault(key, []).append(f)
    return groups

def extract_base_name(file_paths):
    if not file_paths: return "merged"
    name = get_gguf_meta(file_paths[0])
    if name and name != "merged": return name
    raw_name = remove_quantization(file_paths[0].name)
    for pattern in [r'-\d+-of-\d+', r'-split-[a-z]', r'-[a-z](?=\.gguf$)', r'-part\d+', r'-segment\d+']:
        raw_name = re.sub(pattern, '', raw_name, flags=re.IGNORECASE)
    return raw_name[:-5] if raw_name.lower().endswith('.gguf') else raw_name or file_paths[0].stem

def extract_part_number(filename):
    filename = filename.lower()
    if m := re.search(r'-0*(\d+)-of-', filename): return int(m.group(1))
    if m := re.search(r'-split-([a-z])', filename): return ord(m.group(1)) - 96
    if m := re.search(r'-part(\d+)', filename): return int(m.group(1))
    if m := re.search(r'-segment(\d+)', filename): return int(m.group(1))
    return None

def find_parts(directory):
    directory = Path(directory)
    if not directory.exists(): return []
    parts = []
    for f in directory.glob("*.gguf"):
        if num := extract_part_number(f.name): parts.append((num, f))
    return [p for _, p in sorted(parts, key=lambda x: x[0])] if parts else sorted(directory.glob("*.gguf"))

def merge_parts(parts, output_path, progress_callback, process_holder=None):
    tool = find_executable("llama-gguf-split", C.get('llama_path'))
    if not tool:
        raise RuntimeError("llama-gguf-split не найден! Укажите путь в настройках")
    required_space = sum(p.stat().st_size for p in parts)
    if shutil.disk_usage(output_path.parent).free < required_space * DISK_SPACE_MARGIN:
        raise RuntimeError("Недостаточно места на диске!")
    cmd = [tool, "--merge", str(parts[0]), str(output_path)]
    kw = {'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True, 'bufsize': 1}
    if sys.platform == 'win32': kw['creationflags'] = 0x08000000
    proc = subprocess.Popen(cmd, **kw)
    if process_holder is not None: process_holder['proc'] = proc
    last = 0
    while proc.poll() is None:
        if line := proc.stdout.readline():
            if m := re.search(r'(\d+)%', line):
                pct = int(m.group(1))
                if pct > last: last = pct; progress_callback(pct)
            print(f"\r{line.strip()}", end="", flush=True)
    return proc.returncode == 0

def download_file_with_resume(url, output_path, token=None, cancel_event=None, progress_callback=None):
    """
    Скачивание с Resume, защитой от Range Fallback (200 вместо 206)
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    local_size = output_path.stat().st_size if output_path.exists() else 0
    range_requested = local_size > 0
    
    if range_requested:
        headers['Range'] = f'bytes={local_size}-'
        mode = 'ab'
    else:
        mode = 'wb'

    for attempt in range(MAX_RETRIES):
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)) as resp:
                # Range Not Satisfiable — файл уже скачан полностью
                if resp.status_code == 416:
                    if progress_callback: progress_callback(1, 1)
                    return True
                
                # ✅ КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Проверка поддержки Range
                if range_requested and resp.status_code == 200:
                    # Сервер не поддержал Range — начинаем заново
                    log.warning(f"Сервер не поддержал Range для {Path(output_path).name}, начинаем заново")
                    mode = 'wb'
                    local_size = 0
                    range_requested = False
                
                # HTTP ошибки
                if resp.status_code in (401, 403):
                    raise RuntimeError(f"Доступ запрещен (HTTP {resp.status_code}). Проверьте токен.")
                if resp.status_code == 404:
                    raise RuntimeError("Файл не найден на сервере (HTTP 404).")
                if resp.status_code == 429:
                    raise RuntimeError("Слишком много запросов (HTTP 429).")
                if resp.status_code >= 500:
                    raise RuntimeError(f"Ошибка сервера (HTTP {resp.status_code}).")
                if resp.status_code >= 400:
                    raise RuntimeError(f"HTTP ошибка {resp.status_code}")
                resp.raise_for_status()
                
                content_type = resp.headers.get('content-type', '').lower()
                if 'text/html' in content_type:
                    raise RuntimeError("Сервер вернул HTML вместо файла. Проверьте токен или URL.")
                
                # ✅ Правильный расчёт total в зависимости от статуса
                if resp.status_code == 206:
                    # Partial Content — content-length это размер оставшейся части
                    total = int(resp.headers.get('content-length', 0)) + local_size
                else:
                    # Full Content — content-length это полный размер файла
                    total = int(resp.headers.get('content-length', 0))
                
                downloaded = local_size
                with open(output_path, mode) as f:
                    for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                        if cancel_event and cancel_event.is_set():
                            f.close()
                            if mode == 'wb': output_path.unlink(missing_ok=True)
                            raise RuntimeError("Скачивание отменено")
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback:
                                progress_callback(downloaded, total)
                return True
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt < MAX_RETRIES - 1:
                log.warning(f"Сетевая ошибка ({attempt+1}/{MAX_RETRIES}): {e}. Повтор...")
                time.sleep(RETRY_DELAY)
            else:
                raise RuntimeError(f"Сетевая ошибка после {MAX_RETRIES} попыток: {e}")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP ошибка: {e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ошибка запроса: {e}")

# === GUI ===
class GGUFDownloader:
    def __init__(self, root):
        if not HF_AVAILABLE:
            messagebox.showerror("Ошибка", "Установите: pip install huggingface_hub")
            sys.exit(1)
        self.root = root
        self.root.title(f"GGUF Merge Tool v{VERSION}")
        self.root.geometry("950x700")
        self.root.resizable(True, True)
        self.files = []
        self.checkboxes = []
        self.running = False
        self.cancel_requested = False
        self.executor = None
        self.futures = []
        self.process_holder = {'proc': None}
        self.api = HfApi()
        self.cancel_event = threading.Event()
        self._load_llama_path()
        self._build_ui()
        self._load_token()
        self._update_merge_button_state()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_llama_path(self):
        try:
            path = Path("llama_path.txt").read_text().strip()
            if path and Path(path).exists():
                C['llama_path'] = path
                invalidate_cache()
        except: pass

    def _save_llama_path(self, path):
        Path("llama_path.txt").write_text(path)
        C['llama_path'] = path
        invalidate_cache()

    def _update_merge_button_state(self):
        base_dir = self.llama_entry.get().strip()
        if find_executable("llama-gguf-split", base_dir):
            self.merge_btn.config(state="normal")
        else:
            self.merge_btn.config(state="disabled")

    def _check_tool(self):
        base_dir = self.llama_entry.get().strip()
        if find_executable("llama-gguf-split", base_dir):
            return True
        msg = "llama-gguf-split не найден!\n\nУкажите путь к папке с llama.cpp в настройках,\nили скачайте с GitHub."
        if messagebox.askyesno("Инструмент не найден", msg + "\n\nСкачать с GitHub?"):
            webbrowser.open("https://github.com/ggerganov/llama.cpp/releases")
            messagebox.showinfo("Инструкция",
                "1. Скачайте последний релиз\n2. Распакуйте\n3. Скопируйте llama-gguf-split.exe в папку\n"
                "   и укажите путь в настройках")
        return False

    def _build_ui(self):
        rf = ttk.LabelFrame(self.root, text=" 1. Репозиторий ", padding=10)
        rf.pack(fill="x", padx=10, pady=5)
        ttk.Label(rf, text="ID:").grid(row=0, column=0)
        self.repo_entry = ttk.Entry(rf); self.repo_entry.insert(0, "unsloth/Qwen3.5-122B-A10B-GGUF")
        self.repo_entry.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Label(rf, text="Ветка:").grid(row=1, column=0)
        self.revision_entry = ttk.Entry(rf); self.revision_entry.insert(0, "main")
        self.revision_entry.grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Label(rf, text="Токен:").grid(row=2, column=0)
        self.token_entry = ttk.Entry(rf, show="*")
        self.token_entry.grid(row=2, column=1, sticky="ew", padx=5)
        rf.columnconfigure(1, weight=1)
        bf = ttk.Frame(rf); bf.grid(row=0, column=2, rowspan=3, padx=5)
        ttk.Button(bf, text="Загрузить", command=self._load_files).pack(side="left", padx=2)
        ttk.Button(bf, text="Выбрать всё", command=self._select_all).pack(side="left", padx=2)
        ttk.Button(bf, text="Скачать всё", command=self._download_all).pack(side="left", padx=2)

        df = ttk.LabelFrame(self.root, text=" 2. Папка для скачивания ", padding=10)
        df.pack(fill="x", padx=10, pady=5)
        self.dir_entry = ttk.Entry(df); self.dir_entry.insert(0, C['dwd'])
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(df, text="Обзор", command=self._browse_dir).pack(side="right", padx=5)

        lf = ttk.LabelFrame(self.root, text=" 2.5. Путь к llama.cpp ", padding=10)
        lf.pack(fill="x", padx=10, pady=5)
        self.llama_entry = ttk.Entry(lf); self.llama_entry.insert(0, C.get('llama_path', ''))
        self.llama_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Label(lf, text="(укажите папку, где находится llama-gguf-split)", font=("Segoe UI", 8)).pack(side="bottom", anchor="w", padx=5)
        ttk.Button(lf, text="Найти", command=self._auto_find_llama).pack(side="right", padx=2)
        ttk.Button(lf, text="Обзор", command=self._browse_llama).pack(side="right", padx=2)

        files_container = ttk.Frame(self.root)
        files_container.pack(fill="both", expand=True, padx=10, pady=5)
        self.files_label_frame = ttk.LabelFrame(files_container, text=" 3. Файлы ", padding=10)
        self.files_label_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.files_label_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.files_label_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.progress_bar = ttk.Progressbar(self.root, mode="determinate")
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.status_label = ttk.Label(self.root, text="Готов")
        self.status_label.pack()

        btf = ttk.Frame(self.root); btf.pack(pady=10)
        self.download_btn = ttk.Button(btf, text="Скачать", command=self._start_download, state="disabled")
        self.download_btn.pack(side="left", padx=5)
        self.verify_btn = ttk.Button(btf, text="Проверить", command=self._verify_hashes, state="disabled")
        self.verify_btn.pack(side="left", padx=5)
        self.merge_btn = ttk.Button(btf, text="Склеить", command=self._start_merge, state="disabled")
        self.merge_btn.pack(side="left", padx=5)
        self.cancel_btn = ttk.Button(btf, text="Отмена", command=self._cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=5)
        self.info_label = ttk.Label(self.root, text="", font=("Segoe UI", 8))
        self.info_label.pack()

    def _browse_dir(self):
        if f := filedialog.askdirectory():
            self.dir_entry.delete(0, tk.END); self.dir_entry.insert(0, f)

    def _browse_llama(self):
        if f := filedialog.askdirectory(title="Выберите папку с llama.cpp"):
            self.llama_entry.delete(0, tk.END); self.llama_entry.insert(0, f)
            self._save_llama_path(f)
            self._update_merge_button_state()

    def _auto_find_llama(self):
        base_dir = self.llama_entry.get().strip()
        if not base_dir:
            messagebox.showwarning("Внимание", "Сначала укажите папку с llama.cpp!")
            return
        self.status_label.config(text="🔍 Поиск в указанной папке...")
        self.root.update()
        if exe := find_executable('llama-gguf-split', base_dir):
            path = str(Path(exe).parent)
            self.llama_entry.delete(0, tk.END)
            self.llama_entry.insert(0, path)
            self._save_llama_path(path)
            self.status_label.config(text=f"✅ Найдено: {path}")
            self._update_merge_button_state()
            messagebox.showinfo("Успех", f"llama-gguf-split найден в:\n{path}")
        else:
            self.status_label.config(text="❌ Не найдено")
            messagebox.showinfo("Не найдено", "llama-gguf-split не найден в указанной папке!")

    def _select_all(self):
        for v in self.checkboxes: v.set(True)
        self._update_info()

    def _download_all(self):
        self._select_all(); self._start_download()

    def _update_info(self):
        sel = [i for i, v in enumerate(self.checkboxes) if v.get()]
        total = sum(self.files[i][1] for i in sel)
        self.info_label.config(text=f"Выбрано: {len(sel)} файлов, {format_size(total)}" if sel else "")

    def _load_token(self):
        try: self.token_entry.insert(0, Path("hf_token.txt").read_text().strip())
        except: pass

    def _set_ui_state(self, state):
        if self.running and state == "normal": return
        for b in [self.download_btn, self.verify_btn]: b.config(state=state)
        if state == "normal":
            self._update_merge_button_state()
        else:
            self.merge_btn.config(state=state)
        self.cancel_btn.config(state="normal" if state == "disabled" and self.running else "disabled")

    def _load_files(self):
        repo = self.repo_entry.get().strip()
        token = self.token_entry.get().strip()
        if token: Path("hf_token.txt").write_text(token)
        if not repo:
            messagebox.showerror("Ошибка", "Введите ID репозитория!"); return
        self._set_ui_state("disabled")
        self.status_label.config(text="Загрузка списка файлов...")
        threading.Thread(target=self._load_files_worker, args=(repo, token), daemon=True).start()

    def _load_files_worker(self, repo, token):
        try:
            info = self.api.repo_info(repo, files_metadata=True, token=token or None)
            files = sorted([f for f in info.siblings if f.rfilename.lower().endswith('.gguf')],
                          key=lambda x: x.rfilename)
            self.root.after(0, self._render_files, files)
        except Exception as e:
            log.error(f"Ошибка загрузки: {e}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))

    def _render_files(self, files):
        for w in self.scrollable_frame.winfo_children(): w.destroy()
        self.files.clear(); self.checkboxes.clear()
        groups = group_files(files)
        for key, gfiles in groups.items():
            if len(gfiles) > 1:
                parts = key.split('|')
                if len(parts) == 2:
                    display = f"📁 {parts[0]} [{parts[1]}]"
                else:
                    display = f"📁 {key}"
                ttk.Label(self.scrollable_frame, text=display, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10, pady=(5,0))
            for f in gfiles:
                size = getattr(f, "size", 0)
                sha = getattr(f, "lfs", {}).get("sha256") if getattr(f, "lfs", None) else None
                self.files.append((f.rfilename, size, sha))
                var = tk.BooleanVar(); var.trace('w', lambda *a: self._update_info())
                self.checkboxes.append(var)
                ttk.Checkbutton(self.scrollable_frame, text=f"  {f.rfilename} [{format_size(size)}]", variable=var).pack(anchor="w", padx=20)
        self.status_label.config(text=f"Найдено: {len(files)} файлов")
        self._update_info()
        if self.files: self._set_ui_state("normal")

    def _cancel(self):
        self.cancel_requested = True; self.cancel_event.set()
        if self.executor:
            for f in self.futures: f.cancel()
            self.executor.shutdown(wait=False); self.executor = None
        self._terminate_process()
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="⚠️ Отменено")
        self.running = False; self._set_ui_state("normal")

    def _terminate_process(self):
        if self.process_holder and self.process_holder.get('proc'):
            if self.process_holder['proc'].poll() is None:
                self.process_holder['proc'].terminate(); self.process_holder['proc'] = None

    def _start_download(self):
        if self.running: return
        sel = [i for i, v in enumerate(self.checkboxes) if v.get()]
        if not sel:
            messagebox.showwarning("Внимание", "Выберите файлы для скачивания!"); return
        target = Path(self.dir_entry.get().strip()); target.mkdir(exist_ok=True)
        total_size = sum(self.files[i][1] for i in sel if self.files[i][1] and self.files[i][1] > 0)
        if total_size > 0 and shutil.disk_usage(target).free < total_size * DISK_SPACE_MARGIN:
            messagebox.showerror("Ошибка", f"Недостаточно места! Нужно: {format_size(total_size)}"); return
        self.running = True; self.cancel_requested = False; self.cancel_event.clear()
        self.futures = []; self.executor = None
        self._set_ui_state("disabled"); self.progress_bar["value"] = 0
        self.status_label.config(text=f"⏳ Загрузка {len(sel)} файлов...")
        threading.Thread(target=self._download_worker, args=(sel, target), daemon=True).start()

    def _download_worker(self, sel, target):
        total_files = len(sel)
        repo = self.repo_entry.get().strip()
        revision = self.revision_entry.get().strip() or "main"
        token = self.token_entry.get().strip() or None
        completed = 0
        errors = []
        lock = threading.Lock()
        speed_data = {}

        def download_one(index, file_index):
            nonlocal completed
            filename, size, _ = self.files[index]
            output_path = target / filename
            try:
                url = hf_hub_url(repo, filename, revision=revision)
                log.debug(f"URL для {filename}: {url}")
                
                actual_size = size if size and size > 0 else 0
                if actual_size == 0 and output_path.exists():
                    actual_size = output_path.stat().st_size
                if actual_size > 0 and shutil.disk_usage(target).free < actual_size * DISK_SPACE_MARGIN:
                    raise RuntimeError(f"Недостаточно места! Нужно: {format_size(actual_size)}")
                
                self.root.after(0, lambda: self.status_label.config(
                    text=f"[{file_index}/{total_files}] {filename} ({format_size(actual_size) if actual_size > 0 else '?'}) - скачивание..."))

                speed_data[filename] = {
                    'last_bytes': 0,
                    'last_time': time.time(),
                    'speed': 0,
                    'total_bytes': actual_size
                }

                def progress_callback(downloaded, total):
                    now = time.time()
                    data = speed_data[filename]
                    data['total_bytes'] = total if total > 0 else data['total_bytes']
                    
                    # Скорость
                    if now - data['last_time'] >= 0.5:
                        speed = (downloaded - data['last_bytes']) / (now - data['last_time']) / (1024**2)
                        if speed > 0:
                            data['speed'] = speed
                        data['last_bytes'] = downloaded
                        data['last_time'] = now
                    
                    # Проценты
                    pct = int((downloaded / total) * 100) if total > 0 else 0
                    speed_mb = data['speed']
                    
                    # ✅ ETA с защитой от отрицательных значений
                    if total > 0 and speed_mb > 0.01:
                        remaining_bytes = total - downloaded
                        if remaining_bytes > 0:
                            eta_seconds = remaining_bytes / (speed_mb * 1024**2)
                            if eta_seconds >= 86400:
                                days = int(eta_seconds // 86400)
                                hours = int((eta_seconds % 86400) // 3600)
                                eta_str = f"{days}д {hours}ч"
                            elif eta_seconds >= 3600:
                                hours = int(eta_seconds // 3600)
                                minutes = int((eta_seconds % 3600) // 60)
                                eta_str = f"{hours}ч {minutes}м"
                            elif eta_seconds >= 60:
                                minutes = int(eta_seconds // 60)
                                seconds = int(eta_seconds % 60)
                                eta_str = f"{minutes}м {seconds}с"
                            else:
                                eta_str = f"{max(1, int(eta_seconds))}с"
                        else:
                            eta_str = "✅"
                    else:
                        eta_str = "⏳"
                    
                    speed_str = f"{speed_mb:.1f} MB/s" if speed_mb > 0 else "?"
                    self.root.after(0, self._update_progress, pct, filename, file_index, total_files, speed_str, eta_str)

                download_file_with_resume(url, output_path, token, self.cancel_event, progress_callback)
                
                with lock:
                    completed += 1
                    pct = int((completed / total_files) * 100)
                self.root.after(0, self._update_progress, pct, filename, file_index, total_files, "✅", "")
                log.info(f"Скачан: {filename} ({format_size(output_path.stat().st_size)})")
                return True
            except Exception as e:
                error_msg = f"{filename}: {e}"
                log.error(error_msg)
                with lock:
                    errors.append(error_msg)
                if not self.cancel_requested:
                    self.root.after(0, lambda msg=error_msg: self.status_label.config(text=f"❌ {msg}"))
                return False

        self.executor = ThreadPoolExecutor(max_workers=JOBS)
        self.futures = [self.executor.submit(download_one, idx, i) for i, idx in enumerate(sel)]
        try:
            for f in as_completed(self.futures):
                if self.cancel_requested: break
                f.result()
        except Exception as e:
            log.error(f"Ошибка в пуле: {e}")
        finally:
            self.executor.shutdown(wait=False)
            self.executor = None
            speed_data.clear()

        if not self.cancel_requested:
            if errors:
                log.error(f"Ошибки скачивания: {errors}")
                self.root.after(0, lambda: messagebox.showerror("Ошибки скачивания", "\n".join(errors[:5])))
            self.root.after(0, self._finish_download)

    def _update_progress(self, progress, filename, current, total, speed_str="", eta_str=""):
        self.progress_bar["value"] = progress
        
        status_parts = []
        if speed_str and speed_str != "✅":
            status_parts.append(speed_str)
        if eta_str:
            status_parts.append(f"ETA: {eta_str}")
        
        status = " | ".join(status_parts) if status_parts else ""
        
        if speed_str == "✅":
            status = "✅ Завершено"
        
        self.status_label.config(text=f"[{current}/{total}] {Path(filename).name}: {progress}% {status}")

    def _finish_download(self):
        self.progress_bar["value"] = 100
        self.status_label.config(text="✅ Загрузка завершена!")
        self.running = False
        self._set_ui_state("normal")
        if not self.cancel_requested:
            messagebox.showinfo("Готово", "Все файлы скачаны!")

    def _verify_hashes(self):
        if self.running: return
        sel = [i for i, v in enumerate(self.checkboxes) if v.get()]
        if not sel:
            messagebox.showwarning("Внимание", "Выберите файлы для проверки!"); return
        self.running = True; self._set_ui_state("disabled")
        threading.Thread(target=self._verify_worker, args=(sel,), daemon=True).start()

    def _verify_worker(self, sel):
        target = Path(self.dir_entry.get().strip())
        errors = []; verified = 0
        for i, idx in enumerate(sel, 1):
            filename, _, sha = self.files[idx]
            file_path = target / filename
            if not file_path.exists(): errors.append(f"{filename}: не найден"); continue
            if not sha: errors.append(f"{filename}: нет хэша"); continue
            self.root.after(0, lambda n=filename, c=i: self.status_label.config(text=f"[{c}/{len(sel)}] Хэш {Path(n).name}..."))
            hasher = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(64 * 1024 * 1024): hasher.update(chunk)
            if hasher.hexdigest().lower() == sha.lower(): verified += 1
            else: errors.append(f"{filename}: хэш не совпадает!")
        self.root.after(0, self._finish_verify, verified, len(sel), errors)

    def _finish_verify(self, verified, total, errors):
        self.running = False; self._set_ui_state("normal"); self.progress_bar["value"] = 100
        if verified == total:
            self.status_label.config(text=f"✅ Все {total} хэшей совпали")
            messagebox.showinfo("Успех", f"Все {total} файлов целы!")
        else: messagebox.showerror("Ошибки", "\n".join(errors))

    def _start_merge(self):
        if self.running: return
        base_dir = self.llama_entry.get().strip()
        if not find_executable("llama-gguf-split", base_dir):
            self._check_tool()
            self._update_merge_button_state()
            if not find_executable("llama-gguf-split", base_dir): return
        sel = [i for i, v in enumerate(self.checkboxes) if v.get()]
        if len(sel) < 2:
            messagebox.showwarning("Внимание", "Выберите минимум 2 части для склейки!"); return
        target = Path(self.dir_entry.get().strip())
        parts = [target / self.files[i][0] for i in sel if (target / self.files[i][0]).exists()]
        if len(parts) != len(sel):
            messagebox.showerror("Ошибка", "Некоторые файлы не найдены на диске!"); return
        output_path = target / f"{extract_base_name(parts)}.gguf"
        if output_path.exists() and not messagebox.askyesno("Перезапись", f"{output_path.name} существует. Перезаписать?"): return
        self.running = True; self.cancel_requested = False
        self.process_holder = {'proc': None}
        self._set_ui_state("disabled"); self.progress_bar["value"] = 0
        self.status_label.config(text="Склейка...")

        def worker():
            try:
                def progress_callback(progress):
                    self.root.after(0, lambda: self.progress_bar.configure(value=progress))
                if merge_parts(parts, output_path, progress_callback, self.process_holder):
                    self.root.after(0, lambda: self.progress_bar.configure(value=100))
                    self.root.after(0, lambda: self.status_label.config(text="✅ Склейка завершена!"))
                    self.root.after(0, lambda: messagebox.showinfo("Успех", f"Склеено: {output_path.name}"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Склейка не удалась"))
            except Exception as e:
                log.error(f"Ошибка склейки: {e}")
                self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
            finally:
                self.root.after(0, self._finish_merge)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_merge(self):
        self.running = False; self._set_ui_state("normal")

    def _on_close(self):
        self.cancel_requested = True; self.cancel_event.set()
        if self.executor:
            for f in self.futures: f.cancel()
            self.executor.shutdown(wait=False); self.executor = None
        self._terminate_process(); self.root.destroy()

# === CLI ===
def cli_download(repo, directory, revision="main", token=None, files=None):
    if not HF_AVAILABLE:
        print("[ERROR] huggingface_hub не установлен"); return 1
    directory = Path(directory); directory.mkdir(exist_ok=True)
    if files:
        file_iter = tqdm(files, desc="Файлы", unit="file") if HAS_TQDM else files
        for f in file_iter:
            url = hf_hub_url(repo, f, revision=revision)
            output = directory / f
            pbar = None
            def progress(downloaded, total):
                nonlocal pbar
                if pbar is None and HAS_TQDM and total:
                    pbar = tqdm(total=total, desc=f, unit="B", unit_scale=True, leave=False)
                if pbar:
                    pbar.update(downloaded - pbar.n)
            try:
                download_file_with_resume(url, output, token, None, progress)
            except Exception as e:
                print(f"\n❌ Ошибка: {f}: {e}")
                return 1
            finally:
                if pbar: pbar.close()
    else:
        snapshot_download(repo, local_dir=directory, token=token, revision=revision)
    print("✅ Готово!"); return 0

def cli_merge(directory, output=None, force=False):
    parts = find_parts(directory)
    if len(parts) < 2:
        print(f"[ERROR] Найдено {len(parts)} частей. Нужно минимум 2"); return 1
    if not output: output = Path(directory) / f"{extract_base_name(parts)}.gguf"
    else: output = Path(output)
    if output.exists() and not force:
        print(f"[WARN] {output} существует. Используйте --force"); return 1
    print(f"[INFO] Найдено {len(parts)} частей"); print(f"[INFO] Выходной файл: {output}")
    print("[INFO] Запуск склейки...")
    last = 0
    def cb(pct):
        nonlocal last
        if pct > last: last = pct; print(f"\rПрогресс: {pct}%", end="", flush=True)
    try:
        if merge_parts(parts, output, cb):
            print(f"\n✅ Склейка завершена: {output}"); return 0
        print("\n❌ Ошибка склейки"); return 1
    except Exception as e:
        log.error(f"Ошибка склейки: {e}"); print(f"\n❌ {e}"); return 1

def cli_mode():
    parser = argparse.ArgumentParser(description=f"GGUF Merge Tool v{VERSION}")
    parser.add_argument("--version", action="version", version=f"v{VERSION}")
    sub = parser.add_subparsers(dest='command', help='Команда')
    dl = sub.add_parser('download', help='Скачать файлы')
    dl.add_argument("-d", "--dir", required=True)
    dl.add_argument("-r", "--repo", required=True)
    dl.add_argument("-b", "--branch", default="main")
    dl.add_argument("-t", "--token")
    dl.add_argument("-f", "--files", nargs="+")
    mg = sub.add_parser('merge', help='Склеить части')
    mg.add_argument("-d", "--dir", required=True)
    mg.add_argument("-o", "--output")
    mg.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()
    if args.command == 'download': sys.exit(cli_download(args.repo, args.dir, args.branch, args.token, args.files))
    elif args.command == 'merge': sys.exit(cli_merge(args.dir, args.output, args.force))
    else: parser.print_help(); sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1: cli_mode()
    else: root = tk.Tk(); app = GGUFDownloader(root); root.mainloop()