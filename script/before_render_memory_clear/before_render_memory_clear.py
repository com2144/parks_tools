import hou

def memory_clear():
    now_proj_file = hou.hipFile.path()
    hou.hipFile.save(now_proj_file, save_to_recent_files=True)
    hou.hipFile.load(now_proj_file)

memory_clear()