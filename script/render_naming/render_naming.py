import os
import re
import hou


from render_naming_model import RenderNamingModel
import render_nameing_ui


class RenderNaming:
    def __init__( self, nodes ):
        self.selected_nodes = nodes
        self.model = RenderNamingModel()
        self.ui = render_nameing_ui.RenderNamingUI()
        self.valid = True

        self.select_nodelist = self.get_sel_nodes()
        if not self.select_nodelist:
            self.valid = False
            return
        
        self._set_sel_tbl()

        self.ui.write_func( lambda: self.write_naming_action() )
        self.ui.close_ui( lambda: self.ui.close() )


    def get_sel_nodes( self ):
        tmp_node_list = []
        
        file_name = os.path.basename( hou.hipFile.path() )
        pattern = r"^(?P<name>.+)_shot_work_fx_v\d{3}\.(hiplc|hipnc|hip)$"
        match = re.match(pattern, file_name)
        if not match:
            hou.ui.displayMessage( f'This scene file is Wrong naming :: {file_name}', 
                    severity=hou.severityType.Error )
            return None
        else:
            self.model.hip_file_name = file_name

        for node in self.selected_nodes:
            if node.parent().type().name() not in [ 'out', 'stage' ]:
                hou.ui.displayMessage( 'Select the "out" or "stage" node', 
                        severity=hou.severityType.Error )
                return None
            
            if node.parent().type().name() == 'out' and node.type().name() not in [ 'ifd' ]:
                hou.ui.displayMessage( 'Select the "mantra" node', 
                    severity=hou.severityType.Error )
                return None
            
            if node.parent().type().name() == 'stage':
                if node.type().name() != 'usdrender_rop':
                    hou.ui.displayMessage( 'Select the "usdrender_rop" node', 
                        severity=hou.severityType.Error )
                    return
                
                if node.input(0).type().name() not in [ 'karmarenderproperties' ]:
                    hou.ui.displayMessage( 'Link the "karmarendersettings" node', 
                        severity=hou.severityType.Error )
                    return None
            
            tmp_node_list.append( node )
        return tmp_node_list


    def _set_sel_tbl( self ):
        if self.select_nodelist:
            render_tbl = self.ui.render_tbl
            row_count = len( self.select_nodelist )
            column_count = render_tbl.columnCount()

            render_tbl.setRowCount( row_count )

            tmp_tbl_list = []
            for row_idx, select_node in enumerate(self.select_nodelist):
                wg_list = []
                for col_idx in range( column_count ):
                    if col_idx == 0:
                        chkbox_item = render_nameing_ui.CheckBoxWidget()
                        chkbox_item.chk_box.setCheckable( True )
                        chkbox_item.chk_box.setChecked( True )
                        render_tbl.setCellWidget( row_idx, col_idx, chkbox_item )
                        wg_list.append( chkbox_item.chk_box )
                    
                    elif col_idx == 1:
                        lb_item = render_nameing_ui.LabelWidget()
                        lb_item.lb.setText( select_node.path() )
                        render_tbl.setCellWidget( row_idx, col_idx, lb_item )
                        wg_list.append( lb_item.lb )

                    elif col_idx == 2:
                        line_item = render_nameing_ui.LineEditWidget()
                        render_tbl.setCellWidget( row_idx, col_idx, line_item)
                        wg_list.append( line_item.line_edt )     
                        
                tmp_tbl_list.append( wg_list )
            
            self.model.select_data_list = tmp_tbl_list


    def write_naming_action( self ):
        error_node_list = []
        for chk, path, info in self.model.select_data_list:
            if chk.isChecked():
                render_node = hou.node( str(path.text()) )

                ver_chk_node_path = f'/{render_node.parent().name()}/adjust_version'
                ver_chk_node = hou.node( ver_chk_node_path )

                if ver_chk_node is None:
                    ver_chk_null = hou.node( f'/{render_node.parent().name()}').createNode( 'null', 'adjust_version' )
                    
                    parm_group = ver_chk_null.parmTemplateGroup()
                    ver_parm = hou.IntParmTemplate( 'version', 'Version', 1, default_value=(0,))

                    if not ver_chk_null.parm( 'version' ):
                        parm_group.append( ver_parm )
                    
                    ver_chk_null.setParmTemplateGroup( parm_group )

                    ver_chk_null.parm( 'version' ).set(1)
                    ver_chk_null.setColor( hou.Color((1.0, 0.0, 0.0)) )
                    ver_chk_null.setUserData( "nodeshape", "circle" )
                    ver_chk_null.moveToGoodPosition()
                
                if render_node.parent().name() == 'stage':
                    if str(info.text()):
                        parent_node = render_node.input(0)
                        parent_node.setName( str(info.text()))
                        
                        _, ext = os.path.splitext( os.path.basename(parent_node.parm( 'picture' ).rawValue()) )
                        ext = ext[1:]
                        review_path = os.path.dirname(hou.hscriptExpression('$HIP')) + '/review'

                        parent_node.parm( 'picture' ).set(f'{review_path}/{ext}/$OS/v`padzero(3,chs("../adjust_version/version"))`'
                                                          f'/$OS.v`padzero(3,chs("../adjust_version/version"))`.$F4.{ext}')
                    
                    else:
                        error_node_list.append( f'"{render_node.name()}" is empty element name')
                
                elif render_node.parent().name() == 'out':
                    if str(info.text()):
                        render_node.setName( str(info.text()))
                        _, ext = os.path.splitext( os.path.basename(render_node.parm( 'vm_picture' ).rawValue()) )
                        ext = ext[1:]
                        review_path = os.path.dirname(hou.hscriptExpression('$HIP')) + '/review'

                        render_node.parm( 'vm_picture' ).set(f'{review_path}/{ext}/$OS/v`padzero(3,chs("../adjust_version/version"))`'
                                                             f'/$OS.v`padzero(3,chs("../adjust_version/version"))`.$F4.{ext}')
                        
                    else:
                        error_node_list.append( f'"{render_node.name()}" is empty element name')
        
        if error_node_list:
            msg = '\n'.join( error_node_list )
            hou.ui.displayMessage( f'----- Warning Message -----\n{msg}', 
                severity=hou.severityType.Warning )
        else:
            hou.ui.displayMessage( 'Render Node Naming Done!' )