from PySide2.QtWidgets import *
from PySide2.QtGui import *

class PipelineSetupView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Setup')

        layout = QVBoxLayout()
        self.setLayout(layout)

        browse_line_layout = QHBoxLayout()

        self.browse_line_edit = QLineEdit()
        self.browse_line_edit.setPlaceholderText("Enter the root path")
        browse_line_layout.addWidget(self.browse_line_edit)

        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_clicked)
        browse_line_layout.addWidget(self.browse_button)

        layout.addLayout(browse_line_layout)

        project_line_layout = QHBoxLayout()

        self.project_line_edit = QLineEdit()
        self.project_line_edit.setPlaceholderText("Enter the Project name")
        project_line_layout.addWidget(self.project_line_edit)

        self.ext_combo_box = QComboBox()
        ext_list = ['hip', 'hiplc', 'hipnc']
        for ext in ext_list:
            self.ext_combo_box.addItem(ext)
        project_line_layout.addWidget(self.ext_combo_box)

        layout.addLayout(project_line_layout)

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
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        self.move(x, y)


    @staticmethod
    def browse_clicked():
        print('select root path directory')

    @staticmethod
    def ok_clicked():
        print('project set')

    @staticmethod
    def cancel_clicked(self):
        print('work cancel')
    
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
        ow = self.Options()
        ow |= self.DontUseNativeDialog
        ow |= self.ShowDirsOnly
        ow = self.getExistingDirectory(None, "Select Directory", "", options=ow)
        self.option = ow


if __name__ == '__main__':
    app = QApplication()
    window = PipelineSetupView()
    window.show()
    app.exec_()