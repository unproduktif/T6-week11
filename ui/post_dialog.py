# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : (Isi Kelas)

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QLabel
)


class PostDialog(QDialog):

    def __init__(self, parent=None, data=None):
        super().__init__(parent)

        self.setWindowTitle("Form Post")
        self.setFixedWidth(420)

        layout = QVBoxLayout(self)

        title = QLabel("Form Post")
        title.setObjectName("dialog_title")

        layout.addWidget(title)

        form = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan title")

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Masukkan body")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Masukkan author")

        self.slug_input = QLineEdit()
        self.slug_input.setPlaceholderText("contoh: judul-post")

        self.status_input = QComboBox()
        self.status_input.addItems([
            "published",
            "draft"
        ])

        title_label = QLabel("Title")
        body_label = QLabel("Body")
        author_label = QLabel("Author")
        slug_label = QLabel("Slug")
        status_label = QLabel("Status")

        for lbl in [
            title_label,
            body_label,
            author_label,
            slug_label,
            status_label
        ]:
            lbl.setObjectName("form_label")

        form.addRow(title_label, self.title_input)
        form.addRow(body_label, self.body_input)
        form.addRow(author_label, self.author_input)
        form.addRow(slug_label, self.slug_input)
        form.addRow(status_label, self.status_input)

        layout.addLayout(form)

        self.save_btn = QPushButton("Simpan")
        self.save_btn.setObjectName("btn_save")
        self.save_btn.clicked.connect(self.validate_input)

        layout.addWidget(self.save_btn)

        if data:
            self.title_input.setText(data["title"])
            self.body_input.setText(data["body"])
            self.author_input.setText(data["author"])
            self.slug_input.setText(data["slug"])
            self.status_input.setCurrentText(data["status"])

    def validate_input(self):

        if self.title_input.text() == "":
            QMessageBox.warning(
                self,
                "Error",
                "Title wajib diisi"
            )
            return

        if self.body_input.toPlainText() == "":
            QMessageBox.warning(
                self,
                "Error",
                "Body wajib diisi"
            )
            return

        if self.author_input.text() == "":
            QMessageBox.warning(
                self,
                "Error",
                "Author wajib diisi"
            )
            return

        if self.slug_input.text() == "":
            QMessageBox.warning(
                self,
                "Error",
                "Slug wajib diisi"
            )
            return

        self.accept()

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "body": self.body_input.toPlainText(),
            "author": self.author_input.text(),
            "slug": self.slug_input.text(),
            "status": self.status_input.currentText()
        }