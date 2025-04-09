from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Konfigurasi umum aplikasi.

    Attributes:
        name (str): Nama aplikasi
        version (str): Versi aplikasi
        description (str): Deskripsi singkat aplikasi
        environment (str): Mode lingkungan aplikasi (development/production)
        log_level (str): Level logging aplikasi
    """

    name: str = "Exa Manager"
    version: str = "1.0.0"
    description: str = "Addon untuk mengelola produk di aplikasi Otomax"

    # Gunakan alias alih-alih parameter env
    environment: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")

    # Tambahan konfigurasi spesifik aplikasi
    default_page_size: int = Field(default=20, alias="APP_DEFAULT_PAGE_SIZE")
    max_page_size: int = Field(default=100, alias="APP_MAX_PAGE_SIZE")
    sync_interval_minutes: int = Field(default=60, alias="SYNC_INTERVAL_MINUTES")

    # Konfigurasi model untuk Pydantic V2
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Mengabaikan field tambahan dari .env
    )
