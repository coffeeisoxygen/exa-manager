"""
Modul untuk mengelola konfigurasi aplikasi.

File konfigurasi disimpan dalam format .ini dan berisi pengaturan
untuk server, database, dan aplikasi.
"""

import os
from configparser import ConfigParser
from typing import Dict

DEFAULT_CONFIG: Dict[str, Dict[str, str]] = {
    "server": {"ip": "127.0.0.1", "port": "8000"},
    "database": {
        "sqlite_path": "./data/exa_manager.db",
        "mssql_trusted_connection": "false",  # Windows Authentication | SQL Authentication
        "mssql_server": "localhost",
        "mssql_database": "OTOMAX",
        "mssql_username": "",
        "mssql_password": "",
        "mssql_driver": "ODBC Driver 17 for SQL Server",
        "mssql_timeout": "30",
    },
    "app": {
        "update_interval": "3600",  # dalam detik (1 jam)
        "log_level": "INFO",
    },
}


def load_or_create_config(file_path: str = "./config.ini") -> ConfigParser:
    """
    Memuat file konfigurasi atau membuat file baru dengan nilai default jika belum ada.

    Args:
        file_path: Lokasi file konfigurasi

    Returns:
        ConfigParser: Objek konfigurasi siap pakai.
    """
    config = ConfigParser()

    if os.path.exists(file_path):
        config.read(file_path)
        _ensure_default_config(config)
    else:
        _create_default_config(config, file_path)

    return config


def _ensure_default_config(config: ConfigParser) -> None:
    """
    Memastikan setiap section dan key dalam konfigurasi memiliki nilai default.

    Args:
        config: Objek konfigurasi yang akan diperiksa dan dilengkapi.
    """
    for section, values in DEFAULT_CONFIG.items():
        if section not in config:
            config[section] = values
        else:
            for key, value in values.items():
                config[section].setdefault(key, value)


def _create_default_config(config: ConfigParser, file_path: str) -> None:
    """
    Membuat file konfigurasi baru dengan nilai default.

    Args:
        config: Objek konfigurasi yang akan diisi.
        file_path: Lokasi file konfigurasi yang akan dibuat.
    """
    for section, values in DEFAULT_CONFIG.items():
        config[section] = values

    with open(file_path, "w") as config_file:
        config.write(config_file)
