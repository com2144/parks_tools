import os
import shutil
import subprocess

import openpyxl
from shotgun_api3 import Shotgun

from pprint import pprint


class LoadConvertModel:
    def __init__(self):
        url = 'https://rndtest.shotgrid.autodesk.com/'
        script_names = 'script_psj'
        script_key = '^paskzjpyknuijyzugkrbzo3F'
        self.sg = Shotgun(base_url=url, script_name=script_names, api_key=script_key)

        self.file_path = ''
        self.home_root = ''

        self.xlsx_data = []

        self.all_project = []
        self.project = None
        self.sequence = None
        self.existing_shots = None
        self.shot = None
        self.version = None

        self.version_num = []
        self.scan_path = []
        self.type = []
        self.just_in = []
        self.just_out = []
        self.resolution = []
        self.ext = []
        self.start_frame = []
        self.end_frame = []
        self.duration = []
        self.timecode_in = []
        self.timecode_out = []
        self.framerate = []
        self.date = []

        self.work_root = []
        self.org_root = []
        self.mp4_file_path_list = []

    def set_file_path(self, path):
        self.file_path = path

    def data_info(self):
        split_path = self.file_path.split('/')
        self.home_root = os.sep.join(split_path[:3]) + os.sep

        workbook = openpyxl.load_workbook(self.file_path)
        worksheet = workbook.active
        header = [cell.value for cell in worksheet[1]]
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            self.xlsx_data.append(dict(zip(header, row)))
        pprint(self.xlsx_data)

    def set_project(self):
        fields = ['name', 'sg_status']
        projects = self.sg.find("Project", [], fields)

        for project in projects:
            if project.get('sg_status') == 'Active':
                self.all_project.append(project.get('name'))

    def get_project(self, project_name):
        filters = [['name', 'is', project_name],
                   ['sg_status', 'is', 'Active']
                   ]
        fields = ['id', 'name']
        self.project = self.sg.find_one('Project', filters, fields)

        print('---------------------------------project information---------------------------------')
        pprint(self.project)
        print('--------------------------------------------------------------------------------------')

    def get_sequence_and_upload(self):
        existing_sequence_codes = set()

        sequence_list = []

        project_id = self.project.get("id")

        filters = [['project', 'is', {'type': 'Project', 'id': project_id}]]
        fields = ['id', 'code']
        self.sequence = self.sg.find('Sequence', filters, fields)

        for sequence in self.sequence:
            existing_sequence_codes.add(sequence['code'])

        for data in self.xlsx_data:
            sequence_name = data['seq_name']
            if sequence_name is not None and sequence_name not in existing_sequence_codes:
                sequence_data = {
                    'code': sequence_name,
                    'project': {'type': 'Project', 'id': project_id}  # Replace with the actual project ID
                }
                new_sequence = self.sg.create('Sequence', sequence_data)
                sequence_list.append(new_sequence)
                existing_sequence_codes.add(sequence_name)

            elif sequence_name is not None:
                filters = [['project', 'is', {'type': 'Project', 'id': project_id}],
                           ['code', 'is', sequence_name]]
                fields = ['id', 'code']
                self.sequence = self.sg.find('Sequence', filters, fields)
                print(f"Sequence '{sequence_name}' already exists. Skipping creation.")

        if len(self.sequence) == 0:
            self.sequence = sequence_list

        print('---------------------------------sequence information---------------------------------')
        pprint(self.sequence)
        print('--------------------------------------------------------------------------------------')

    def get_shot_and_upload(self):
        existing_shot_codes = set()

        shot_list = []

        project_id = self.project.get('id')
        for seq in self.sequence:
            sequence_id = seq.get('id')
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project_id}],
                ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}]
            ]
            fields = ['id', 'code', 'sg_shot_type', 'sg_sequence', 'sg_scan_path', 'sg_ext']
            self.shot = self.sg.find('Shot', filters, fields)

        for one_shot in self.shot:
            existing_shot_codes.add(one_shot.get('code'))

        for data in self.xlsx_data:
            shot_code = data['shot_name']
            self.version_num = data['version']
            self.scan_path = data['scan_path']
            self.type = data['type']
            self.just_in = str(data['just_in'])
            self.just_out = str(data['just_out'])
            self.resolution = str(data['resolution'])
            self.ext = data['ext']
            self.start_frame = str(data['start_frame'])
            self.end_frame = str(data['end_frame'])
            self.duration = str(data['duration'])
            self.timecode_in = str(data['timecode_in'])
            self.timecode_out = str(data['timecode_out'])
            self.framerate = str(data['framerate'])
            self.date = str(data['date'])

            if shot_code is not None and shot_code not in existing_shot_codes:
                sequence_filters = [['id', 'is', seq.get('id')] for seq in self.sequence]
                sequence_entity = self.sg.find_one('Sequence', sequence_filters)
                shot_data = {
                    'code': shot_code,
                    'sg_sequence': sequence_entity,
                    'sg_scan_path': self.scan_path,
                    'sg_just_in': self.just_in,
                    'sg_just_out': self.just_out,
                    'sg_shot_type': self.type,
                    'sg_resolution': self.resolution,
                    'sg_ext': self.ext,
                    'sg_start_frame': self.start_frame,
                    'sg_end_frame': self.end_frame,
                    'sg_duration': self.duration,
                    'sg_timecode_in': self.timecode_in,
                    'sg_timecode_out': self.timecode_out,
                    'sg_framerate': self.framerate,
                    'sg_date': self.date,
                    'sg_version_number': self.version_num,
                    'project': {'type': 'Project', 'id': project_id}  # Replace with the actual project ID
                }
                new_shot = self.sg.create('Shot', shot_data)
                shot_list.append(new_shot)
                existing_shot_codes.add(shot_code)

            elif shot_code is not None:
                for seq in self.sequence:
                    sequence_id = seq.get('id')
                    filters = [
                        ['project', 'is', {'type': 'Project', 'id': project_id}],
                        ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],
                    ]
                    fields = ['id', 'code', 'sg_shot_type', 'sg_sequence', 'sg_scan_path', 'sg_ext', 'sg_version_number']
                    self.shot = self.sg.find('Shot', filters, fields)
                print(f"Shot '{shot_code}' already exists. Skipping creation.")

        if len(self.shot) == 0:
            self.shot = shot_list

        print('---------------------------------shot information---------------------------------')
        pprint(self.shot)
        print('----------------------------------------------------------------------------------')

    def copy_file_action(self):
        proj_name = self.project.get('name')
        proj_name = proj_name.upper()
        proj_name = proj_name[:3]

        for shot_info in self.shot:
            shot_type = shot_info.get('sg_shot_type')
            scan_file_path = shot_info.get('sg_scan_path')
            scan_file_list = os.listdir(scan_file_path)

            seq_name = shot_info.get('sg_sequence').get('name')
            shot_name = shot_info.get('code')

            ver_num = shot_info.get('sg_version_number')
            version_name = f'v{ver_num:03d}'

            if shot_type != 'org':
                another_path = os.path.join(self.home_root, self.project.get('name'), 'sequences', seq_name, shot_name,
                                            'plate', version_name, shot_type)

                if not os.path.exists(another_path):
                    os.makedirs(another_path)

                for orig_file_name in scan_file_list:
                    source_path = os.path.join(scan_file_path, orig_file_name)
                    target_path = os.path.join(another_path, orig_file_name)
                    if not os.path.exists(target_path):
                        shutil.copy2(source_path, target_path)

            else:
                work_path = os.path.join(self.home_root, self.project.get('name'), 'sequences', seq_name, shot_name, 'plate', version_name)
                org_path = os.path.join(work_path, 'org')

                if not os.path.exists(org_path):
                    os.makedirs(org_path)

                self.work_root.append(work_path)
                self.org_root.append(org_path)

                for orig_file_name in scan_file_list:
                    hash_num = orig_file_name.split('_')
                    hash_num = hash_num[-1].split('.')
                    convert_num = hash_num[-2].lstrip('0')

                    new_orig_name = f"{proj_name}_{seq_name}_{shot_name}_{version_name}_{convert_num}.{shot_info.get('sg_ext')}"

                    source_path = os.path.join(scan_file_path, orig_file_name)
                    target_path = os.path.join(org_path, new_orig_name)
                    if not os.path.exists(target_path):
                        shutil.copy2(source_path, target_path)

    def jpg_file_action(self):
        self.copy_file_action()

        proj_name = self.project.get('name')
        proj_name = proj_name.upper()
        proj_name = proj_name[:3]

        for dir_index, org_dir in enumerate(self.org_root):
            org_dir_path = os.listdir(org_dir)

            for origin_file in org_dir_path:
                jpg_dir_path = os.path.join(self.work_root[dir_index], 'jpg')

                if not os.path.exists(jpg_dir_path):
                    os.makedirs(jpg_dir_path)

                hash_num = origin_file.split('_')
                hash_num = hash_num[-1].split('.')
                convert_num = hash_num[-2].lstrip('0')

                ver_num = self.shot[dir_index].get('sg_version_number')
                version_name = f'v{ver_num:03d}'

                exr_file = os.path.join(self.org_root[dir_index], origin_file)
                jpg_file = os.path.join(jpg_dir_path,
                                        f"{proj_name}_{self.shot[dir_index].get('sg_sequence').get('name')}_{self.shot[dir_index].get('code')}_{version_name}_{convert_num}.jpg")

                if not os.path.exists(jpg_file):
                    ffmpeg_cmd = f"ffmpeg -i {exr_file} {jpg_file}"
                    subprocess.run(ffmpeg_cmd, shell=True)

    def mp4_file_action(self):
        self.jpg_file_action()
        for dir_index, work_dir in enumerate(self.work_root):
            jpg_file_path = os.path.join(work_dir, 'jpg')
            jpg_file_list = os.listdir(jpg_file_path)
            mp4_path = os.path.join(work_dir, 'mp4')

            if not os.path.exists(mp4_path):
                os.makedirs(mp4_path)

            jpg_file = jpg_file_list[dir_index]
            jpg_file_name = os.path.splitext(jpg_file)[0]
            mp4_file = '_'.join(jpg_file_name.split('_')[:-1])

            jpg_path = os.path.join(jpg_file_path, f'{mp4_file}_%04d.jpg')
            mp4_file_path = os.path.join(mp4_path, f'{mp4_file}.mp4')

            self.mp4_file_path_list.append(mp4_file_path)

            frame_start = 1001
            frame_end = frame_start + len(jpg_file_list) - 1

            if not os.path.exists(mp4_file_path):
                ffmpeg_cmd = f'ffmpeg -framerate 24 -start_number {frame_start} -i {jpg_path} -frames:v {frame_end} {mp4_file_path}'
                subprocess.run(ffmpeg_cmd, shell=True)

    def video_uploader(self):
        self.mp4_file_action()
        project_id = self.project.get('id')

        proj_name = self.project.get('name')
        proj_name = proj_name.upper()
        proj_name = proj_name[:3]

        for seq in self.sequence:
            sequence_id = seq.get('id')
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project_id}],
                ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],
                ['sg_shot_type', 'is', 'org']
            ]
            fields = ['id', 'code', 'sg_shot_type', 'sg_sequence', 'sg_scan_path', 'sg_ext', 'sg_version_number']
            self.shot = self.sg.find('Shot', filters, fields)

        for index, shot_info in enumerate(self.shot):
            shot_id = shot_info.get('id')
            shot_name = shot_info.get('code')
            seq_name = shot_info.get('sg_sequence').get('name')

            ver_num = shot_info.get('sg_version_number')
            version_name = f'v{ver_num:03d}'

            filters = [["entity", "is", {"type": "Shot", "id": shot_id}]]
            fields = ['id', 'code', 'sg_uploaded_movie', 'sg_status_list', 'sg_version_type', 'sg_path_to_movie']
            self.version = self.sg.find_one("Version", filters, fields)

            if self.version is None:
                version_data = {
                    'project': {'type': 'Project', 'id': project_id},
                    'entity': {'type': 'Shot', 'id': shot_id},
                    'code': f'{proj_name}_{seq_name}_{shot_name}_{version_name}',
                    'sg_status_list': 'na',
                    'sg_version_type': 'org',
                    'sg_path_to_movie': self.mp4_file_path_list[index],
                }
                self.version = self.sg.create("Version", version_data)
            else:
                print(f" Version '{self.version.get('code')}' already exists. Skipping creation.")

            mp4file_name = f'{proj_name}_{seq_name}_{shot_name}_{version_name}.mp4'

            uploaded_movie = self.version.get('sg_uploaded_movie')
            if uploaded_movie is None or uploaded_movie.get('name') != mp4file_name:
                self.sg.upload("Version", self.version.get('id'), self.mp4_file_path_list[index],
                               "sg_uploaded_movie")

            print('---------------------------------version information---------------------------------')
            pprint(self.version)
            print('-------------------------------------------------------------------------------------')


def main():
    test = LoadConvertModel()
    test.set_file_path('/TD/show/hanjin/production/excel/shots_list/hanjin.xlsx')
    test.data_info()
    test.get_project('hanjin')
    test.get_sequence_and_upload()
    test.get_shot_and_upload()
    test.video_uploader()


if __name__ == '__main__':
    main()