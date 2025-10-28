# student_performance_tracker

Paket `tracker` untuk mengelola data mahasiswa, menghitung nilai akhir, dan membuat laporan Markdown.

## Cara menjalankan
Pastikan kamu berada di folder `student_performance_tracker`, lalu jalankan:

```bash
python app.py
```

Laporan akan disimpan di `out/report.md`.

Atau jalankan langsung paket sebagai modul (entry point):

```bash
python -m tracker
```

## Struktur
- tracker/: paket berisi model dan util report
- data/: berisi contoh CSV attendance.csv & grades.csv
- out/: hasil report.md
