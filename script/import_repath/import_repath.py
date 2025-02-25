import hou

import os
import copy


import  import_repath_ui
from    import_repath_model     import ImportRepathModel


class ImportRepath:
    def __init__( self, nodes ):
        self.selected_nodes = nodes
        self.model = ImportRepathModel()
        self.ui = import_repath_ui.ImportRepathUi()

        self._set_sel_tbl()
        self._set_init_rn_wg()

        self.ui.add_rn_item_func( lambda: self.add_item() )
        self.ui.minus_rn_item_func( lambda: self.remove_item() )
        self.ui.replace_func( lambda: self.replace_action())
        self.ui.close_ui( lambda: self.ui.close() )


    def _get_selected_node( self ):
        tmp_node_list = []

        for node in self.selected_nodes:
            if node.parent().type().name() != 'geo':
                hou.ui.displayMessage( 'Select the geometry node', 
                                        severity=hou.severityType.Error )
                return
            
            elif node.type().name() not in self.model.node_type_list:
                hou.ui.displayMessage( f'Select the "{self.model.node_type_list}" nodes', 
                                            severity=hou.severityType.Error )
                return
            
            else:
                tmp_node_list.append( node )
        
        self.model.select_node_list = tmp_node_list


    def _set_sel_tbl( self, replace=False ):
        if not replace:
            self._get_selected_node()

        if self.model.select_node_list:
            sel_tbl = self.ui.sel_tbl
            row_count = len( self.model.select_node_list )
            column_count = sel_tbl.columnCount()

            sel_tbl.setRowCount( row_count )

            tmp_tbl_list = []
            for row_idx, select_node in enumerate(self.model.select_node_list):
                wg_list = []
                for col_idx in range( column_count ):
                    if col_idx == 0:
                        chkbox_item = import_repath_ui.CheckBoxWidget()
                        chkbox_item.chk_box.setCheckable( True )
                        chkbox_item.chk_box.setChecked( True )
                        sel_tbl.setCellWidget( row_idx, col_idx, chkbox_item )
                        wg_list.append( chkbox_item.chk_box.isChecked() )
                    
                    elif col_idx == 1:
                        node_name = hou.node( select_node.path() ).name()
                        name_lb_item = import_repath_ui.LabelWidget()
                        name_lb_item.lb.setText( node_name )
                        sel_tbl.setCellWidget( row_idx, col_idx, name_lb_item )

                    elif col_idx == 2:
                        node = hou.node( select_node.path() )
                        path_lb_item = import_repath_ui.LabelWidget()
                        
                        if select_node.type().name() == 'alembic':
                            path_lb_item.lb.setText( node.parm('fileName').eval() )
                            wg_list.append( node.parm('fileName') )
                        
                        elif select_node.type().name() == 'file':
                            path_lb_item.lb.setText( node.parm('file').eval() )
                            wg_list.append( node.parm('file') )

                        elif select_node.type().name() == 'usdimport':
                            path_lb_item.lb.setText( node.parm('usdimport').eval() )
                            wg_list.append( node.parm('usdimport') )
                        
                        sel_tbl.setCellWidget( row_idx, col_idx, path_lb_item )
                    
                tmp_tbl_list.append( wg_list )
            
            self.model.select_data_list = tmp_tbl_list 


    def _set_init_rn_wg( self ):
        rn_tbl = self.ui.rn_tbl
        column_count = rn_tbl.columnCount()

        rn_tbl.setRowCount( 1 )

        wg_list = []
        for col_idx in range( column_count ):
            if col_idx == 0:
                orig_item = import_repath_ui.LineEditWidget()
                rn_tbl.setCellWidget( 0, col_idx, orig_item )
                wg_list.append( orig_item.line_edt )
            
            elif col_idx == 1:
                tr_item = import_repath_ui.LineEditWidget()
                rn_tbl.setCellWidget( 0, col_idx, tr_item )
                wg_list.append( tr_item.line_edt )
        
        self.model.rn_list.append( wg_list )


    def add_item( self ):
        rn_tbl = self.ui.rn_tbl
        row_count = rn_tbl.rowCount()
        column_count = rn_tbl.columnCount()

        rn_tbl.setRowCount( row_count + 1 )

        wg_list = []
        for col_idx in range( column_count ):
            if col_idx == 0:
                orig_item = import_repath_ui.LineEditWidget()
                rn_tbl.setCellWidget( row_count, col_idx, orig_item )
                wg_list.append( orig_item.line_edt )
            
            elif col_idx == 1:
                tr_item = import_repath_ui.LineEditWidget()
                rn_tbl.setCellWidget( row_count, col_idx, tr_item )
                wg_list.append( tr_item.line_edt )
        
        self.model.rn_list.append( wg_list )


    def remove_item( self ):
        rn_tbl = self.ui.rn_tbl
        row_count = rn_tbl.rowCount()

        if row_count > 1:
            rn_tbl.removeRow( row_count -1 )
            self.model.rn_list.pop()


    def replace_action( self ):
        target_node_list = self.rn_info( self.model.select_data_list, 
                                        self.model.rn_list )
        
        if isinstance( target_node_list, dict ):
            hou.ui.displayMessage( target_node_list['rename_error'], 
                        severity=hou.severityType.Error )
            return
        
        else:
            self.ui.sel_tbl.clear()
            self.model.select_data_list = []
            self._set_sel_tbl( replace=True )
            self.ui.rn_tbl.clear()
            self.model.rn_list = []
            self._set_init_rn_wg()
            
            hou.ui.displayMessage( 'RePath is success.',
                                  severity=hou.severityType.Message )


    def rn_info( self, node_path_list, rn_item_list ):
        error_list = []
        updated_list = copy.copy( node_path_list )

        for sr, tr in rn_item_list:
            source_txt = str( sr.text() )
            target_txt = str( tr.text() )

            for idx, item in enumerate( updated_list ):
                if item[0]:
                    path, ext = os.path.splitext( item[1].eval() )

                    if not source_txt and target_txt:
                        error_list.append( f'[{idx}] source and target input the letter.' )
                    
                    if source_txt not in item[1].eval():
                        error_list.append( f'[{idx}] "{source_txt}" not in {item[1].eval()}' )
                    
                    if not error_list:
                        new_path = f'{path.replace(source_txt, target_txt)}{ext}'
                        updated_list[idx][1].set( new_path )
        
        if error_list:
            error_msg = ('=' * 10) + '\n'
            error_msg += '\n'.join( error_list ) + '\n'
            error_msg += ('=' * 10)

            return { 'rename_error': error_msg }
        else:        
            return updated_list
