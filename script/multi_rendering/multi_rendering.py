import os
import platform
import json
import hou

import multi_rendering_ui
from multi_rendering_model import MultiRenderingModel


NOW_PATH = os.path.dirname( os.path.abspath(__file__) )


class MultiRendering:
    def __init__( self, preset_dict=None ):
        self.ui = multi_rendering_ui.MultRenderingUi()
        self.model = MultiRenderingModel()

        if preset_dict:
            self._set_preset( preset_dict )

        self.ui.plus_btn_func( lambda: self.node_tree_open() )
        self.ui.minus_btn_func( lambda: self.remove_select_item() )
        self.ui.up_btn_func( lambda: self.up_order_lb() )
        self.ui.down_btn_func( lambda: self.down_order_lb() )
        self.ui.all_render_chk_func( lambda toggled: self.render_check_action(toggled) )
        self.ui.render_btn_func( lambda: self.render_action() )
        self.ui.close_ui( lambda: self.ui.close() )

        self.ui.set_close_callback( self.save_table_data )


    def _set_preset( self, preset_dict ):
        render_tbl = self.ui.render_tbl
        column_count = render_tbl.columnCount()
        row_count = len( preset_dict['preset'] )

        render_tbl.setRowCount( row_count )

        tmp_tbl_list = []
        for row_idx, info in enumerate( preset_dict['preset'] ):
            wg_list = []
            for col_idx in range( column_count ):
                if col_idx == 0:
                    chkbox_item = multi_rendering_ui.CheckBoxWidget()
                    chkbox_item.chk_box.setCheckable( True )
                    chkbox_item.chk_box.setChecked( info[0] )
                    render_tbl.setCellWidget( row_idx, col_idx, chkbox_item )
                    wg_list.append( chkbox_item.chk_box )
                    
                elif col_idx == 1:
                    lb_item = multi_rendering_ui.LabelWidget()
                    lb_item.lb.setText( info[1] )
                    render_tbl.setCellWidget( row_idx, col_idx, lb_item )
                    wg_list.append( lb_item.lb )
                
                elif col_idx == 2:
                    order_lb_item = multi_rendering_ui.LabelWidget()
                    order_lb_item.lb.setText( info[2] )
                    render_tbl.setCellWidget( row_idx, col_idx, order_lb_item )
                    wg_list.append( order_lb_item.lb )

            tmp_tbl_list.append( wg_list )

        self.model.render_list = tmp_tbl_list


    def node_tree_open( self ):
        node_tree_dlg = multi_rendering_ui.NodeTreeDialog( parent=self.ui )
        node_tree_dlg.selectSignal.connect( self.node_tree_handle_select )
        node_tree_dlg.closeSignal.connect( self.node_tree_handle_cancel )
        node_tree_dlg.exec_()


    def node_tree_handle_select( self, selected_nodes ):
        node_list = []

        for node in selected_nodes:
            node_list.append( node )
        
        self._set_init_render_wg( node_list )


    def _set_init_render_wg( self, node_list ):
        render_tbl = self.ui.render_tbl
        column_count = render_tbl.columnCount()

        tmp_tbl_list = self.model.render_list

        duplicate_found_list = []
        if tmp_tbl_list:
            cleanup_node_list = []
            for node in node_list:
                node_path = node.path()
                duplicate_found = False
                for row in tmp_tbl_list:
                    if row[1].text() == node_path:
                        duplicate_found = True
                        duplicate_found_list.append( node_path )
                        break
                if not duplicate_found:
                    cleanup_node_list.append( node )
        else:
            cleanup_node_list = node_list

        current_row_count = render_tbl.rowCount()
        new_rows_count = len(cleanup_node_list)
        total_rows = current_row_count + new_rows_count

        render_tbl.setRowCount( total_rows )
        
        for idx, node in enumerate( cleanup_node_list ):
            row_idx = current_row_count + idx
            wg_list = []
            for col_idx in range( column_count ):
                if col_idx == 0:
                    chkbox_item = multi_rendering_ui.CheckBoxWidget()
                    chkbox_item.chk_box.setCheckable( True )
                    chkbox_item.chk_box.setChecked( False )
                    render_tbl.setCellWidget( row_idx, col_idx, chkbox_item )
                    wg_list.append( chkbox_item.chk_box )
                    
                elif col_idx == 1:
                    node_path = node.path()
                    lb_item = multi_rendering_ui.LabelWidget()
                    lb_item.lb.setText( node_path )
                    render_tbl.setCellWidget( row_idx, col_idx, lb_item )
                    wg_list.append( lb_item.lb )
                
                elif col_idx == 2:
                    order_lb_item = multi_rendering_ui.LabelWidget()
                    order_lb_item.lb.setText( str(row_idx + 1) )
                    render_tbl.setCellWidget( row_idx, col_idx, order_lb_item )
                    wg_list.append( order_lb_item.lb )

            tmp_tbl_list.append( wg_list )

        self.model.render_list = tmp_tbl_list

        if duplicate_found_list:
            duplicate_path = '\n'.join( duplicate_found_list )
            print( '='*20 )
            print( f'Already Set node !!\n\n{duplicate_path}' )
            print( '='*20 )


    def remove_select_item( self ):
        render_tbl = self.ui.render_tbl
        row_count = render_tbl.rowCount()
        remove_rows_list = []

        for row in range( row_count ):
            chkbox_container = render_tbl.cellWidget( row, 0 )
            if chkbox_container and chkbox_container.chk_box.isChecked():
                remove_rows_list.append( row )
        
        for row in sorted( remove_rows_list, reverse=True ):
            label_container = render_tbl.cellWidget(row, 2)
            removed_label = int(label_container.lb.text()) if label_container else None

            render_tbl.removeRow( row )
            self.model.render_list.pop( row )

            if removed_label is not None:
                for r in range( render_tbl.rowCount() ):
                    current_label_container = render_tbl.cellWidget(r, 2)
                    if current_label_container:
                        current_val = int( current_label_container.lb.text() )
                        if current_val > removed_label:
                            current_label_container.lb.setText( str(current_val - 1) )


    def get_single_selected_row(self):
        render_tbl = self.ui.render_tbl
        row_count = render_tbl.rowCount()
        selected_rows = []

        for row in range( row_count ):
            chk_widget = render_tbl.cellWidget( row, 0 )
            if chk_widget and chk_widget.chk_box.isChecked():
                selected_rows.append( row )
        
        if len(selected_rows) == 1:
            return selected_rows[0]
        else:
            hou.ui.displayMessage( f'Select the 1 node. now :: {len(selected_rows)}', severity=hou.severityType.Error )
            return None


    def up_order_lb( self ):
        render_tbl = self.ui.render_tbl
        row_count = render_tbl.rowCount()
        current_row = self.get_single_selected_row()

        if current_row is None:
            return

        current_lb_wg = render_tbl.cellWidget( current_row, 2 )
        current_val = int(current_lb_wg.lb.text())
        if current_val == 1:
            hou.ui.displayMessage( f'Already rank is up {current_val} order', 
                                    severity=hou.severityType.Warning )
            return

        target_row = None
        for row in range( row_count ):
            lb_wg = render_tbl.cellWidget( row, 2 )
            if lb_wg and int(lb_wg.lb.text()) == current_val - 1:
                target_row = row
                break
        
        target_lb_wg = render_tbl.cellWidget( target_row, 2 )

        current_lb_wg.lb.setText( str(current_val - 1) )
        target_lb_wg.lb.setText( str(current_val) )

        self.model.render_list[current_row], self.model.render_list[target_row] = \
            self.model.render_list[target_row], self.model.render_list[current_row]


    def down_order_lb( self ):
        render_tbl = self.ui.render_tbl
        row_count = render_tbl.rowCount()
        current_row = self.get_single_selected_row()

        if current_row is None:
            return
        
        current_lb_wg = render_tbl.cellWidget(current_row, 2)
        current_val = int(current_lb_wg.lb.text())
        if current_val == row_count:
            hou.ui.displayMessage( f'Already rank is down {current_val} order', 
                                    severity=hou.severityType.Warning )
            return

        target_row = None
        for row in range( row_count ):
            lb_wg = render_tbl.cellWidget( row, 2 )
            if lb_wg and int(lb_wg.lb.text()) == current_val + 1:
                target_row = row
                break
        
        target_lb_wg = render_tbl.cellWidget(target_row, 2)

        current_lb_wg.lb.setText( str(current_val + 1) )
        target_lb_wg.lb.setText( str(current_val) )

        self.model.render_list[current_row], self.model.render_list[current_row + 1] = \
            self.model.render_list[current_row + 1], self.model.render_list[current_row]


    def render_check_action( self, toggled ):
        render_tbl = self.ui.render_tbl
        row_count = render_tbl.rowCount()

        for row in range( row_count ):
            chk_wg = render_tbl.cellWidget( row, 0 )
            chk_wg.chk_box.setChecked( toggled )


    def node_tree_handle_cancel( self ):
        print( 'Node tree close' )


    def render_action( self ):
        sorted_list = sorted(self.model.render_list, key=lambda row: int(row[2].text()))

        path_confirm = False
        for chk_wg, path_lb_wg, _ in sorted_list:
            if chk_wg.isChecked():
                render_node = hou.node( str(path_lb_wg.text()) )
                if render_node.type().name() == 'ifd':
                    out_path = render_node.parm( 'vm_picture' ).eval()
                elif render_node.type().name() == 'usdrender_rop':
                    out_path = render_node.inputs()[0].parm( 'picture' ).eval()
                
                if not out_path:
                    path_confirm = True
                
                if not path_confirm:
                    render_node.parm( 'execute' ).pressButton()

                else:
                    hou.ui.displayMessage( f'Confirm the"{str(path_lb_wg.text())}" node output path', 
                                            severity=hou.severityType.Error )
                    return
        
        hou.ui.displayMessage( 'Rendering Done!' )

        self.save_table_data()


    def save_table_data( self ):
        sorted_list = sorted(self.model.render_list, key=lambda row: int(row[2].text()))
        for item in sorted_list:
            clean_infos = []
            clean_infos.append( item[0].isChecked() )
            clean_infos.append( str(item[1].text()) )
            clean_infos.append( str(item[2].text()) )

            self.model.preset_info_list.append( clean_infos )
        
        unique_by_both = []
        seen_keys = set()
        for row in self.model.preset_info_list:
            key = (row[1], row[2])
            if key not in seen_keys:
                seen_keys.add(key)
                unique_by_both.append(row)
        
        final_unique = []
        seen_paths = set()
        for row in unique_by_both:
            node_path = row[1]
            if node_path not in seen_paths:
                seen_paths.add(node_path)
                final_unique.append(row)

        final_unique.sort(key=lambda r: int(r[2]))
        for i, row in enumerate(final_unique):
            row[2] = i + 1

        self.model.preset_dict = { 'preset': final_unique }

        json_dir = os.path.join( NOW_PATH, '.preset' )
        if not os.path.exists( json_dir ):
            os.makedirs( json_dir )
        
        hip_file = hou.hipFile.path()
        if platform.system() == 'Windows':
            hip_file = hip_file.replace('/', '\\')
        
        if os.path.exists( hip_file ):
            hip_file_name, _ = os.path.splitext( os.path.basename(hip_file) )

            json_file = os.path.join( json_dir, f'{hip_file_name}.json')

            with open( json_file, 'w', encoding='utf-8' ) as file:
                json.dump( self.model.preset_dict, file, indent=4 )