"""
Orkestrasi utama aplikasi Exa Manager.

Modul ini berisi fungsi-fungsi factory untuk membuat aplikasi FastAPI
dan mengatur seluruh komponen aplikasi.
"""

import logging
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings

# Setup logger
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Mengatur siklus hidup aplikasi FastAPI.

    Dijalankan saat startup dan shutdown aplikasi.

    Args:
        app: Instans aplikasi FastAPI
    """
    # Konfigurasi logging
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.app.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info("Aplikasi memulai...")

    # Inisialisasi komponen aplikasi (akan ditambahkan nanti)
    # - Database
    # - Cache
    # - Services

    yield  # Aplikasi berjalan di sini

    # Cleanup pada shutdown
    logger.info("Aplikasi shutdown...")
    # - Tutup koneksi database
    # - Cleanup resources


def create_app() -> FastAPI:
    """
    Factory function untuk membuat instance aplikasi FastAPI.

    Mengatur semua komponen aplikasi termasuk routes, middleware, dan error handlers.

    Returns:
        FastAPI: Objek aplikasi FastAPI yang telah dikonfigurasi
    """
    # Mendapatkan konfigurasi terpadu
    settings = get_settings()

    # Membuat aplikasi FastAPI dengan pengaturan dari konfigurasi
    app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        lifespan=lifespan,
    )

    # Tambahkan middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable):
        """
        Middleware untuk logging request.
        """
        logger.debug(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        return response

    # Tambahkan exception handler
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Handler untuk menangani semua exception yang tidak tertangkap.
        """
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Terjadi kesalahan pada server"},
        )

    # Daftarkan routes (akan diimplementasikan nanti)
    # register_routes(app)

    return app
