import hou
import os
import json

class PipelineSetupModel:
    def __init__(self):
        self._home_path = ''
        self.project_name = ''
        self.project_path = ''
        self.ext = ''

        self.fx_shots_path = ''

        self.dir_path = ''
        self.user_path = ''

        self.user_dict = None

        self.home_json_path()
        self.access_setting()

    @property
    def home_path(self):
        return self._home_path

    @home_path.setter
    def home_path(self, value):
        self._home_path = value
    
    def project_set(self, proj_name):
        self.project_name = proj_name
        self.project_path = f'{self.home_path}/{proj_name}'
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
    
    def ext_set(self, hou_ext):
        self.ext = hou_ext
    
    def assets_path_init_set(self):
        assets_path = f'{self.project_path}/asset'
        asset_list = ['char', 'env', 'prop', 'veh']

        for asset in asset_list:
            list_path = f'{assets_path}/{asset}'
            if not os.path.exists(list_path):
                os.makedirs(list_path)

    def shots_path_init_set(self):
        self.fx_shots_path = f'{self.project_path}/shot/fx'
        fx_shot_list = ['work', 'ref']
        work_list = ['houdini', 'nuke', 'maya', 'cam','review']

        ref_list = ['artwork', 'footage']

        for shot in fx_shot_list:
            if shot == 'ref':
                for ref_item in ref_list:
                    fx_ref_path = f'{self.fx_shots_path}/ref/{ref_item}'
                    if not os.path.exists(fx_ref_path):
                        os.makedirs(fx_ref_path)
            else:
                fx_work_path = f'{self.fx_shots_path}/{shot}'
                for work in work_list:
                    work_file_path = f'{fx_work_path}/{work}'
                    if not os.path.exists(work_file_path):
                        os.makedirs(work_file_path)

        plate_shots_path = f'{self.project_path}/shot/plate'
        plate_list = ['org', 'jpg', 'mp4']

        for plate in plate_list:
            list_path = f'{plate_shots_path}/{plate}'
            if not os.path.exists(list_path):
                os.makedirs(list_path)

    def review_path_init_set(self):
        review_path = f'{self.fx_shots_path}/work/review'
        review_list = ['jpg', 'mp4', 'exr']

        for review in review_list:
            review_list_path = f'{review_path}/{review}'
            if not os.path.exists(review_list_path):
                os.makedirs(review_list_path)
    
    def houdini_path_init_set(self):
        work_path = f'{self.fx_shots_path}/work/houdini'
        cache_dir_path = f'{work_path}/cache'
        if not os.path.exists(cache_dir_path):
            os.makedirs(cache_dir_path)

        file_name = f'{work_path}/{self.project_name}_shot_fx_work_v001.{self.ext}'
        if not os.path.exists(file_name):
            hou.hipFile.save(file_name, save_to_recent_files=False)
    
    def home_json_path(self):
        now_path = os.path.realpath(__file__)
        split_path = now_path.split('\\')[:-1]
        self.dir_path = f"{'/'.join(split_path)}/.config"
        self.user_path = f"{self.dir_path}/user.json"
    
    def access_setting(self):
        if not os.path.exists(self.dir_path):
            try:
                os.makedirs(self.dir_path)
            except OSError:
                raise ValueError("Failed to create the directory.")
        try:
            if not os.path.exists(self.user_path):
                self.reset_setting()
        except OSError:
            raise ValueError("Failed to create user.json file.")
        return True
    
    def save_setting(self):
        self.user_dict = {
            'home': self.home_path
        }
        with open(self.user_path, 'w') as json_file:
            json.dump(self.user_dict, json_file)
    
    def load_setting(self):
        with open(self.user_path, 'r') as json_file:
            self.user_dict = json.load(json_file)
    
    def reset_setting(self):
        self.home_path = ''
        self.save_setting()

def main():
    test = PipelineSetupModel()
    test.home_path = 'C:/Users/com2144/Desktop/test'
    test.project_set('pt')
    test.ext_set('hiplc')
    test.assets_path_init_set()
    test.shots_path_init_set()
    test.review_path_init_set()
    test.houdini_path_init_set()

if __name__ == '__main__':
    main()
