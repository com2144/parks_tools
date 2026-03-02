import os
import subprocess
import platform
import psutil
import shutil
from importlib import reload

import hou

import export_mov_ui
import export_mov_model

reload(export_mov_ui)
reload(export_mov_model)


class ExportMov:
    def __init__(self):
        self.ui = export_mov_ui.ExportMovUI()
        self.model = export_mov_model.ExportMovModel()

        self.set_init_frame_range()

        self.cam_node_tree_dlg = None

        self.ui.cam_select_btn_func(lambda: self.cam_node_tree_open())
        self.ui.browse_btn_func(lambda: self.set_save_dir())
        self.ui.ok_btn_func(lambda:self.ok_action())
        self.ui.close_ui(lambda: self.ui.close())
    

    def set_init_frame_range(self):
        start, end = hou.playbar.playbackRange()
        self.ui.start_frame.setText(str(int(start)))
        self.ui.end_frame.setText(str(int(end)))


    def cam_node_tree_open(self):
        self.cam_node_tree_dlg = export_mov_ui.CamNodeTreeDialog(parent=self.ui)
        self.cam_node_tree_dlg.selectSignal.connect(self.cam_node_tree_handle_select)
        self.cam_node_tree_dlg.closeSignal.connect(self.cam_node_tree_handle_close)
        self.cam_node_tree_dlg.exec_()


    def cam_node_tree_handle_select(self, node):
        self.model.cam_node = node
        self.ui.cam_edt.setText(node.path())


    def cam_node_tree_handle_close(self):
        print('Cam Node tree close')
        self.cam_node_tree_dlg = None


    def set_save_dir(self):
        home_path = os.path.expanduser('~')
        save_dir_path = export_mov_ui.QFileDialog.getExistingDirectory(
            self.ui,
            'Select Directory',
            home_path
        )

        if not save_dir_path:
            self.ui.message_box('error', 'Empty SavePath', 'Select the SaveDir !!')
            return

        hip_file_name = os.path.splitext(hou.hipFile.basename())[0]

        self.model.jpg_path =  os.path.join(save_dir_path, '.tmp', hip_file_name + '.$F4' + '.jpg').replace('\\','/')
        self.model.mov_path = os.path.join(save_dir_path, hip_file_name+'.mov').replace('\\','/')
        self.ui.save_path_edt.setText(self.model.mov_path)


    def ok_action(self):
        if not self.ui.cam_edt.text():
            self.ui.message_box('error', 'CamPath Empty', 'Select the Cam node !!')
            return

        if not self.ui.save_path_edt.text():
            self.ui.message_box('error', 'SavePath Empty', 'Select the Save Path !!')
            return
        
        if not os.path.exists(os.path.dirname(self.model.mov_path)):
            self.ui.message_box('error', 'SaveDirPath Error', 'Save Dir is not exists !!')
            return
        
        if not os.path.exists(os.path.dirname(self.model.jpg_path)):
            os.mkdir(os.path.dirname(self.model.jpg_path))
        else:
            jpg_list = os.listdir(os.path.dirname(self.model.jpg_path))
            if jpg_list:
                rm_result = self.ui.message_box('warning', 'JpgDir Exists', 'JpgDir is Exists, Do you want to overwrite?', confirm=True)
                if rm_result == 'yes':
                    for file in jpg_list:
                        jpg_path = os.path.join(os.path.dirname(self.model.jpg_path), file)
                        if os.path.isfile(jpg_path):
                            os.remove(jpg_path)

        cam_x, cam_y = self.model.cam_node.parmTuple('res').eval()
        start_text = self.ui.start_frame.text().strip()
        end_text = self.ui.end_frame.text().strip()

        try:
            self.model.start = int(start_text)
            self.model.end = int(end_text)
        except ValueError:
            self.ui.message_box('error', 'ValueError', 'Input the integer value !!')
            return
        
        cur_desktop = hou.ui.curDesktop()
        sceneviewer = cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
        viewport = sceneviewer.selectedViewport()
        viewport.settings().setCamera(self.model.cam_node.path())

        flipbook_options = sceneviewer.flipbookSettings()
        flipbook_options.stash()
        flipbook_options.output(self.model.jpg_path)
        flipbook_options.frameRange((float(self.model.start), float(self.model.end)))
        flipbook_options.useResolution(True)
        flipbook_options.resolution((int(cam_x), int(cam_y)))

        sceneviewer.flipbook(
            viewport=viewport,
            settings=flipbook_options
        )

        flipbook_options = sceneviewer.flipbookSettings()
        flipbook_options.stash()
        flipbook_options.output('')
        start, end = hou.playbar.playbackRange()
        flipbook_options.frameRange((float(start), float(end)))

        is_windows = platform.system().lower() == "windows"

        for proc in psutil.process_iter(attrs=["pid", "name"]):
            name = proc.info["name"]

            if name.lower() in ["mplay-bin", "mplay.exe"]:
                pid = proc.info["pid"]

                if is_windows:
                    os.system(f"taskkill /PID {pid} /F")
                else:
                    os.system(f"kill -9 {pid}")

        self.mk_mov()


    def mk_mov(self):
        jpg_dir_list = os.listdir(os.path.dirname(self.model.jpg_path))
        if not jpg_dir_list:
            self.ui.message_box('error', 'jpg make Error', 'Make the jpg error')
            return
        
        psj_site = os.getenv('PSJ_SITE')
        ffmpeg_exec = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
        ffmpeg_path = os.path.join(psj_site, 'external_script', 'mp4_converter', 'tools', ffmpeg_exec)

        jpg_path = self.model.jpg_path.replace('$F4', '%04d')

        cmd = [ffmpeg_path]
        cmd.append('-y')
        cmd.append('-start_number')
        cmd.append(str(self.model.start))
        cmd.append('-i')
        cmd.append(jpg_path)
        cmd.append('-c:v')
        cmd.append('prores_ks')
        cmd.append('-profile:v')
        cmd.append('3')
        cmd.append(self.model.mov_path)

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"stderr\n {result.stderr}")
            self.ui.message_box("error", "ffmpeg Error", 'Export to Mov Error')
            return
        else:
            print(f"stdout\n {result.stdout}")
            self.ui.message_box('info', 'ExportMov Done', 'Export to Mov Done.')