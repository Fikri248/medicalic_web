# Selenium Automation Tests - Apotek Medicalic

Repositori ini memuat skrip otomatisasi *End-to-End* (E2E) UI Testing menggunakan Python Selenium WebDriver untuk proyek aplikasi web Apotek Medicalic. Paket pengujian ini disusun untuk mendukung laporan akhir mata kuliah Pengujian dan Implementasi Sistem.

## Persyaratan
- Python 3.10+
- Google Chrome Browser
- PIP (Python Package Manager)

## Instalasi
1. Buka terminal di direktori `selenium-tests/`.
2. Jalankan perintah instalasi pustaka:
   ```bash
   pip install -r requirements.txt
   ```
3. Salin `.env.example` ke `.env`:
   ```bash
   copy .env.example .env   # (Untuk Windows)
   cp .env.example .env     # (Untuk Linux/Mac)
   ```
4. Sesuaikan variabel di `.env` (pastikan `BASE_URL`, email admin, dan password sudah tepat).

## Cara Menjalankan Pengujian

Menjalankan seluruh file test (Auth, Obat, Transaksi, Laporan):
```bash
pytest
```

Menjalankan file test tertentu dengan verbosity tinggi (untuk detail):
```bash
pytest -v tests/test_transaksi.py
```

Menjalankan test dengan log output cetak:
```bash
pytest -s
```

## Struktur Test
- `test_auth.py`: Uji coba login sukses, login gagal, proteksi dashboard tanpa login, dan logout.
- `test_obat.py`: Uji coba penambahan data obat (menghindari merusak data riil dengan memberi prefix dummy `Obat Selenium {Timestamp}`) dan pencarian data.
- `test_transaksi.py`: Uji coba alur transaksi normal dan uji validasi pencegahan transaksi jika jumlah permintaan melebihi stok sisa obat.
- `test_laporan.py`: Uji aksesibilitas tautan ekspor laporan.
