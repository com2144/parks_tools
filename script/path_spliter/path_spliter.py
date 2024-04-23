import hou

def split_node():
    selected_node = hou.selectedNodes()[0]
    
    if not selected_node:
        warning_window('노드를 선택해야합니다!')
        return
    
    node_path = selected_node.path()
    node = hou.node(node_path)
    
    geo = node.geometry()
    
    path_info = []
    
    for prim in geo.prims():
        path = prim.attribValue('path')
        path_split = path.split('/')
        path_split = path_split[4].split('_')
        if path_split[0] not in path_info:
            path_info.append(path_split[0])
            
    parent_path = node_path.split('/')
    del parent_path[-1]
    rejoin_path = '/'.join(parent_path)
    
    for value in path_info:
        blast_node = hou.node(rejoin_path).createNode('blast', f'blast_{value}')
        blast_node.parm('group').set(f'@path==*{value}*')
        blast_node.parm('negate').set(1)
        blast_node.setFirstInput(node)
        blast_node.moveToGoodPosition()
        
        out_node = hou.node(rejoin_path).createNode('null', f'OUT_{value}')
        out_node.setFirstInput(blast_node)
        out_node.moveToGoodPosition()

def warning_window(message):
    hou.ui.displayMessage(message, severity=hou.severityType.ImportantMessage)
        

split_node()