from view import *
from model import *


class LoadConvertController:
    def __init__(self):
        self.model = LoadConvertModel()
        self.view = LoadConvertView()

        self.model.set_project()

        for project in self.model.all_project:
            self.view.combo_box.addItem(project)

        self.selected_xlsx = ''
        self.selected_project = ''

        self.view.combo_box.currentIndexChanged.connect(self.combo_box_changed)
        self.view.browse_button.clicked.connect(self.browse_clicked)
        self.view.ok_button.clicked.connect(self.ok_clicked)
        self.view.cancel_button.clicked.connect(self.cancel_clicked)

    def combo_box_changed(self):
        self.selected_project = self.view.combo_box.currentText()
        self.view.label.setText(f'Converting Project: {self.selected_project}')
        print(f'selected project: {self.selected_project}')

    def browse_clicked(self):
        dialog = BrowseDialog()
        self.selected_xlsx = dialog.file_name
        self.view.line_edit.setText(self.selected_xlsx)
        self.model.set_file_path(self.selected_xlsx)
        print(f'selected xlsx file: {self.selected_xlsx}')

    def ok_clicked(self):
        if not self.model.file_path:
            self.view.message_box('Choose the xlsx file')
            self.clean_up()
            return
        if not self.selected_project:
            self.view.message_box('Choose the project')
            self.clean_up()
            return
        if not self.model.file_path and self.selected_project:
            self.view.message_box('Choose the xlsx file and project')
            self.clean_up()
        else:
            self.model.set_file_path(self.model.file_path)
            self.model.data_info()
            self.model.get_project(self.selected_project)
            self.model.get_sequence_and_upload()
            self.model.get_shot_and_upload()
            self.model.video_uploader()
            self.view.message_box('Work is Done')

    def clean_up(self):
        self.view.line_edit.setText('')
        self.selected_xlsx = ''
        self.model.file_path = ''

    def cancel_clicked(self):
        self.view.close()


if __name__ == '__main__':
    app = QApplication()
    controller = LoadConvertController()
    controller.view.show()
    app.exec_()
