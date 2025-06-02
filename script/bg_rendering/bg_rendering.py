import os
import sys

from bg_rendering_model import *
import bg_rendering_ui


HOU_EXEC = sys.executable


class BGrender:
    def __init__(self):
        self.model = BGrenderModel()
        self.ui = bg_rendering_ui.BGrenderUI()

        self.ui.browse_btn.clicked.connect(self._set_hip_file)
        self.ui.cancel_btn.clicked.connect(self.ui.close)


    def _set_hip_file(self):
        home_path = os.path.expanduser('~') 
        file_path = bg_rendering_ui.QFileDialog.getOpenFileName(
            self.ui,
            'Select Hip File',
            home_path,
            'Houdini Files (*.hip *.hiplc *.hipnc)'
        )

        if file_path[0]:
            self.model.hip_file = str(file_path[0])
            self.ui.browse_edt.setText(self.model.hip_file)
        
        else:
            self.ui.message_box('error', 'Hip File Empty', 'Select the Hip File !')
            return






if __name__ == '__main__':
    app = bg_rendering_ui.QApplication(sys.argv)

    bg_render = BGrender()

    main_ui = bg_render.ui
    main_ui.show()

    sys.exit(app.exec_())