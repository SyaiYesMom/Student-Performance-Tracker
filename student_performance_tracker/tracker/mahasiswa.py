class Mahasiswa:
    """Representasi Mahasiswa dengan enkapsulasi untuk persentase hadir.

    Attributes:
        nim: string NIM mahasiswa
        nama: string nama mahasiswa
        _hadir_persen: float internal (0..100)
    """
    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0.0

    @property
    def hadir_persen(self):
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, v):
        if v is None:
            raise ValueError("hadir_persen tidak boleh None")
        v = float(v)
        if v < 0 or v > 100:
            raise ValueError("hadir_persen harus 0..100")
        self._hadir_persen = round(v, 2)

    def info(self):
        return "{} - {} (Hadir: {:.2f}%)".format(self.nim, self.nama, self.hadir_persen)

    def __repr__(self):
        return "<Mahasiswa {} {} hadir={:.2f}%>".format(self.nim, self.nama, self.hadir_persen)
