class Penilaian:
    """Menyimpan komponen nilai dan menghitung nilai akhir berbobot.

    Bobot default: quiz 15%, tugas 25%, uts 25%, uas 35%.
    """
    def __init__(self, quiz=0, tugas=0, uts=0, uas=0):
        self._quiz = 0.0
        self._tugas = 0.0
        self._uts = 0.0
        self._uas = 0.0
        self.quiz = quiz
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def _validate(self, v):
        if v is None:
            raise ValueError("nilai tidak boleh None")
        v = float(v)
        if v < 0 or v > 100:
            raise ValueError("nilai harus 0..100")
        return round(v, 2)

    @property
    def quiz(self): return self._quiz
    @quiz.setter
    def quiz(self, v): self._quiz = self._validate(v)

    @property
    def tugas(self): return self._tugas
    @tugas.setter
    def tugas(self, v): self._tugas = self._validate(v)

    @property
    def uts(self): return self._uts
    @uts.setter
    def uts(self, v): self._uts = self._validate(v)

    @property
    def uas(self): return self._uas
    @uas.setter
    def uas(self, v): self._uas = self._validate(v)

    def nilai_akhir(self, w_quiz=0.15, w_tugas=0.25, w_uts=0.25, w_uas=0.35):
        skor = (
            self.quiz * w_quiz +
            self.tugas * w_tugas +
            self.uts * w_uts +
            self.uas * w_uas
        )
        return round(skor, 2)

    def __repr__(self):
        return "<Penilaian q={} t={} uts={} uas={}>".format(self.quiz, self.tugas, self.uts, self.uas)
