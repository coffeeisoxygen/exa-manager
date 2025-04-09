"""
Modul untuk setup dan konfigurasi logger aplikasi.

Menyediakan sistem logging dengan:
- Output ke file dengan rotasi harian
- Output ke konsol dengan warna
- Non-blocking logging dengan queue handler
- Support untuk multiple environment (development, testing, production)
"""

import datetime
import logging
import os
import sys
from logging.handlers import QueueHandler, QueueListener, TimedRotatingFileHandler
from queue import Queue

from colorama import Fore, Style
from colorama import init as colorama_init
from dotenv import load_dotenv

from app.config import load_or_create_config

# Inisialisasi warna terminal
colorama_init(autoreset=True)

# Load dari file .env (kalau ada)
load_dotenv()

# Tentukan environment (default: production)
ENV = os.getenv("ENV", "production").lower()

# Konfigurasi dasar
config = load_or_create_config()

# Default log level berdasarkan environment
DEFAULT_LOG_LEVELS = {
    "development": "DEBUG",
    "testing": "DEBUG",
    "production": "INFO",
}

# Ambil log level dari environment atau config, dengan fallback ke default berdasarkan environment
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    config.get("app", "log_level", fallback=DEFAULT_LOG_LEVELS.get(ENV, "INFO")),
).upper()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


# Warna sesuai level log
def colorize(level, message):
    color_map = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }
    return f"{color_map.get(level, '')}{message}{Style.RESET_ALL}"


# Formatter dengan warna
class ColorFormatter(logging.Formatter):
    def format(self, record):
        original_msg = super().format(record)
        return colorize(record.levelname, original_msg)


# Format dasar
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
color_formatter = ColorFormatter(
    "[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)

# === HANDLER FILE DENGAN ROTASI HARIAN ===
# Menggunakan format tanggal pada nama file untuk memudahkan tracking
tanggal_sekarang = datetime.datetime.now().strftime("%Y%m%d")
log_filename = os.path.join(LOG_DIR, f"app_{ENV}_{tanggal_sekarang}.log")
file_handler = TimedRotatingFileHandler(
    filename=log_filename,
    when="midnight",  # rotasi setiap tengah malam
    interval=1,
    backupCount=7,  # simpan 7 hari
    encoding="utf-8",
    utc=False,
)
# Mengubah suffix menjadi format yang lebih konsisten
file_handler.suffix = "_%Y%m%d"
file_handler.setFormatter(formatter)

# === HANDLER CONSOLE (PAKE WARNA) ===
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(color_formatter)

# === NON-BLOCKING QUEUE HANDLER ===
log_queue = Queue()
queue_handler = QueueHandler(log_queue)

# === LISTENER UNTUK MENJALANKAN HANDLER DI BACKGROUND ===
listener = QueueListener(log_queue, file_handler, console_handler)
listener.start()


# === SETUP LOGGER UTAMA ===
def setup_logger(name: str = "app_logger") -> logging.Logger:
    """
    Membuat dan mengkonfigurasi logger aplikasi.

    Args:
        name: Nama untuk logger

    Returns:
        Logger yang sudah dikonfigurasi sesuai environment
    """
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    logger.addHandler(queue_handler)
    logger.propagate = False  # Hindari duplikat log

    # Log environment saat pertama kali setup
    if name == "app_logger":
        logger.info(f"Aplikasi berjalan dalam mode: {ENV.upper()}")
        logger.info(f"Log level: {LOG_LEVEL}")

    return logger
