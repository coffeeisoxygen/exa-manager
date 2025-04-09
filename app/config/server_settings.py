from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """
    Konfigurasi untuk server FastAPI.

    Attributes:
        host (str): Alamat IP server
        port (int): Port server
        reload (bool): Mode auto-reload untuk development
        workers (int): Jumlah worker proses
        log_level (str): Level logging untuk uvicorn
    """

    # Gunakan alias alih-alih parameter env
    host: str = Field(default="127.0.0.1", alias="SERVER_IP")
    port: int = Field(default=8000, alias="SERVER_PORT")
    reload: bool = Field(default=True, alias="SERVER_RELOAD")
    workers: int = Field(default=1, alias="SERVER_WORKERS")
    log_level: str = Field(default="info", alias="SERVER_LOG_LEVEL")

    # Tambahkan extra="ignore" untuk mengabaikan field yang tidak terdaftar
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Mengabaikan field tambahan dari .env
    )
