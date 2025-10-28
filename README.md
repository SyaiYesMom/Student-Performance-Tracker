# Student Performance Tracker
### Deskripsi singkat

Proyek ini adalah aplikasi sederhana untuk melacak dan merekap penilaian mahasiswa. README ini menjelaskan struktur proyek dan rincian setiap file kode.

## Struktur direktori (ringkasan)
 - `student_performance_tracker/README.md`
 - `student_performance_tracker/app.py`
 - `student_performance_tracker/out/report.md`
 - `student_performance_tracker/requirements.txt`
 - `student_performance_tracker/tracker/__init__.py`
 - `student_performance_tracker/tracker/__main__.py`
 - `student_performance_tracker/tracker/mahasiswa.py`
 - `student_performance_tracker/tracker/penilaian.py`
 - `student_performance_tracker/tracker/rekap_kelas.py`
 - `student_performance_tracker/tracker/report.py`
(+) plus beberapa berkas artefak environment seperti `.venv/` dan `__pycache__/` yang umumnya tidak perlu dimasukkan ke repo Git.

## Penjelasan file dan cara kerja kode
Untuk setiap file kode (ringkasan):

 > `student_performance_tracker/tracker/__main__.py`

Modul berisi fungsi yang mengikat komponen-komponen utama dan menyediakan entry point yang dapat dijalankan langsung. Terdapat blok `if __name__ == "__main__"` untuk menjalankan aplikasi secara langsung.

 > `student_performance_tracker/tracker/mahasiswa.py`

Modul ini berisi definisi kelas yang merepresentasikan entitas mahasiswa (mis. atribut: NIM, nama). Kelas ini kemungkinan menyediakan method untuk menampilkan atau memformat info mahasiswa.

 > `student_performance_tracker/tracker/penilaian.py`

Berisi class / fungsi yang menangani entitas penilaian—menyimpan nilai, mata-kuliah, bobot, dan operasi terkait (mis. validasi nilai, agregasi).

 > `student_performance_tracker/tracker/rekap_kelas.py`

Modul untuk merekap data kelas: menghitung rata-rata, distribusi nilai, menghitung jumlah lulus/gagal, dan menyusun rekap per-kelas atau per-mata-kuliah.

 > `student_performance_tracker/tracker/report.py`

Bertugas membuat laporan akhir (mis. Markdown/HTML/text) dari hasil rekap; kemungkinan menulis ke folder `out/` seperti `out/report.md`.

 > `student_performance_tracker/app.py`

File titik masuk (entry script) tingkat atas yang memanggil modul tracker, memuat konfigurasi, dan menjalankan proses penuh (load data → proses → generate report).

 > `student_performance_tracker/out/report.md`

Contoh output laporan yang dihasilkan oleh program — berguna sebagai referensi format output.

 > `student_performance_tracker/requirements.txt`

Daftar dependensi Python yang dibutuhkan oleh proyek (paket pihak ketiga). Instal dengan `pip install -r requirements.txt`.

  > Catatan: README juga menekankan agar direktori virtual environment (`.venv`, 
  > `venv`) dan `__pycache__` diabaikan dalam repo (tambahkan ke `.gitignore`).

## Cara menjalankan (ringkasan)

1. Buat virtual environment dan aktifkan:
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Linux / macOS
   # atau
   .venv\Scripts\activate        # Windows
   ```
2. Instal dependensi:
   ```bash
   pip install -r student_performance_tracker/requirements.txt
   ```
3. Jalankan modul utama (contoh; sesuaikan jika modul entry berbeda):
   ```bash
   python student_performance_tracker/app.py
   # atau bila ada __main__.py
   python -m student_performance_tracker.tracker
   ```
