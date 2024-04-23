# !/usr/bin/env python
# :coding: utf-8

from model import *
from view import *
from PySide2.QtWidgets import *
import sys
import os


class DownLoadController:
    def __init__(self, main_window, argv):

        self.model = DownLoadModel(argv)
        self.action = self.model.action_handle.action
        self.main_window = main_window
        self.view = DownLoadMainView()

        self.dialog = None

        self.path = self.model.path

        self.browse_sig = False

        self.view.main_ui()
        self.view.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.view.ok_button.clicked.connect(self.on_ok_button_clicked)
        self.view.cancel_button.clicked.connect(self.on_cancel_button_clicked)

    def on_browse_button_clicked(self):
        self.browse_sig = True

        if self.dialog is not None:
            self.dialog.close()

        browse_option = BrowseDialog()
        self.path = browse_option.option

        if not self.path:
            self.show_warning('Choose the directory')
        else:
            self.view.path_line_edit.setText(self.path)

    def on_ok_button_clicked(self):
        self.model.download_url_file(self.path)
        if os.path.exists(self.path):
            self.show_warning('Mp4 files save!')
        else:
            self.show_warning('Failed to save Mp4 files')
        self.browse_sig = False

    def on_cancel_button_clicked(self):
        self.browse_sig = False
        self.main_window.close()

    @staticmethod
    def show_warning(error_message):
        warning_box_style = """
            QMessageBox{
                font: 15pt "Courier New";
                background-color: rgb(50, 50, 50);
                color: rgb(225, 225, 225);
            }

            /* Set the style of the text label */
            QLabel {
                color: rgb(225, 225, 225);
                font-size: 18px;
            }

            /* Set the style of the OK button */
            QPushButton {
                background-color: rgb(40, 40, 40);
                color: rgb(225, 225, 225);
                padding: 5px;
                border: 1px solid rgb(225, 225, 225);
                border-radius: 3px;
            }

            /* Set the style of the OK button when hovered */
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }

            /* Set the style of the OK button when pressed */
            QPushButton:pressed {
                background-color: rgb(30, 30, 30);
            }
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Message")
        msg_box.setText(f"{error_message}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(warning_box_style)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    try:
        controller = DownLoadController(window, sys.argv)
        controller.model.action_handle.log.info("ShotgunAction: Firing... %s" % (sys.argv[1]))
    except IndexError as e:
        raise ShotgunActionException("Missing GET arguments")
    controller.model.action_handle.log.info("ShotgunAction process finished.")
    window.setCentralWidget(controller.view)
    window.setWindowTitle('Mp4 Downloader')
    window.setFixedSize(500, 150)
    window.setStyleSheet("background-color: rgb(50, 50, 50);")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
