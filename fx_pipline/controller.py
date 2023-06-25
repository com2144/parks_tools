from fx_pipline.model import PipelineSetupModel
from fx_pipline.view import PipelineSetupView, BrowseDialog

class PipelineSetupController:
    def __init__(self):
        self.model = PipelineSetupModel()
        self.view = PipelineSetupView()

        self.view.browse_button.clicked.connect(self.browse_clicked)


    def browse_clicked(self):
        dialog = BrowseDialog()
        self.model.home_path = dialog.option
        self.view.browse_line_edit.setText(self.model.home_path)
        print(self.model.home_path)