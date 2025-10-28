from .mahasiswa import Mahasiswa
from .penilaian import Penilaian

class RekapKelas:
    """Agregator yang menyatukan Mahasiswa dan Penilaian serta util predikat."""
    def __init__(self):
        self._by_nim = {}   # nim -> {'mhs': Mahasiswa, 'nilai': Penilaian}

    def tambah_mahasiswa(self, mhs):
        if not isinstance(mhs, Mahasiswa):
            raise TypeError("tambah_mahasiswa membutuhkan objek Mahasiswa")
        if mhs.nim in self._by_nim:
            raise KeyError("NIM sudah ada: {}".format(mhs.nim))
        self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}

    def set_hadir(self, nim, persen):
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError("NIM tidak ditemukan")
        item['mhs'].hadir_persen = persen

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError("NIM tidak ditemukan")
        p = item['nilai']
        if quiz is not None: p.quiz = quiz
        if tugas is not None: p.tugas = tugas
        if uts is not None: p.uts = uts
        if uas is not None: p.uas = uas

    def predikat(self, skor):
        if skor >= 85: return "A"
        if skor >= 75: return "B"
        if skor >= 65: return "C"
        if skor >= 50: return "D"
        return "E"

    def rekap(self):
        rows = []
        for nim, d in self._by_nim.items():
            m = d['mhs']; p = d['nilai']
            akhir = p.nilai_akhir()
            rows.append({
                'nim': nim,
                'nama': m.nama,
                'hadir': m.hadir_persen,
                'akhir': akhir,
                'predikat': self.predikat(akhir),
            })
        return rows

    def export_for_report(self):
        """Kembalikan list of dict sesuai format report builder."""
        rows = []
        for nim, d in self._by_nim.items():
            m = d['mhs']; p = d['nilai']
            rows.append({
                'student_id': nim,
                'name': m.nama,
                'attendance_rate': m.hadir_persen,
                'final_score': p.nilai_akhir(),
            })
        return rows
