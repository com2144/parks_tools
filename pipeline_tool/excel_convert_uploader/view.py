from PySide2.QtWidgets import *
from PySide2.QtGui import *


class LoadConvertView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Excel Converter')
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        browse_line_layout = QHBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter a xlsx file")
        browse_line_layout.addWidget(self.line_edit)

        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_clicked)
        browse_line_layout.addWidget(self.browse_button)

        layout.addLayout(browse_line_layout)

        self.combo_box = QComboBox()
        layout.addWidget(self.combo_box)

        self.label = QLabel('Converting Project: ')
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()

        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self.ok_clicked)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_clicked)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.center_on_screen()

    def center_on_screen(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 1.6
        y = (screen_geometry.height() - self.height()) // 1.3

        self.move(x, y)

    @staticmethod
    def ok_clicked():
        print('convert start')

    def cancel_clicked(self):
        print('work cancel')
        self.close()

    @staticmethod
    def browse_clicked():
        print('find xlsx file')

    @staticmethod
    def message_box(message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(f"{message}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


class BrowseDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setDirectory('/home/west/')
        self.file_name, _ = self.getOpenFileName(self,
                                                 "Select File",
                                                 filter="Excel Files (*.xlsx);;CSV Files (*.csv)")


if __name__ == '__main__':
    app = QApplication()
    window = LoadConvertView()
    window.show()
    app.exec_()
