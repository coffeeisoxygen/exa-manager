"""
Entry point untuk aplikasi.

Menginisialisasi konfigurasi, logger, dan memulai aplikasi.
"""

from app.app_config import AppConfig
from app.logger import setup_logger

# Inisialisasi konfigurasi
config = AppConfig()

# Setup logger
logger = setup_logger()

if __name__ == "__main__":
    logger.info("Aplikasi dimulai...")
    logger.info(
        f"Server berjalan di {config.get('server', 'ip')}:{config.get('server', 'port')}"
    )
