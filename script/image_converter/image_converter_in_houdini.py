import hou
import os
import subprocess

class ImageConverting:
    def __init__(self):
        self.file_name = ''
        self.ext = ''
        self.mp4_file_path = ''
        self.render_path = '' 
        self.image_file_path = ''
        self.start_frame = 0
        self.end_frame = 0
        
    
    def render_action(self):
        select_node = hou.ui.selectNode()
        
        if select_node is None:
            self.warning_message('Select Node plz!')
            return
        
        confirm_out = select_node.split('/')
            
        if 'out' in confirm_out:
            self.node = hou.node(select_node)
            self.make_paths()
            self.convert_action()
            
        elif 'out' not in confirm_out:
            self.warning_message('Select Out network plz')
            return

            
            
    def make_paths(self):
        image_path = self.node.parm('vm_picture').evalAsString()
        root_path = image_path.split('/')
        
        self.file_name = root_path[-1]
        ver_num = root_path[-2]
        render_dir_name = root_path[-3]
        jpg_dir_name = root_path[-4]
        
        
        for i in range(0,4):
            del root_path[-1]

        root_path = '/'.join(root_path)
        
        
        file_name_split = self.file_name.split('.')
        self.ext = file_name_split[-1]
        
        
        for i in range(0,3):
            del file_name_split[-1]        
        
        self.file_name = '.'.join(file_name_split)     
        

        mp4_path = f'{root_path}/mp4/{self.file_name}/{ver_num}'

        if not os.path.exists(mp4_path):
            os.makedirs(mp4_path)
                
        self.mp4_file_path = f'{mp4_path}/{self.file_name}.{ver_num}.mp4'
        self.render_path = f'{root_path}/{jpg_dir_name}/{render_dir_name}/{ver_num}'
        self.image_file_path = f'{self.render_path}/{self.file_name}.{ver_num}.%04d.{self.ext}'
        
   
    def convert_action(self):
        self.start_frame = int(self.node.parm('f1').evalAsString())
        self.end_frame = int(self.node.parm('f2').evalAsString())
        
        end_to_start = self.end_frame - self.start_frame + 1

        if not os.path.exists(self.render_path):
            os.makedirs(self.render_path)
        
        render_dir_count = len(os.listdir(self.render_path))
        
        if self.ext not in ['jpg', 'exr']:
            self.warning_message('Wrong extension setup!')
            return
            
        if os.path.exists(self.mp4_file_path):
            os.remove(self.mp4_file_path)
            
        if end_to_start != render_dir_count:
            self.node.parm('trange').set(1)
            self.node.parm('execute').pressButton()
            ffmpeg_cmd = f'ffmpeg -framerate 24 -start_number {self.start_frame} -i {self.image_file_path} -frames:v {self.end_frame} {self.mp4_file_path}'
            subprocess.run(ffmpeg_cmd, shell=True)
            self.warning_message('Converting is Done')           
        else:
            ffmpeg_cmd = f'ffmpeg -framerate 24 -start_number {self.start_frame} -i {self.image_file_path} -frames:v {self.end_frame} {self.mp4_file_path}'
            subprocess.run(ffmpeg_cmd, shell=True)
            self.warning_message('Converting is Done')
  
    @staticmethod
    def warning_message(message):
        hou.ui.displayMessage(message, title='Warning', severity=hou.severityType.Message)

    # def yes_or_no_window(self):
    #     signal = hou.ui.displayMessage("mp4 already exists. Do you want to convert?", buttons=('Yes', 'No'))
    #     if signal == 0:
    #         os.remove(self.mp4_file_path)
    #         ffmpeg_cmd = f'ffmpeg -framerate 24 -start_number {self.start_frame} -i {self.image_file_path} -frames:v {self.end_frame} {self.mp4_file_path}'
    #         subprocess.run(ffmpeg_cmd, shell=True)
    #         self.warning_message('Converting is Done')
    #     else: 
    #         pass
        
        
def main():
    test = ImageConverting()
    test.render_action()
    
main()