from typing import Any, Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    Konfigurasi untuk koneksi database.

    Attributes:
        sqlite_path (str): Path ke file database SQLite
        sqlite_connect_args (Dict): Argumen koneksi untuk SQLite
        mssql_* : Konfigurasi untuk koneksi SQL Server (Otomax)
    """

    # SQLite settings
    sqlite_path: str = Field(default="./exa_manager.db", alias="DATABASE_SQLITE_PATH")
    sqlite_connect_args: Dict[str, Any] = {"check_same_thread": False}

    # SQL Server settings (Otomax)
    mssql_host: str = Field(default="localhost", alias="DATABASE_MSSQL_HOST")
    mssql_port: int = Field(default=1433, alias="DATABASE_MSSQL_PORT")
    mssql_db: str = Field(default="otomax", alias="DATABASE_MSSQL_DB")
    mssql_user: str = Field(default="sa", alias="DATABASE_MSSQL_USER")
    mssql_password: str = Field(default="password", alias="DATABASE_MSSQL_PASSWORD")
    mssql_driver: str = Field(
        default="ODBC Driver 17 for SQL Server", alias="DATABASE_MSSQL_DRIVER"
    )

    @property
    def sqlite_url(self) -> str:
        """Mendapatkan URL koneksi SQLite."""
        return f"sqlite:///{self.sqlite_path}"

    @property
    def mssql_url(self) -> str:
        """Mendapatkan URL koneksi SQL Server."""
        return f"mssql+pyodbc://{self.mssql_user}:{self.mssql_password}@{self.mssql_host}:{self.mssql_port}/{self.mssql_db}?driver={self.mssql_driver.replace(' ', '+')}"

    # Konfigurasi model untuk Pydantic V2
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Mengabaikan field tambahan dari .env
    )
