from PySide2.QtWidgets import *
from rename_model import *
from rename_view import *
import os


class RenamePathController:
    def __init__(self):
        self.main_model = RenameMainModel()
        self.main_view = RenameMainView()
        self.newname_model = RenameNewPathModel()
        self.newname_view = RenameNewPathView()

        self.dir_path = self.main_model.path
        self.action_count = 0
        self.browse_count = False

        self.file_list_dialog = None

        self.deleted_old_text_widget = []
        self.deleted_new_text_widget = []
        self.deleted_rename_hbox = []
        self.deleted_rename_hwidget = []

        self.file_count = 0

        self.path_ui()

    def path_ui(self):
        self.main_view.line_edit.setPlaceholderText("Enter a file path")

        self.main_view.path_hbox_layout.addWidget(self.main_view.line_edit)
        self.main_view.path_hbox_layout.addWidget(self.main_view.browse_button)
        self.main_view.main_vbox_layuout.addLayout(self.main_view.path_hbox_layout)

        self.main_view.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.main_view.use_button_hbox_layout.addWidget(self.main_view.plus_button)
        self.main_view.use_button_hbox_layout.addWidget(self.main_view.minus_button)
        self.main_view.main_vbox_layuout.addLayout(self.main_view.use_button_hbox_layout)

        self.main_view.plus_button.clicked.connect(self.on_plus_button_clicked)
        self.main_view.minus_button.clicked.connect(self.on_minus_button_clicked)
        self.main_view.rename_button.clicked.connect(self.on_rename_button_clicked)

        self.newname_view.new_name_layout.addWidget(self.newname_view.old_edit)
        self.newname_view.new_name_layout.addWidget(self.newname_view.new_edit)
        self.newname_view.widget_hbox_layout.setLayout(self.newname_view.new_name_layout)
        self.newname_model.old_text_widget.append(self.newname_view.old_edit)
        self.newname_model.new_text_widget.append(self.newname_view.new_edit)
        self.newname_model.rename_hbox.append(self.newname_view.new_name_layout)
        self.newname_model.rename_hwidget.append(self.newname_view.widget_hbox_layout)

        self.main_view.new_name_vbox_layout.setSpacing(0)
        self.main_view.new_name_vbox_layout.addWidget(self.newname_view.widget_hbox_layout)
        self.main_view.widget_vbox_layout.setLayout(self.main_view.new_name_vbox_layout)

        self.main_view.scroll_edit_layout.setWidgetResizable(True)
        self.main_view.scroll_edit_layout.setWidget(self.main_view.widget_vbox_layout)
        self.main_view.main_vbox_layuout.addWidget(self.main_view.scroll_edit_layout)

        self.main_view.rename_button_hbox_layout.addWidget(self.main_view.rename_button)
        self.main_view.main_vbox_layuout.addLayout(self.main_view.rename_button_hbox_layout)

        self.main_view.setLayout(self.main_view.main_vbox_layuout)

    def on_browse_button_clicked(self):
        self.browse_count = True
        self.newname_model.old_full_path = []

        if self.file_list_dialog is not None:
            self.file_list_dialog.close()

        browse_option = BrowseDialog()
        self.dir_path = browse_option.option

        if self.dir_path == '':
            self.show_warning('Choose the directory')
            self.window_all_clear()
            return

        if not self.check_files_exist(self.dir_path):
            self.show_warning("The selected directory contains no files.")
            browse_option.close()
        else:
            self.set_file_path(self.dir_path)
            self.main_view.line_edit.setText(self.dir_path)
            self.show_files_in_directory(self.dir_path)

    def show_files_in_directory(self, directory):
        file_list = os.listdir(directory)

        self.file_list_dialog = FileListDialog(self.main_view)
        self.file_list_dialog.set_files(file_list)

        self.file_list_dialog.show()
        self.file_list_dialog.finished.connect(self.on_file_list_dialog_finished)

    def on_file_list_dialog_finished(self):
        self.main_view.line_edit.setText('')
        self.file_list_dialog = None

    @staticmethod
    def check_files_exist(dir_path):
        if os.path.exists(dir_path):
            for entry in os.listdir(dir_path):
                confine_path = dir_path + '/' + entry
                _, file_ext = os.path.splitext(confine_path)
                if file_ext != '':
                    return True
            return False

    def set_file_path(self, path):
        if os.path.isdir(path):
            file_list = os.listdir(path)
        else:
            dir_path = os.path.dirname(path)
            file_list = os.listdir(dir_path)

        for index, file_name in enumerate(file_list):
            full_path = path + '/' + file_name
            if os.path.exists(full_path):
                self.newname_model.old_full_path.append(full_path)

    def on_plus_button_clicked(self):
        self.action_count += 1

        if self.action_count > 0 and self.deleted_old_text_widget and self.deleted_new_text_widget and self.deleted_rename_hbox and self.deleted_rename_hwidget:
            for i in range(self.action_count + 1):
                self.newname_model.old_text_widget.append(self.deleted_old_text_widget[i])
                self.newname_model.new_text_widget.append(self.deleted_new_text_widget[i])
                self.newname_model.rename_hbox.append(self.deleted_rename_hbox[i])
                self.newname_model.rename_hwidget.append(self.deleted_rename_hwidget[i])
        elif self.action_count > 0:
            line_style = """
            QLineEdit{
                border: 1px solid grey;
                border-radius: 4px;
                font: 10pt\"Courier New\";
                background-color: rgb(225, 225, 225);
                color: rgb(0, 0, 0)
            }        
            """
            new_old_edit = QLineEdit()
            new_old_edit.setStyleSheet(line_style)
            new_new_edit = QLineEdit()
            new_new_edit.setStyleSheet(line_style)
            new_hbox_layout = QHBoxLayout()
            new_widget_hbox_layout = QWidget()

            self.newname_model.old_text_widget.append(new_old_edit)
            self.newname_model.new_text_widget.append(new_new_edit)
            self.newname_model.rename_hbox.append(new_hbox_layout)
            self.newname_model.rename_hwidget.append(new_widget_hbox_layout)

        self.deleted_old_text_widget = []
        self.deleted_new_text_widget = []
        self.deleted_rename_hbox = []
        self.deleted_rename_hwidget = []

        for i in range(self.action_count):
            self.newname_model.rename_hbox[i + 1].addWidget(self.newname_model.old_text_widget[i + 1])
            self.newname_model.rename_hbox[i + 1].addWidget(self.newname_model.new_text_widget[i + 1])
            self.newname_model.rename_hwidget[i + 1].setLayout(self.newname_model.rename_hbox[i + 1])
            self.main_view.new_name_vbox_layout.addWidget(self.newname_model.rename_hwidget[i + 1])
        self.main_view.new_name_vbox_layout.setSpacing(0)
        self.main_view.widget_vbox_layout.setLayout(self.main_view.new_name_vbox_layout)
        self.main_view.scroll_edit_layout.setWidgetResizable(True)
        self.main_view.scroll_edit_layout.setWidget(self.main_view.widget_vbox_layout)

    def on_minus_button_clicked(self):
        if self.action_count > 0:
            if self.newname_model.old_text_widget[-1].text():
                self.newname_model.old_text_widget[-1].setText('')
                self.newname_model.new_text_widget[-1].setText('')

            self.newname_model.old_text_widget[-1].setParent(None)
            self.newname_model.new_text_widget[-1].setParent(None)

            self.newname_model.rename_hbox[-1].removeWidget(self.newname_model.old_text_widget[-1])
            self.newname_model.rename_hbox[-1].removeWidget(self.newname_model.new_text_widget[-1])
            self.main_view.new_name_vbox_layout.takeAt(self.main_view.new_name_vbox_layout.count() - 1)

            self.newname_model.old_text_widget.pop()
            self.newname_model.new_text_widget.pop()
            self.newname_model.rename_hbox.pop()
            self.newname_model.rename_hwidget.pop()

            self.action_count -= 1

    def on_rename_button_clicked(self):
        if self.browse_count:
            for old_text in self.newname_model.old_text_widget:
                self.newname_model.old_file_user_name.append(old_text.text())
            for new_text in self.newname_model.new_text_widget:
                self.newname_model.new_file_user_name.append(new_text.text())

            for i in range(self.action_count + 1):
                old_name = self.newname_model.old_file_user_name[i]
                new_name = self.newname_model.new_file_user_name[i]

                if not old_name and not new_name:
                    self.show_warning('Writing a file name.')
                    self.window_all_clear()
                    return

                if old_name and new_name and len(self.newname_model.old_full_path) != len(self.newname_model.new_full_path):
                    self.process_rename(old_name, new_name)
                else:
                    self.show_warning('File name does not exist.')
                    self.window_all_clear()
                    return
            self.window_all_clear()
            self.show_warning('Rename is done.')

        elif not self.browse_count:
            self.show_warning('Push the browse button.')
            self.window_all_clear()
            return

    def process_rename(self, old_name, new_name):
        for full_path in self.newname_model.old_full_path:
            if any(user_file_name in full_path for user_file_name in old_name):
                origin_file_name = os.path.basename(full_path)
                without_origin_file_ext, origin_file_ext = os.path.splitext(origin_file_name)
                new_file_name = without_origin_file_ext.replace(old_name, new_name)
                new_full_path = '/'.join(full_path.split("/")[:-1]) + '/' + new_file_name + origin_file_ext
                self.newname_model.new_full_path.append(new_full_path)
                os.rename(full_path, new_full_path)
            else:
                self.show_warning('File name does not exist.')
                self.window_all_clear()
                return
        self.newname_model.old_full_path = self.newname_model.new_full_path
        self.newname_model.new_full_path = []

    def window_all_clear(self):
        if self.action_count > 0:
            for i in range(self.action_count + 1):
                self.newname_model.old_text_widget[i].setText('')
                self.newname_model.new_text_widget[i].setText('')
                self.deleted_old_text_widget.append(self.newname_model.old_text_widget[i])
                self.deleted_new_text_widget.append(self.newname_model.new_text_widget[i])
                self.deleted_rename_hbox.append(self.newname_model.rename_hbox[i])
                self.deleted_rename_hwidget.append(self.newname_model.rename_hwidget[i])

            for i in range(self.action_count):
                self.newname_model.old_text_widget[i + 1].setParent(None)
                self.newname_model.new_text_widget[i + 1].setParent(None)
                self.newname_model.rename_hbox[i + 1].removeWidget(self.newname_model.old_text_widget[i + 1])
                self.newname_model.rename_hbox[i + 1].removeWidget(self.newname_model.new_text_widget[i + 1])
                self.main_view.new_name_vbox_layout.takeAt(self.main_view.new_name_vbox_layout.count() - 1)

        self.newname_model.old_text_widget[0].setText('')
        self.newname_model.new_text_widget[0].setText('')

        self.newname_model.old_file_user_name = []
        self.newname_model.new_file_user_name = []

        self.newname_model.old_full_path = []
        self.main_view.line_edit.setText('')

        self.action_count = 0
        self.browse_count = False

        if self.file_list_dialog is not None:
            self.file_list_dialog.close()

    @staticmethod
    def show_warning(error_message):
        warning_box_style = """
            QMessageBox{
                font: 15pt "Courier New";
                background-color: rgb(60, 60, 60);
                color: rgb(225, 225, 225);
            }

            /* Set the style of the text label */
            QLabel {
                color: rgb(225, 225, 225);
                font-size: 18px;
            }

            /* Set the style of the OK button */
            QPushButton {
                background-color: rgb(50, 50, 50);
                color: rgb(225, 225, 225);
                padding: 5px;
                border: 1px solid rgb(225, 225, 225);
                border-radius: 3px;
            }

            /* Set the style of the OK button when hovered */
            QPushButton:hover {
                background-color: rgb(80, 80, 80);
            }

            /* Set the style of the OK button when pressed */
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(f"{error_message}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(warning_box_style)
        msg_box.exec_()


def main():
    app = QApplication()
    controller = RenamePathController()
    window = QMainWindow()
    window.setCentralWidget(controller.main_view)
    window.setWindowTitle("Renamer")
    window.setFixedSize(400, 210)
    window.setStyleSheet("background-color: rgb(50, 50, 50);")
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
