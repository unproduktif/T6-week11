# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : (Isi Kelas)

from PySide6.QtCore import QObject, Signal


class Worker(QObject):

    finished = Signal(object)
    error = Signal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))