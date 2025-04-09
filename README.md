# Exa Manager

Addon untuk aplikasi Otomax untuk mengatur dan mengelola update produk secara otomatis.

## Fitur Utama

- Update harga produk otomatis dari multi supplier
- Open/close produk secara otomatis berdasarkan kondisi yang ditentukan

## Teknologi

- Python 3.12+
- SQLAlchemy dan SQLModel untuk ORM
- FastAPI untuk REST API
- SQLite sebagai database lokal
- Integrasi dengan SQL Server (Otomax)

## Penggunaan

1. Setup virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Untuk Linux/Mac
   # atau
   .venv\Scripts\activate  # Untuk Windows
   ```

2. Install dependencies:

   ```bash
   pip install -e .
   ```

3. Jalankan aplikasi:

   ```bash
   exa-manager
   ```

## Konfigurasi

Aplikasi menggunakan file `config.ini` untuk konfigurasi. File ini akan dibuat otomatis dengan nilai default saat aplikasi pertama kali dijalankan.

Bagian konfigurasi:

- `api`: Pengaturan FastAPI dan server
- `database`: Koneksi ke SQLite dan SQL Server
- `logging`: Level log, format, dan rotasi file
