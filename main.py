"""
Entry point utama aplikasi Exa Manager.

Modul ini menyediakan fungsi untuk memulai aplikasi dengan uvicorn.
"""

import uvicorn

from app.config import get_settings


def start():
    """
    Entry point utama aplikasi.

    Membuat aplikasi FastAPI dan menjalankannya dengan uvicorn.
    """
    # Mendapatkan pengaturan aplikasi
    settings = get_settings()

    # Jalankan server dengan uvicorn
    uvicorn.run(
        "app.app:create_app",  # Menggunakan factory function sebagai target
        factory=True,  # Memberi tahu uvicorn bahwa ini adalah factory function
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        workers=settings.server.workers,
        log_level=settings.server.log_level,
    )


if __name__ == "__main__":
    start()
