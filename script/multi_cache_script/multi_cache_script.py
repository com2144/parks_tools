import hou
import os


def task_chk(node):
    check = node.parm("cache_list_check").eval()
    instance_count = get_multiparm_instance_count(node, "cache_check")
    
    for idx in range( instance_count ):
        node.parm(f"cache_check{idx+1}").set(check)


def get_multiparm_instance_count(node, base_name):
    count = 0
    while True:
        parm = node.parm(f"{base_name}{count+1}")
        if parm is None:
            break
        count += 1
    return count


def selectnode(node, parm_index):
    select_cache_node = hou.ui.selectNode(node_type_filter=hou.nodeTypeFilter.Sop, title='Choose the Filecache Node')
    cache_node = hou.node(select_cache_node)
    
    if cache_node is not None:
        cache_range = cache_node.parmTuple('f').eval()
        cache_node_type = cache_node.type().name()
        
        path_parm = node.parm(f"path{parm_index}")
        range_parm = node.parmTuple(f'range{parm_index}_')
        
        if cache_node_type == 'filecache::2.0' and path_parm.eval() != select_cache_node:
            path_parm.set(select_cache_node)
            range_parm.set((cache_range[0], cache_range[1]))
            statuscolor(node, parm_index)
            
        elif path_parm.eval() == select_cache_node:
            message_window('이미 선택한 node입니다.')
            
        else:
            message_window('filecache node를 선택해주세요.')
            
    else:
        message_window('filecache node를 선택해주세요.')

        
def drag_node(node, parm_index):
    path = node.parm(f"path{parm_index}").eval()
    cache_node = hou.node(path)
    
    if cache_node is not None:
        cache_range = cache_node.parmTuple('f').eval()
        cache_node_type = cache_node.type().name()
    
        path_parm = node.parm(f"path{parm_index}")
        range_parm = node.parmTuple(f'range{parm_index}_')
        
        if cache_node_type == 'filecache::2.0':
            range_parm = node.parmTuple(f'range{parm_index}_')
            range_parm.set((cache_range[0],cache_range[1]))
            statuscolor(node, parm_index)
            
        else:
            path_parm.set('')
            hou.ui.displayMessage('filecache node를 선택하세요.')    

            
def openPath(node, parm_index):
    if node.parm(f"path{parm_index}").eval():
        filecache_node = node.parm(f"path{parm_index}").evalAsNode() # select file cache node
        filepath = filecache_node.parm("sopoutput").eval()
        
        split_path = filepath.split("/")
        split_path.reverse()
        
        dir_path = filepath.replace(split_path[0],"")
            
        if os.path.exists(dir_path):
            hou.ui.showInFileBrowser(dir_path)
            
        else:
            message_window(f'{dir_path}의 경로를 찾을 수 없습니다.')
    else:
        message_window(f'{node.parm("path"+parm_index).name()}가 비어있습니다.')        

        
def set_origin(node, parm_index):
    range_parm = node.parmTuple(f"range{parm_index}_")
    path = node.parm(f"path{parm_index}").evalAsNode()
    
    path.parmTuple('f').revertToDefaults()
    orig_range = path.parmTuple('f').eval()
    range_parm.set((orig_range[0],orig_range[1]))
    
    statuscolor(node, parm_index)

    
def set_override(node, parm_index):
    range_parm = node.parmTuple(f"range{parm_index}_")
    path = node.parm(f"path{parm_index}").evalAsNode()
    
    frame_in = range_parm.eval()
    origin_frame = path.parmTuple('f')
    origin_frame.deleteAllKeyframes()
    origin_frame.set((frame_in[0],frame_in[1],1))
    
    statuscolor(node, parm_index)

    
def exec_cache(folder_count):
    node = hou.pwd()
    for i in range(folder_count):
        check = node.parm('cache_check'+str(i+1)).eval()
        cache_node = node.parm('path'+str(i+1)).evalAsNode()
        if check == 1 and cache_node is not None:
            origin_name = cache_node.parm('basename').rawValue()
            cache_node.parm('execute').pressButton()
            cache_node.parm('loadfromdisk').set(1)
            cache_node.parm('reload').pressButton()
            cache_node.parm('basename').set(origin_name)
            statuscolor(node, str(i+1))
            
    message_window('Cache가 완료되었습니다.')

    
def statuscolor(node, parm_index):
    cache_node = node.parm(f"path{parm_index}").evalAsNode()
    cache_range = cache_node.parmTuple('f').eval()

    filepath = cache_node.parm("sopoutput").eval()
    
    split_path = filepath.split("/")
    split_path.reverse()
    
    dir_path = filepath.replace(split_path[0],"")
    
    
    if os.path.exists(dir_path) and len(os.listdir(dir_path)) == int(cache_range[1]-cache_range[0]+1):
        node.parmTuple(f'status{parm_index}').set((0,1,0))
        
    elif os.path.exists(dir_path) and len(os.listdir(dir_path)) != int(cache_range[1]-cache_range[0]+1):
        node.parmTuple(f'status{parm_index}').set((1,1,0))
        
    else:
        node.parmTuple(f'status{parm_index}').set((1,0,0))  

        
def message_window(message):
    hou.ui.displayMessage(message, severity=hou.severityType.ImportantMessage)