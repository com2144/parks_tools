import os
import hou


def load():
    now_proj_file = hou.hipFile.path() 

    save_confirm = os.path.exists( now_proj_file )

    if not save_confirm:
        warning_window( 'Before the save First.' )
        return

    hou.hipFile.save(now_proj_file)
    hou.hipFile.load(now_proj_file)

def warning_window(message):
    hou.ui.displayMessage(message, severity=hou.severityType.ImportantMessage)