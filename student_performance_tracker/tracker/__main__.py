import sys


def _run():
    try:
        # Jalankan CLI yang sudah ada di app.py
        from app import main as app_main
        app_main()
    except Exception as e:
        print(f"! Gagal menjalankan tracker sebagai modul: {e}")
        sys.exit(1)


if __name__ == "__main__":
    _run()


