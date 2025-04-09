from functools import lru_cache

from pydantic_settings import BaseSettings

from app.config.app_settings import AppSettings
from app.config.database_settings import DatabaseSettings
from app.config.server_settings import ServerSettings


class Settings(BaseSettings):
    """
    Konfigurasi utama yang menggabungkan semua pengaturan.

    Attributes:
        server (ServerSettings): Konfigurasi server
        database (DatabaseSettings): Konfigurasi database
        app (AppSettings): Konfigurasi aplikasi
    """

    server: ServerSettings = ServerSettings()
    database: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


@lru_cache()
def get_settings() -> Settings:
    """
    Mendapatkan instance settings dengan cache untuk efisiensi.

    Caching ini mencegah pembacaan berulang dari file .env dan
    menghemat penggunaan memori.

    Returns:
        Settings: Objek konfigurasi aplikasi
    """
    return Settings()
