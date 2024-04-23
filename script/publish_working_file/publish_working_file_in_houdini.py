import hou
import os
import shutil

class Publish_file:
    def __init__(self):
        self.previous_path = ''
        self.work_path = ''
        self.publish_path = ''
        self.file_name = ''
        self.ext = ''
    
    def publish_file_path(self):
        self.previous_path = hou.hipFile.path()
        split_path = self.previous_path.split('/')
        
        previous_file_name = split_path[-1]
        
        for i in range(0,3):
            del split_path[-1]
        
        self.publish_path = '/'.join(split_path)
        self.work_path = f'{self.publish_path}/work/houdini'
        self.publish_path = f'{self.publish_path}/pub/houdini'
        
        
        split_ext = previous_file_name.split('.')
        self.ext = split_ext[-1]
        del split_ext[-1]
            
        split_ver = split_ext[-1].split('_')
        del split_ver[-1]
        
        self.file_name = '_'.join(split_ver)
    
    def make_publish_path(self):
        files = []
        work_dir = os.listdir(self.work_path)
        
        for item in work_dir:
            item_path = f'{self.work_path}/{item}'
            if os.path.isfile(item_path):
                files.append(item)
        
        current_version_num = len(files)
        
        if not os.path.exists(self.publish_path):
            os.makedirs(self.publish_path)
        
        next_publish_file_path = f'{self.publish_path}/{self.file_name}_v{current_version_num:03d}.{self.ext}'
        next_work_file_path = f'{self.work_path}/{self.file_name}_v{(current_version_num+1):03d}.{self.ext}'
        
        if not os.path.exists(next_publish_file_path):
            hou.hipFile.save(next_work_file_path, save_to_recent_files=True)
            hou.hipFile.load(next_work_file_path)
            shutil.copyfile(self.previous_path, next_publish_file_path)

def main():
    pub = Publish_file()
    pub.publish_file_path()
    pub.make_publish_path()
    
main()