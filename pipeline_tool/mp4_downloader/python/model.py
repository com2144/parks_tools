from action_handler import *
import sys


class DownLoadModel:
    def __init__(self, argv):
        self.path = ''
        self.action_handle = ActionHandler(argv)

    def download_url_file(self, path):
        version_fields = ["id", "sg_uploaded_movie"]
        for sid in self.action_handle.selected_ids_filter:
            version = self.action_handle.sg.find_one(self.action_handle.entity_type, [sid], version_fields)
            mp4_down = path + '/' + version["sg_uploaded_movie"]["name"]
            mp4_filter = mp4_down.split('.')
            low_ext = mp4_filter[-1].lower()
            if low_ext != 'mp4':
                pass
            else:
                self.action_handle.sg.download_attachment(version["sg_uploaded_movie"], file_path=mp4_down)


def main():
    try:
        test = DownLoadModel(sys.argv)
        test.path = '/home/west/바탕화면'
        test.download_url_file(test.path)
    except IndexError as e:
        raise ShotgunActionException("Missing GET arguments")


if __name__ == '__main__':
    main()
