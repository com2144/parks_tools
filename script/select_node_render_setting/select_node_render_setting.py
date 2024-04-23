import hou

def select_count_node():
    selected_node = hou.selectedNodes()
    
    if not selected_node:
        warning_window('노드를 선택해야합니다!')
        return
        
    confirm_count = hou.ui.readInput('세팅할 노드의 개수를 적으세요.', buttons=('OK','Cancel'))
    
    if confirm_count[1] == '':
        warning_window('세팅할 노드의 개수를 숫자로 적으세요.')
        return
    
    int_count = int(confirm_count[1])
    
    node_path = selected_node[0].path()
    parent_node = hou.node(node_path)
    
    parent_geo = parent_node.geometry()
    geo_point = len(parent_geo.points())
    
    if int_count > geo_point:
        warning_window('현재 노드의 포인트 수보다 큽니다. 적은 수를 입력하세요.')
        return
    
    split_path = node_path.split('/')
    del split_path[-1]
    rejoin_path = '/'.join(split_path)
    
    for count in range(0, int_count):
        blast_node = hou.node(rejoin_path).createNode('blast',f'blast_{count}')
        blast_node.parm('group').set(str(count))
        blast_node.parm('negate').set(1)
        blast_node.setFirstInput(parent_node)
        blast_node.moveToGoodPosition()
        
        out_node = hou.node(rejoin_path).createNode('null', f'OUT_{count}')
        out_node.setFirstInput(blast_node)
        out_node.moveToGoodPosition()
        
        out_node_path = out_node.path()
        
        rend_geo = hou.node('/obj').createNode('geo', f'element_{count}')
        rend_geo.moveToGoodPosition()
        rend_geo_objmerge = rend_geo.createNode('object_merge', f'element_obj_{count}')
        rend_geo_objmerge.parm('objpath1').set(out_node_path)
        rend_geo_objmerge.parm('xformtype').set(1)
        rend_geo_objmerge.moveToGoodPosition()
        
        objmerge_out_node = rend_geo.createNode('null', f'OUT_{count}')
        objmerge_out_node.setFirstInput(rend_geo_objmerge)
        objmerge_out_node.moveToGoodPosition()
        objmerge_out_node.setRenderFlag(True)
        objmerge_out_node.setDisplayFlag(True)
        
        objmerge_out_path = objmerge_out_node.path()
        
        rend_out = hou.node('/out').createNode('ifd', f'element_rend_{count}')
        rend_out.parm('vobject').set('')
        rend_out.parm('forceobject').set(objmerge_out_path)
        rend_out.moveToGoodPosition()
        
def warning_window(message):
    hou.ui.displayMessage(message, severity=hou.severityType.ImportantMessage)
    
        
select_count_node()