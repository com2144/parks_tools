import hou

def center_pivot():
    selected_node = hou.selectedNodes()[0]
    
    node_path = selected_node.path()
    node = hou.node(node_path)
    
    node_type = node.type().name()
    
    if node_type == 'xform':
        pivot_translate = node.parmTuple('p')
        pivot_translate[0].setExpression('$CEX')
        pivot_translate[1].setExpression('$CEY')
        pivot_translate[2].setExpression('$CEZ')
    
        pivot_rotate = node.parmTuple('pr')
        pivot_rotate[0].setExpression('$CEX')
        pivot_rotate[1].setExpression('$CEY')
        pivot_rotate[2].setExpression('$CEZ')
    else:
        hou.ui.displayMessage('Choose the "transform" node', severity=hou.severityType.ImportantMessage)
            
center_pivot()