# Minimal CLI controller for student_performance_tracker
import csv
from pathlib import Path
try:
    from tracker import RekapKelas, Mahasiswa, Penilaian
    from tracker import build_markdown_report, save_text, letter_grade, build_html_report
except Exception:
    # allow running within different import contexts
    from tracker.rekap_kelas import RekapKelas
    from tracker.mahasiswa import Mahasiswa
    from tracker.penilaian import Penilaian
    from tracker.report import build_markdown_report, save_text, letter_grade, build_html_report

DATA_DIR = Path("data")
OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

def load_csv(path):
    p = Path(path)
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

# --- Helpers untuk read/write CSV dan operasi per baris ---
ATT_HEADERS = ["student_id", "name", "week1", "week2", "week3", "week4", "week5"]
GRD_HEADERS = ["student_id", "name", "quiz", "assignment", "mid", "final"]

def _save_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline='' agar kompatibel Windows tanpa baris kosong ekstra
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            # pastikan hanya kolom yang terdaftar yang ditulis
            w.writerow({k: r.get(k, "") for k in fieldnames})

def _calc_attendance_percent(row: dict) -> float:
    weeks = [k for k in row.keys() if k.startswith("week")]
    if not weeks:
        return 0.0
    total = len(weeks)
    hadir = 0
    for w in weeks:
        val = (row.get(w, "") or "").strip()
        if val != "":
            try:
                hadir += int(float(val))
            except Exception:
                hadir += 0
    return round(hadir / total * 100.0, 2)

def append_student_to_csvs(nim: str, nama: str):
    att_path = DATA_DIR / "attendance.csv"
    grd_path = DATA_DIR / "grades.csv"

    # Attendance
    if att_path.exists():
        att_rows = load_csv(att_path)
    else:
        att_rows = []
    if not any(r.get("student_id") == nim for r in att_rows):
        att_rows.append({
            "student_id": nim,
            "name": nama,
            "week1": "0", "week2": "0", "week3": "0", "week4": "0", "week5": "0",
        })
        _save_csv(att_path, ATT_HEADERS, att_rows)

    # Grades
    if grd_path.exists():
        grd_rows = load_csv(grd_path)
    else:
        grd_rows = []
    if not any(r.get("student_id") == nim for r in grd_rows):
        grd_rows.append({
            "student_id": nim,
            "name": nama,
            "quiz": "0", "assignment": "0", "mid": "0", "final": "0",
        })
        _save_csv(grd_path, GRD_HEADERS, grd_rows)

def update_attendance_weeks(nim: str, weeks_update: dict):
    """weeks_update berisi kunci week1..week5 dengan nilai '0'/'1' atau ''"""
    att_path = DATA_DIR / "attendance.csv"
    if not att_path.exists():
        raise FileNotFoundError("attendance.csv tidak ditemukan")
    rows = load_csv(att_path)
    found = False
    for r in rows:
        if r.get("student_id") == nim:
            found = True
            # pastikan semua week1..week5 ada
            for i in range(1, 6):
                key = f"week{i}"
                if key in weeks_update and weeks_update[key] is not None:
                    val = str(weeks_update[key]).strip()
                    r[key] = "1" if val == "1" else ("0" if val == "0" else (r.get(key, "") or ""))
            break
    if not found:
        raise KeyError("NIM tidak ditemukan di attendance.csv")
    _save_csv(att_path, ATT_HEADERS, rows)
    return rows

def update_grades_for_student(nim: str, quiz=None, assignment=None, mid=None, final=None, fallback_name: str = ""):
    grd_path = DATA_DIR / "grades.csv"
    rows = load_csv(grd_path) if grd_path.exists() else []
    found = False
    for r in rows:
        if r.get("student_id") == nim:
            found = True
            if quiz is not None: r["quiz"] = str(float(quiz))
            if assignment is not None: r["assignment"] = str(float(assignment))
            if mid is not None: r["mid"] = str(float(mid))
            if final is not None: r["final"] = str(float(final))
            if not r.get("name"): r["name"] = fallback_name
            break
    if not found:
        # jika belum ada, tambahkan baris baru (nilai None -> 0)
        rows.append({
            "student_id": nim,
            "name": fallback_name,
            "quiz": str(float(quiz or 0)),
            "assignment": str(float(assignment or 0)),
            "mid": str(float(mid or 0)),
            "final": str(float(final or 0)),
        })
    _save_csv(grd_path, GRD_HEADERS, rows)
    return rows

