from model import *
from view import *

class PipelineSetupController:
    def __init__(self):
        self.model = PipelineSetupModel()
        self.view = PipelineSetupView()

        self.view.browse_button.clicked.connect(self.browse_clicked)
        self.view.ok_button.clicked.connect(self.ok_clicked)
        self.view.cancel_button.clicked.connect(self.cancel_clicked)

    def browse_clicked(self):
        dialog = BrowseDialog()
        self.model.home_path = dialog.option
        self.view.browse_line_edit.setText(self.model.home_path)
        self.model.save_setting()
    
    def ok_clicked(self):
        if not self.view.browse_line_edit.text():
            self.view.message_box('Choose the home path')
            self.clean_up()
            return
        elif not self.view.project_line_edit.text():
            self.view.message_box('Write a Project name')
            self.clean_up()
            return
        elif not (self.model.home_path and self.view.project_line_edit):
            self.view.message_box('Choose the home path and write Project name')
            self.clean_up()
            return
        else:
            self.model.project_set(self.view.project_line_edit.text())
            self.model.ext_set(self.view.ext_combo_box.currentText())

            asset_path = f'{self.model.home_path}/{self.model.project_name}/asset'
            shot_path = f'{self.model.home_path}/{self.model.project_name}/shot'

            if not (os.path.exists(asset_path) or os.path.exists(shot_path)):
                self.model.assets_path_init_set()
                self.model.shots_path_init_set()
                self.model.review_path_init_set()
                self.model.houdini_path_init_set()
                self.view.message_box('Project initial setting Done')
                self.clean_up()
            else:
                self.view.message_box('Project already exists')
                self.clean_up()
   
    def clean_up(self):
        self.view.browse_line_edit.setText('')
        self.view.project_line_edit.setText('')
        self.model.home_path = ''
        self.model.project_name = ''
    
    def cancel_clicked(self):
        self.view.close()
    
    def root_confirm_box(self, root_path):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(f"{root_path} is already exists. Do you want to use it?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        result = msg_box.exec_()

        if result == QMessageBox.Ok:
            self.view.browse_line_edit.setText(root_path)
            self.model.home_path = root_path
        elif result == QMessageBox.Cancel:
            self.clean_up()
            self.model.reset_setting()

    
if __name__ == '__main__':
    app = QApplication()
    controller = PipelineSetupController()
    controller.view.show()
    controller.model.load_setting()
    if controller.model.user_dict.get('home'):
        controller.root_confirm_box(controller.model.user_dict.get('home')) 
    app.exec_()
