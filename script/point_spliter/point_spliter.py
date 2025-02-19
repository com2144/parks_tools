import os
import hou


def load( data ):
    selected_node = hou.selectedNodes()

    if not selected_node:
        warning_window('Select the Node plz!')
        return
    
    selected_node = selected_node[0]
    
    node_path = selected_node.path()
    parent_path = os.path.dirname(node_path)
    node = hou.node(node_path)
    
    geo = node.geometry()

    if geo.findPointAttrib( data ):
        render = hou.ui.displayMessage('You want render setting??', 
                                       buttons=('OK', 'Cancel'), 
                                       title='Render setting')

        max_value = max(point.attribValue(data) for point in geo.points())

        if max_value:
            for i in range(max_value+1):
                blast_node = hou.node(parent_path).createNode('blast', f'blast_{data}_{i}')
                blast_node.parm('group').set(f'@{data}=={i}')
                blast_node.parm('negate').set(1)
                blast_node.setFirstInput(node)
                blast_node.moveToGoodPosition()

                out_node = hou.node(parent_path).createNode('null', f'OUT_{data}_{i}')
                out_node.setFirstInput(blast_node)
                out_node.moveToGoodPosition()

                if render == 0:
                    out_node_path = out_node.path()
                    
                    rend_geo = hou.node('/obj').createNode('geo', f'{data}_{i}')
                    rend_geo.moveToGoodPosition()
                    rend_geo_objmerge = rend_geo.createNode('object_merge', f'{data}_obj_{i}')
                    rend_geo_objmerge.parm('objpath1').set(out_node_path)
                    rend_geo_objmerge.parm('xformtype').set(1)
                    rend_geo_objmerge.moveToGoodPosition()
                    
                    objmerge_out_node = rend_geo.createNode('null', f'OUT_{i}')
                    objmerge_out_node.setFirstInput(rend_geo_objmerge)
                    objmerge_out_node.moveToGoodPosition()
                    objmerge_out_node.setRenderFlag(True)
                    objmerge_out_node.setDisplayFlag(True)
                    
                    objmerge_out_path = objmerge_out_node.path()
                    
                    rend_out = hou.node('/out').createNode('ifd', f'{data}_rend_{i}')
                    rend_out.parm('vobject').set('')
                    rend_out.parm('forceobject').set(objmerge_out_path)
                    rend_out.moveToGoodPosition()

        else:
            warning_window(f'point cluster is "{max_value}".')

    else:
        warning_window(f'"{data}" point attrib is not exists.')


def warning_window(message):
    hou.ui.displayMessage(message, severity=hou.severityType.ImportantMessage)