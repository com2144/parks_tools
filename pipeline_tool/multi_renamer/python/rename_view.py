from PySide2.QtWidgets import *
from rename_model import *
import os


class RenameMainView(QWidget):
    def __init__(self):
        super().__init__()
        browse_style = """
        QPushButton{
            width: 70px; height: 30px;
            border: 1px solid grey;
            border-radius: 4px;
            font: 11pt\"Courier New\";
            background-color: rgb(60, 60, 60);
            color: rgb(225, 225, 225)   
        }
       QPushButton:hover {
            background-color: rgb(80, 80, 80);
        }                  
       QPushButton:pressed {
            background-color: rgb(40, 40, 40);
       }
        """
        line_style = """
        QLineEdit{
            width: 70px; height: 30px;
            border: 1px solid grey;
            border-radius: 4px;
            font: 10pt\"Courier New\";
            background-color: rgb(225, 225, 225);
            color: rgb(0, 0, 0)
        }        
        """
        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet(line_style)
        self.browse_button = QPushButton("Browse")
        self.browse_button.setStyleSheet(browse_style)
        self.path_hbox_layout = QHBoxLayout()

        self.use_button_hbox_layout = QHBoxLayout()
        self.plus_button = QPushButton("+")
        self.plus_button.setStyleSheet(browse_style)
        self.minus_button = QPushButton("-")
        self.minus_button.setStyleSheet(browse_style)

        self.new_name_vbox_layout = QVBoxLayout()
        self.widget_vbox_layout = QWidget()
        self.scroll_edit_layout = QScrollArea()

        self.rename_button = QPushButton("Rename")
        self.rename_button.setStyleSheet(browse_style)
        self.rename_button_hbox_layout = QHBoxLayout()

        self.main_vbox_layuout = QVBoxLayout()


class FileListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Files in Directory")
        self.list_widget = QListWidget(self)
        self.dialog_layout = QVBoxLayout()
        self.dialog_layout.addWidget(self.list_widget)
        self.setLayout(self.dialog_layout)
        self.setModal(False)
        center_point = QDesktopWidget().availableGeometry().center()
        new_x = center_point.x() + 220
        new_y = center_point.y() - 153
        self.setFixedSize(300, 210)
        self.move(new_x, new_y)

    def set_files(self, file_list):
        for file in file_list:
            file_name, file_ext = os.path.splitext(file)
            if file_ext != '':
                self.list_widget.addItem(file_name)
                list_widget_style = """
                QListWidget{
                    font: 10pt\"Courier New\";
                    color: rgb(225, 225, 225)
                }
                """
                self.list_widget.setStyleSheet(list_widget_style)


class BrowseDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        ow = self.Options()
        ow |= self.DontUseNativeDialog
        ow |= self.ShowDirsOnly
        ow = self.getExistingDirectory(None, "Select Directory", "", options=ow)
        self.option = ow
        # |=를 사용하는 이유 -> QFileDialog의 기능을 overwrite하지 않고 기능을 더해주는 의미


class RenameNewPathView(QWidget):
    def __init__(self):
        super().__init__()
        line_style = """
        QLineEdit{
            border: 1px solid grey;
            border-radius: 4px;
            font: 10pt\"Courier New\";
            background-color: rgb(225, 225, 225);
            color: rgb(0, 0, 0)
        }        
        """
        self.old_edit = QLineEdit()
        self.old_edit.setStyleSheet(line_style)
        self.new_edit = QLineEdit()
        self.new_edit.setStyleSheet(line_style)
        self.new_name_layout = QHBoxLayout()
        self.widget_hbox_layout = QWidget()


class TestUi:
    def __init__(self):
        super().__init__()
        self.main_view = RenameMainView()
        self.newname_view = RenameNewPathView()

        self.test_main_ui()

    def test_main_ui(self):
        self.main_view.line_edit.setPlaceholderText("Enter a file path")

        self.main_view.path_hbox_layout.addWidget(self.main_view.line_edit)
        self.main_view.path_hbox_layout.addWidget(self.main_view.browse_button)
        self.main_view.main_vbox_layuout.addLayout(self.main_view.path_hbox_layout)

        self.main_view.browse_button.clicked.connect(self.feature_browse_button_clicked)

        self.main_view.use_button_hbox_layout.addWidget(self.main_view.plus_button)
        self.main_view.use_button_hbox_layout.addWidget(self.main_view.minus_button)
        self.main_view.main_vbox_layuout.addLayout(self.main_view.use_button_hbox_layout)

        self.main_view.plus_button.clicked.connect(self.feature_plus_button_clicked)
        self.main_view.minus_button.clicked.connect(self.feature_minus_button_clicked)
        self.main_view.rename_button.clicked.connect(self.feature_rename_button_clicked)

        self.newname_view.new_name_layout.addWidget(self.newname_view.old_edit)
        self.newname_view.new_name_layout.addWidget(self.newname_view.new_edit)
        self.newname_view.widget_hbox_layout.setLayout(self.newname_view.new_name_layout)

        self.main_view.new_name_vbox_layout.setSpacing(0)
        self.main_view.new_name_vbox_layout.addWidget(self.newname_view.widget_hbox_layout)
        self.main_view.widget_vbox_layout.setLayout(self.main_view.new_name_vbox_layout)

        self.main_view.scroll_edit_layout.setWidgetResizable(True)
        self.main_view.scroll_edit_layout.setWidget(self.main_view.widget_vbox_layout)
        self.main_view.main_vbox_layuout.addWidget(self.main_view.scroll_edit_layout)

        self.main_view.rename_button_hbox_layout.addWidget(self.main_view.rename_button)
        self.main_view.main_vbox_layuout.addLayout(self.main_view.rename_button_hbox_layout)

        self.main_view.setLayout(self.main_view.main_vbox_layuout)

    @staticmethod
    def feature_browse_button_clicked():
        print('Searching files in directory')

    @staticmethod
    def feature_plus_button_clicked():
        print("Add old_text and new_text as QLineEdit")

    @staticmethod
    def feature_minus_button_clicked():
        print("Subtract old_text_and new_text QLineEdit")

    @staticmethod
    def feature_rename_button_clicked():
        print("Renaming function")


def main():
    app = QApplication()
    controller = TestUi()
    window = QMainWindow()
    window.setCentralWidget(controller.main_view)
    window.setWindowTitle("Renamer")
    window.setFixedSize(400, 210)
    window.setStyleSheet("background-color: rgb(50, 50, 50);")
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
