"""
Entry point aplikasi Exa Manager.

Modul ini menginisialisasi FastAPI app dan mengatur konfigurasi dasar.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import load_or_create_config
from app.logger import setup_logger

# Inisialisasi logger
logger = setup_logger()

# Load konfigurasi
config = load_or_create_config()
host = config["server"]["ip"]
port = int(config["server"]["port"])

# Konfigurasi FastAPI
app = FastAPI(
    title="Exa Manager",
    description="Addon untuk aplikasi Otomax: Mengatur dan mengelola update produk secara otomatis",
    version="0.1.0",
)

# Tambahkan CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Karena aplikasi berjalan di localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Endpoint root untuk mengecek status API."""
    logger.info("Akses endpoint /")
    return {"msg": "Exa Manager API", "status": "running"}


@app.get("/health")
def health_check():
    """Endpoint untuk health check sistem."""
    logger.debug("Health check dipanggil")
    return {"status": "healthy"}


# Nanti tambahkan router API di sini
# from app.api.router import products_router, suppliers_router
# app.include_router(products_router)
# app.include_router(suppliers_router)


def start():
    """Fungsi untuk memulai aplikasi."""
    logger.info(f"Starting FastAPI App on {host}:{port}...")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    start()
