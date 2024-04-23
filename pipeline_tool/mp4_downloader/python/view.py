from PySide2.QtWidgets import *


class DownLoadMainView(QWidget):
    def __init__(self):
        super().__init__()
        button_style = """
        QPushButton{
            width: 70px; height: 30px;
            background-color: rgb(40, 40, 40);
            color: rgb(225, 225, 225)        
        }
        QPushButton:hover{
            background-color: rgb(70, 70, 70);        
        }
        QPushButton:pressed{
            background-color: rgb(30, 30, 30);
        }
        """
        self.path_line_edit = QLineEdit()
        self.path_line_edit.setStyleSheet("background-color: rgb(90, 90, 90);")
        self.path_line_edit.setFixedSize(350, 35)
        self.browse_button = QPushButton('Browse')
        self.browse_button.setStyleSheet(button_style)
        self.path_hbox_layout = QHBoxLayout()

        self.ok_button = QPushButton('OK')
        self.ok_button.setStyleSheet(button_style)
        self.cancel_button = QPushButton('cancel')
        self.cancel_button.setStyleSheet(button_style)
        self.user_controller_btn_hbox_layout = QHBoxLayout()

        self.main_vbox_layout = QVBoxLayout()
        widget_default_style = """
        QWidget{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: 11pt\"Courier New\";
            background-color: rgb(45, 45, 45);
            color: rgb(225, 225, 225)
        }
        """
        self.setStyleSheet(widget_default_style)

    def main_ui(self):
        self.path_line_edit.setPlaceholderText("Select the save folder")

        self.path_hbox_layout.addWidget(self.path_line_edit)
        self.path_hbox_layout.addWidget(self.browse_button)
        self.main_vbox_layout.addLayout(self.path_hbox_layout)

        # self.browse_button.clicked.connect(self.test_browse_clicked)

        self.user_controller_btn_hbox_layout.addWidget(self.ok_button)
        self.user_controller_btn_hbox_layout.addWidget(self.cancel_button)
        self.main_vbox_layout.addLayout(self.user_controller_btn_hbox_layout)

        # self.ok_button.clicked.connect(self.test_ok_clicked)
        # self.cancel_button.clicked.connect(self.test_cancel_clicked)

        self.setLayout(self.main_vbox_layout)

    @staticmethod
    def test_browse_clicked():
        print("find the saved directory")

    @staticmethod
    def test_ok_clicked():
        print("mp4 save")

    @staticmethod
    def test_cancel_clicked():
        print("end to find directory")


class BrowseDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        op = self.Options()
        op |= self.DontUseNativeDialog
        op |= self.ShowDirsOnly
        op = self.getExistingDirectory(None, "Select Directory", "", options=op)
        self.option = op


def main():
    app = QApplication()
    test_ui = DownLoadMainView()
    test_ui.main_ui()
    window = QMainWindow()
    window.setCentralWidget(test_ui)
    window.setWindowTitle('Mp4 Downloader')
    window.setFixedSize(500, 150)
    window.setStyleSheet("background-color: rgb(50, 50, 50);")
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