def _print_table_from_rows(headers, rows):
    # filter baris kosong total
    filtered = []
    for r in rows:
        if r is None:
            continue
        values = [str(r.get(h, "") or "").strip() for h in headers]
        if any(v != "" for v in values):
            filtered.append(dict(zip(headers, values)))
    rows = filtered
    if not rows:
        print("(tidak ada data)")
        return
    widths = [len(h) for h in headers]
    for r in rows:
        for i, h in enumerate(headers):
            widths[i] = max(widths[i], len(str(r.get(h, ""))))
    def _fmt_row(vals):
        return " | ".join("{:<" + str(widths[i]) + "}" for i in range(len(vals))).format(*vals)
    print()
    print(_fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(_fmt_row([str(r.get(h, "")) for h in headers]))
    print()

def load_attendance_into_rekap(rekap: RekapKelas, att_path: Path):
    att = load_csv(att_path)
    for row in att:
        nim = row.get("student_id"); nama = row.get("name")
        if nim and nama:
            if nim not in rekap._by_nim:
                rekap.tambah_mahasiswa(Mahasiswa(nim, nama))
            rekap.set_hadir(nim, _calc_attendance_percent(row))

def load_grades_into_rekap(rekap: RekapKelas, grd_path: Path):
    grd = load_csv(grd_path)
    for g in grd:
        nim = g.get("student_id"); nama = g.get("name")
        if not nim:
            continue
        if nim not in rekap._by_nim:
            rekap.tambah_mahasiswa(Mahasiswa(nim, nama or nim))
        rekap.set_penilaian(
            nim,
            quiz=float(g.get("quiz", 0) or 0),
            tugas=float(g.get("assignment", 0) or 0),
            uts=float(g.get("mid", 0) or 0),
            uas=float(g.get("final", 0) or 0),
        )

def generate_and_save_report(rekap: RekapKelas) -> Path:
    records = rekap.export_for_report()
    md = build_markdown_report(records)
    out_path = OUT_DIR / "report.md"
    save_text(out_path, md)
    return out_path

def bootstrap_from_csv(rekap, att_path, grd_path):
    att = load_csv(att_path)
    grd = load_csv(grd_path)
    # buat Mahasiswa dari attendance
    for row in att:
        m = Mahasiswa(row["student_id"], row["name"])
        rekap.tambah_mahasiswa(m)
        # hitung hadir%
        weeks = [k for k in row.keys() if k.startswith("week")]
        if weeks:
            total = len(weeks)
            hadir = 0
            for w in weeks:
                val = row[w].strip()
                if val != "":
                    hadir += int(val)
            persen = round(hadir / total * 100.0, 2)
            rekap.set_hadir(m.nim, persen)

    # isi nilai dari grades
    by_nim = {g["student_id"]: g for g in grd}
    for nim in list(rekap._by_nim.keys()):
        g = by_nim.get(nim)
        if g:
            rekap.set_penilaian(
                nim,
                quiz=float(g.get("quiz", 0) or 0),
                tugas=float(g.get("assignment", 0) or 0),
                uts=float(g.get("mid", 0) or 0),
                uas=float(g.get("final", 0) or 0),
            )

def tampilkan_rekap(rows):
    print("\nNIM        | Nama   | Hadir% | Akhir | Pred")
    print("--------------------------------------------")
    for r in rows:
        print("{:<10} | {:<6} | {:>6.2f} | {:>5.2f} | {}".format(
            r['nim'], r['nama'], r['hadir'], r['akhir'], r['predikat']
        ))
    print()

def main(auto_bootstrap=True):
    r = RekapKelas()
    if auto_bootstrap:
        att_path = DATA_DIR / "attendance.csv"
        grd_path = DATA_DIR / "grades.csv"
        if att_path.exists() and grd_path.exists():
            bootstrap_from_csv(r, att_path, grd_path)
    while True:
        print("=== Student Performance Tracker ===")
        print("1) Muat data dari CSV")
        print("2) Tambah mahasiswa")
        print("3) Ubah presensi")
        print("4) Ubah nilai")
        print("5) Lihat rekap")
        print("6) Simpan laporan Markdown")
        print("7) Keluar")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            try:
                print("Muat data dari mana?")
                print("1) attendance.csv")
                print("2) grades.csv")
                sub = input("Pilih: ").strip()
                if sub == "1":
                    att_path = DATA_DIR / "attendance.csv"
                    if not att_path.exists():
                        print("!File attendance.csv tidak ditemukan.")
                    else:
                        load_attendance_into_rekap(r, att_path)
                        print("Data attendance dimuat.")
                        try:
                            att_rows = load_csv(att_path)
                            _print_table_from_rows(ATT_HEADERS, att_rows)
                        except Exception as e:
                            print(f"!Gagal menampilkan attendance: {e}")
                elif sub == "2":
                    grd_path = DATA_DIR / "grades.csv"
                    if not grd_path.exists():
                        print("!File grades.csv tidak ditemukan.")
                    else:
                        load_grades_into_rekap(r, grd_path)
                        print("Data grades dimuat.")
                        try:
                            grd_rows = load_csv(grd_path)
                            _print_table_from_rows(GRD_HEADERS, grd_rows)
                        except Exception as e:
                            print(f"!Gagal menampilkan grades: {e}")
                else:
                    print("!Pilihan tidak dikenali.")
            except Exception as e:
                print(f"!Gagal memuat CSV: {e}")

        elif pilih == "2":
            try:
                nim = input("Masukkan NIM: ").strip()
                nama = input("Masukkan Nama: ").strip()
                if not nim or not nama:
                    print("!NIM dan Nama wajib diisi")
                else:
                    r.tambah_mahasiswa(Mahasiswa(nim, nama))
                    # simpan juga ke kedua CSV
                    append_student_to_csvs(nim, nama)
                    out_path = generate_and_save_report(r)
                    print(f"Mahasiswa ditambahkan dan disimpan ke CSV. Laporan tersimpan: {out_path}")
            except Exception as e:
                print(f"!Gagal tambah mahasiswa: {e}")

        elif pilih == "3":
            try:
                nim = input("NIM: ").strip()
                def _wk(prompt):
                    s = input(prompt).strip()
                    return "1" if s == "1" else "0"
                w1 = _wk("week 1 (0/1): ")
                w2 = _wk("week 2 (0/1): ")
                w3 = _wk("week 3 (0/1): ")
                w4 = _wk("week 4 (0/1): ")
                w5 = _wk("week 5 (0/1): ")
                rows = update_attendance_weeks(nim, {
                    "week1": w1, "week2": w2, "week3": w3, "week4": w4, "week5": w5
                })
                # update hadir% di memori
                row = next((x for x in rows if x.get("student_id") == nim), None)
                if row is not None:
                    r.set_hadir(nim, _calc_attendance_percent(row))
                out_path = generate_and_save_report(r)
                print(f"Presensi mingguan diperbarui dan disimpan ke CSV. Laporan tersimpan: {out_path}")
            except Exception as e:
                print(f"!Gagal ubah presensi: {e}")

        elif pilih == "4":
            try:
                nim = input("NIM: ").strip()
                def _num(prompt):
                    s = input(prompt).strip()
                    return float(s) if s else None
                qz = _num("Nilai Quiz (kosongkan jika tidak ubah): ")
                tg = _num("Nilai Tugas (kosongkan jika tidak ubah): ")
                ut = _num("Nilai UTS (kosongkan jika tidak ubah): ")
                ua = _num("Nilai UAS (kosongkan jika tidak ubah): ")
                r.set_penilaian(nim, quiz=qz, tugas=tg, uts=ut, uas=ua)
                # persist ke grades.csv
                nama_fallback = r._by_nim.get(nim, {}).get('mhs').nama if nim in r._by_nim else ""
                update_grades_for_student(nim, qz, tg, ut, ua, fallback_name=nama_fallback)
                out_path = generate_and_save_report(r)
                print(f"Nilai diperbarui dan disimpan ke CSV. Laporan tersimpan: {out_path}")
            except Exception as e:
                print(f"!Gagal ubah nilai: {e}")

        elif pilih == "5":
            try:
                print("Lihat rekap apa?")
                print("1) Semua mahasiswa")
                print("2) Hanya nilai akhir < 70")
                sub = input("Pilih: ").strip()
                rows = r.rekap()
                if sub == "2":
                    rows = [x for x in rows if float(x.get('akhir', 0)) < 70.0]
                tampilkan_rekap(rows)
            except Exception as e:
                print(f"!Gagal tampilkan rekap: {e}")

        elif pilih == "6":
            try:
                records = r.export_for_report()
                # Simpan Markdown
                md = build_markdown_report(records)
                out_md = OUT_DIR / "report.md"
                save_text(out_md, md)
                # Simpan HTML berwarna
                html = build_html_report(records)
                out_html = OUT_DIR / "report.html"
                save_text(out_html, html)
                print(f"Laporan disimpan ke {out_md} dan {out_html}")
            except Exception as e:
                print(f"!Gagal simpan laporan: {e}")

        elif pilih == "7":
            print("Keluar. Terima kasih!")
            return

        else:
            print("Pilihan tidak dikenali.")

    # produce report automatically
    records = r.export_for_report()
    md = build_markdown_report(records)
    out_path = OUT_DIR / "report.md"
    save_text(out_path, md)
    print("\n✅  Laporan tersimpan di {}\n".format(out_path))
    # also print a simple terminal rekap
    for row in r.rekap():
        print(row) 

if __name__ == "__main__":
    main()


