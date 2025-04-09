"""
Modul konfigurasi untuk Exa Manager.

Berisi pengaturan untuk server, database, dan aplikasi.
Gunakan get_settings() untuk mendapatkan semua konfigurasi.
"""

from app.config.settings import get_settings

__all__ = ["get_settings"]
