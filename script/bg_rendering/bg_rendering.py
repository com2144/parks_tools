import os
import sys
import shutil
import traceback
import time
import subprocess

import hou
import psutil

from bg_rendering_model import *
import bg_rendering_ui


HOU_EXEC = sys.executable


class BGrender:
    def __init__(self):
        self.model = BGrenderModel()
        self.ui = bg_rendering_ui.BGrenderUI()

        self.ui.browse_btn.clicked.connect(self._set_hip_file)
        self.ui.render_btn.clicked.connect(self.render_action)
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
            
            self.ui.table_wg.clear()
            self._set_hou_info_tbl()
        
        else:
            self.ui.message_box('error', 'Hip File Empty', 'Select the Hip File !')
            return


    def _set_hou_info_tbl(self):
        hou.hipFile.load(self.model.hip_file)

        stage_op = hou.node('/stage')
        all_stage_nodes = stage_op.allSubChildren()

        self.model.usdrender_nodes = [node.path() for node in all_stage_nodes if node.type().name() == 'usdrender_rop' and 
                                      node.input(0).type().name() in self.model.render_list ]
        
        render_tbl = self.ui.table_wg
        render_tbl.clearContents()
        render_tbl.setRowCount(0)
        
        row_count = len(self.model.usdrender_nodes)
        column_count = render_tbl.columnCount()

        render_tbl.setRowCount(row_count)

        for row_idx, node_path in enumerate(self.model.usdrender_nodes):
            rop_node = hou.node(node_path)
            tmp_list = []
            for col_idx in range(column_count):
                if col_idx == 0:
                    chkbox_item = bg_rendering_ui.CheckBoxWidget()
                    chkbox_item.chk_box.setCheckable(True)
                    chkbox_item.chk_box.setChecked(True)
                    render_tbl.setCellWidget(row_idx, col_idx, chkbox_item)

                    tmp_list.append(chkbox_item.chk_box)
                
                elif col_idx == 1:
                    lb_item = bg_rendering_ui.LabelWidget()
                    lb_item.lb.setText(rop_node.name())
                    render_tbl.setCellWidget(row_idx, col_idx, lb_item)

                    tmp_list.append(lb_item.lb)
                
                elif col_idx == 2:
                    parent_node = rop_node.input(0)
                    save_seq_path = parent_node.parm('picture').rawValue()

                    path_edt_item = bg_rendering_ui.LineEditWidget()
                    path_edt_item.line_edt.setText(save_seq_path)
                    self.model.export_path_list.append(save_seq_path)
                    render_tbl.setCellWidget(row_idx, col_idx, path_edt_item)

                    tmp_list.append(path_edt_item.line_edt)
                
                elif col_idx == 3:
                    start_frame = rop_node.parm('f1').eval()

                    str_edt_item = bg_rendering_ui.LineEditWidget()
                    str_edt_item.line_edt.setText(str(int(start_frame)))
                    self.model.start_frame_list.append(start_frame)
                    render_tbl.setCellWidget(row_idx, col_idx, str_edt_item)

                    tmp_list.append(str_edt_item.line_edt)
                
                elif col_idx == 4:
                    end_frame = rop_node.parm('f2').eval()

                    end_edt_item = bg_rendering_ui.LineEditWidget()
                    end_edt_item.line_edt.setText(str(int(end_frame)))
                    self.model.end_frame_list.append(end_frame)
                    render_tbl.setCellWidget(row_idx, col_idx, end_edt_item)

                    tmp_list.append(end_edt_item.line_edt)

            self.model.wg_list.append(tmp_list)


    def confirm_render_info(self):
        error_list = []
        difference = False

        for idx, node_path in enumerate(self.model.usdrender_nodes):
            wg_inst = self.model.wg_list[idx]
            rop_node = hou.node(node_path)
            if wg_inst[0].isChecked():
                node_name = str(wg_inst[1].text())
                export_path = str(wg_inst[2].text())
                start_frame = str(wg_inst[3].text())
                end_frame = str(wg_inst[4].text())

                if export_path != self.model.export_path_list[idx]:
                    ext = os.path.splitext(export_path)[-1]
                    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.exr']:
                        error_list.append(f'[{idx}] "{node_name}" is not "{ext}" supported.')
                    else:
                        rop_node.parm('picture').set(export_path)
                        difference = True

                if start_frame != self.model.start_frame_list[idx] or end_frame != self.model.end_frame_list[idx]:
                    rop_node.parm('trange').set(1)
                    frame_parm = rop_node.parmTuple('f')
                    frame_parm.deleteAllKeyframes()

                    if start_frame.isdigit():
                        rop_node.parm('f1').set(int(start_frame))
                        difference = True
                    else:
                        error_list.append(f'[{idx}] "{node_name}" start frame is not int. ::: "{start_frame}"')

                    if end_frame.isdigit():
                        rop_node.parm('f2').set(int(end_frame))
                        difference = True
                    else:
                        error_list.append(f'[{idx}] "{node_name}" end frame is not int. ::: "{end_frame}"')

        if not error_list and difference:
            hou.hipFile.save(self.model.hip_file)
        else:
            error_list.insert(0, 'confirm Rop node info error')
            error_list.insert(1, '='*50)

        return error_list


    def copy_tmp_hip(self):
        error_list = []

        try:
            self.model.tmp_file = os.path.join(os.path.dirname(self.model.hip_file), 
                                            '.' + os.path.basename(self.model.hip_file))

            if os.path.exists(self.model.tmp_file):
                os.remove(self.model.tmp_file)
            
            shutil.copy2(self.model.hip_file, self.model.tmp_file)
        
        except:
            error_list.append('tmp Hip file create error')
            error_list.append('='*50)
            error_list.append(str(traceback.format_exc()))

        return error_list


    def render_action(self):
        error_list = []

        if not self.model.hip_file:
            error_list.append('Press the "Browse" Button and Select the Hip File')

        if not error_list:
            info_confirm = self.confirm_render_info()
            error_list.extend(info_confirm)

        if not error_list:
            copy_tmp = self.copy_tmp_hip()
            error_list.extend(copy_tmp)

        if not error_list:
            render_script = os.path.join(os.path.dirname(self.model.tmp_file), 'rendering_script.py')

            for idx, node_path in enumerate(self.model.usdrender_nodes):
                wg_inst = self.model.wg_list[idx]
                if wg_inst[0].isChecked():
                    frame_range = [f for f in range(int(wg_inst[3].text()), int(wg_inst[4].text())+1)]

                    total_frames = len(frame_range)
                    current_frame_idx = 0

                    print('@'*115)
                    print(f'Node Name :: {str(wg_inst[1].text())}')
                    for frame in frame_range:
                        print('@'*115)
                        content = 'import hou\n\n'

                        content += f'hou.hipFile.load("{self.model.tmp_file}")\n'
                        content += f'render_node = hou.node("{node_path}")\n'
                        content += 'render_node.parm("verbose").set(1)\n'
                        content += 'render_node.parm("trange").set(1)\n'
                        content += 'frame_parm = render_node.parmTuple("f")\n'
                        content += 'frame_parm.deleteAllKeyframes()\n'
                        content += f'frame_parm.set(({frame}, {frame}, 1))\n\n'

                        content += f'hou.hipFile.save("{self.model.tmp_file}")\n'
                        content += 'render_node.parm("execute").pressButton()\n'

                        memory_used = psutil.virtual_memory().percent
                        if memory_used > 90:
                            content += 'hou.exit(exit_code=0, suppress_save_prompt=True)\n'
                        
                        with open(render_script, 'w') as file:
                            file.write(content)
                        
                        if memory_used > 90:
                            print(('#'*20) + f' Memory Used :: {memory_used} ' + ('#'*20))
                            time.sleep(5)
                        
                        result = subprocess.run([HOU_EXEC, '-b', render_script])
                        if result.stderr:
                            error_list.append(f'[{idx}] "{wg_inst[1].text()}" node is render failed ::: frame - "{frame}"')
                            error_list.append(f'Error msg ::: {result.stderr.strip()}')
                        
                        current_frame_idx += 1
                        print('@'*115)
                        self.print_progress_bar(current_frame_idx, total_frames)
                        print('@'*115)
                        print('\n')

                    print('#'*115)
                    print(f'[{idx}] "{str(wg_inst[2].text())}" Render Done!')
                    print('#'*115)
                    print('\n')

            self.rm_job(self.model.hip_file, render_script)

            print('\n')
            print('*'*115)
            print('All Render Job Done !!!!')
            print('*'*115)
            print('\n')
            self.ui.message_box('info', 'Render Task', 'All Render Job Done !!!!')

        if error_list:
            error_list.insert(0, 'Rendering Process Error')
            error_list.insert(1, '^'*50)
            error_list.append('='*50)

            error_msg = '\n'.join(error_list)

            self.ui.message_box('error', 'Rendering Error', error_msg)


    def rm_job(self, hip, render_script):
        if os.path.exists(hip):
            os.remove(hip)
        
        if os.path.exists(render_script):
            os.remove(render_script)


    def print_progress_bar(self, iteration, total, length=90):
        percent = iteration / total
        filled_length = int(length * percent)
        bar = '█' * filled_length + '-' * (length - filled_length)
        print(f'\r Progress {iteration}/{total} |{bar}| {percent*100:.1f}%')




if __name__ == '__main__':
    app = bg_rendering_ui.QApplication(sys.argv)

    bg_render = BGrender()

    main_ui = bg_render.ui
    main_ui.show()

    sys.exit(app.exec_())