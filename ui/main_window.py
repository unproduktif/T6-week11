# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : (Isi Kelas)

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QTextEdit,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
    QToolBar,
    QSplitter
)

from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QColor

from api.api_service import ApiService
from ui.post_dialog import PostDialog
from ui.worker import Worker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.selected_post_id = None

        self.setWindowTitle("Post Manager")
        self.resize(1300, 700)

        self.setup_toolbar()
        self.setup_ui()
        self.load_posts()

    def setup_toolbar(self):

        toolbar = QToolBar()
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setObjectName("btn_refresh")
        self.refresh_btn.clicked.connect(self.load_posts)

        self.add_btn = QPushButton("➕ Add")
        self.add_btn.setObjectName("btn_add")
        self.add_btn.clicked.connect(self.add_post)

        self.edit_btn = QPushButton("✏ Edit")
        self.edit_btn.setObjectName("btn_edit")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_post)

        self.delete_btn = QPushButton("🗑 Delete")
        self.delete_btn.setObjectName("btn_delete")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_post)

        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)

    def setup_ui(self):

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(18)

        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()

        title = QLabel("Post Manager REST API")
        title.setObjectName("main_title")

        subtitle = QLabel(
            "Manage posts with REST API and multi-threading"
        )
        subtitle.setObjectName("subtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        self.loading_label = QLabel("🟢 Ready")
        self.loading_label.setObjectName("loading_label")

        header_layout.addWidget(self.loading_label)
        main_layout.addLayout(header_layout)

        card_layout = QHBoxLayout()

        self.total_post_card = QLabel("Total Posts\n0")
        self.publish_card = QLabel("Published\n0")
        self.draft_card = QLabel("Draft\n0")

        for card in [
            self.total_post_card,
            self.publish_card,
            self.draft_card
        ]:
            card.setObjectName("dashboard_card")
            card.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(card)

        main_layout.addLayout(card_layout)
        splitter = QSplitter()
        splitter.setHandleWidth(0)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setMinimumHeight(520)

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Title",
            "Author",
            "Status"
        ])

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(True)

        self.table.setShowGrid(False)

        self.table.itemSelectionChanged.connect(
            self.on_row_selected
        )

        left_layout.addWidget(self.table)

        right_widget = QWidget()
        right_widget.setObjectName("detail_panel")

        right_layout = QVBoxLayout(right_widget)

        detail_title = QLabel("📄 Detail Post")
        detail_title.setObjectName("detail_title")

        right_layout.addWidget(detail_title)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)

        right_layout.addWidget(self.detail_text)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([900, 400])

        main_layout.addWidget(splitter)

    def set_loading(self, text="Loading..."):
        self.loading_label.setText(text)

        self.refresh_btn.setEnabled(False)
        self.add_btn.setEnabled(False)
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

    def stop_loading(self):
        self.loading_label.setText("Ready")

        self.refresh_btn.setEnabled(True)
        self.add_btn.setEnabled(True)

        if self.selected_post_id:
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)

    def run_thread(self, fn, callback, *args):

        thread = QThread()
        worker = Worker(fn, *args)

        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        worker.finished.connect(callback)
        worker.finished.connect(thread.quit)

        worker.error.connect(self.show_error)
        worker.error.connect(thread.quit)

        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)

        thread.start()

        self.current_thread = thread
        self.current_worker = worker

    def load_posts(self):

        self.set_loading("🔄 Loading posts...")

        self.run_thread(
            ApiService.get_posts,
            self.on_posts_loaded
        )

    def on_posts_loaded(self, data):

        self.table.setRowCount(0)

        posts = data["data"]

        published = 0
        draft = 0

        for row, post in enumerate(posts):

            self.table.insertRow(row)

            if post["status"] == "published":
                published += 1
            else:
                draft += 1

            items = [
                post["id"],
                post["title"],
                post["author"],
                post["status"]
            ]

            for col, value in enumerate(items):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(Qt.AlignCenter)

                item.setForeground(QColor("#1E293B"))

                if post["status"] == "published":
                    item.setBackground(
                        QColor("#E8FFF3")
                    )
                else:
                    item.setBackground(
                        QColor("#FFF7E8")
                    )

                self.table.setItem(row, col, item)

        self.total_post_card.setText(
            f"Total Posts\n{len(posts)}"
        )

        self.publish_card.setText(
            f"Published\n{published}"
        )

        self.draft_card.setText(
            f"Draft\n{draft}"
        )

        self.stop_loading()

    def on_row_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        self.selected_post_id = int(
            self.table.item(row, 0).text()
        )

        self.edit_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

        self.set_loading("📄 Loading detail...")

        self.run_thread(
            ApiService.get_post,
            self.show_detail,
            self.selected_post_id
        )

    def show_detail(self, data):

        post = data["data"]

        self.current_post_detail = post

        comments = post.get("comments", [])

        if post["status"] == "published":
            status_color = "#05CD99"
            status_bg = "#E8FFF3"
        else:
            status_color = "#F59E0B"
            status_bg = "#FFF7E8"

        comments_html = ""

        if comments:

            for comment in comments:
                comments_html += f"""
                <div style="
                    background:#F8FAFC;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:8px;
                    border:1px solid #E2E8F0;
                ">
                    💬 {comment['name']}
                </div>
                """

        else:

            comments_html = """
            <div style="
                color:#64748B;
                padding:10px;
            ">
                Tidak ada komentar
            </div>
            """

        detail_html = f"""
        <div style='font-family:Segoe UI; color:#1E293B;'>

            <div style='
                background:white;
                border-radius:16px;
                padding:18px;
                border:1px solid #E2E8F0;
            '>

                <div style='
                    font-size:24px;
                    font-weight:bold;
                    color:#2B3674;
                    margin-bottom:14px;
                '>
                    {post['title']}
                </div>

                <div style='margin-bottom:14px;'>

                    <span style='
                        background:{status_bg};
                        color:{status_color};
                        padding:6px 12px;
                        border-radius:12px;
                        font-size:12px;
                        font-weight:bold;
                    '>
                        {post['status']}
                    </span>

                </div>

                <table width='100%' cellspacing='8'>

                    <tr>
                        <td width='90'>
                            <b>ID</b>
                        </td>
                        <td>
                            : {post['id']}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <b>Author</b>
                        </td>
                        <td>
                            : {post['author']}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <b>Slug</b>
                        </td>
                        <td>
                            : {post['slug']}
                        </td>
                    </tr>

                </table>

            </div>

            <div style='height:16px;'></div>

            <!-- BODY -->

            <div style='
                background:white;
                border-radius:16px;
                padding:18px;
                border:1px solid #E2E8F0;
            '>

                <div style='
                    font-size:18px;
                    font-weight:bold;
                    color:#2B3674;
                    margin-bottom:12px;
                '>
                    Body Content
                </div>

                <div style='
                    line-height:1.7;
                    color:#334155;
                '>
                    {post['body']}
                </div>

            </div>

            <div style='height:16px;'></div>

            <!-- COMMENTS -->

            <div style='
                background:white;
                border-radius:16px;
                padding:18px;
                border:1px solid #E2E8F0;
            '>

                <div style='
                    font-size:18px;
                    font-weight:bold;
                    color:#2B3674;
                    margin-bottom:12px;
                '>
                    💬 Comments ({len(comments)})
                </div>

                {comments_html}

            </div>

        </div>
        """

        self.detail_text.setHtml(detail_html)

        self.stop_loading()

    def add_post(self):

        dialog = PostDialog(self)

        if dialog.exec():

            self.set_loading("➕ Menambahkan post...")

            self.run_thread(
                ApiService.create_post,
                self.on_post_created,
                dialog.get_data()
            )

    def on_post_created(self, data):

        QMessageBox.information(
            self,
            "Sukses",
            f"Post berhasil dibuat\nID: {data['data']['id']}"
        )

        self.load_posts()

    def edit_post(self):

        if not self.selected_post_id:
            return

        if not hasattr(self, "current_post_detail"):
            return

        post = self.current_post_detail

        post_data = {
            "title": post["title"],
            "body": post["body"],
            "author": post["author"],
            "slug": post["slug"],
            "status": post["status"]
        }

        dialog = PostDialog(self, post_data)

        if dialog.exec():

            self.set_loading("✏ Mengupdate post...")

            self.run_thread(
                ApiService.update_post,
                self.on_post_updated,
                self.selected_post_id,
                dialog.get_data()
            )

    def on_post_updated(self, data):

        QMessageBox.information(
            self,
            "Sukses",
            "Post berhasil diupdate"
        )

        self.load_posts()

    def delete_post(self):

        if not self.selected_post_id:
            return

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin menghapus post ini?"
        )

        if confirm == QMessageBox.Yes:

            self.set_loading("🗑 Menghapus post...")

            self.run_thread(
                ApiService.delete_post,
                self.on_post_deleted,
                self.selected_post_id
            )

    def on_post_deleted(self, data):

        QMessageBox.information(
            self,
            "Sukses",
            "Post berhasil dihapus"
        )

        self.selected_post_id = None

        self.detail_text.clear()

        self.load_posts()

    def show_error(self, message):

        self.stop_loading()

        if "422" in message:
            message = "Slug sudah digunakan"

        QMessageBox.critical(
            self,
            "Error",
            message
        )