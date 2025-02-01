import os

from constant import *


class Rename:
    def __init__( self, model, gui_module, main_ui ):
        self.model = model
        self.gui_module = gui_module
        self.ui = main_ui

        self.rn_list = []
    

    def add_item( self ):
        rn_tbl = self.ui.rename_tbl
        row_count = rn_tbl.rowCount()
        column_count = rn_tbl.columnCount()

        rn_tbl.setRowCount( row_count + 1)

        wg_list = []
        for col_idx in range( column_count ):
            if col_idx == 0:
                sr_item = self.gui_module.LineEditWidget()
                rn_tbl.setCellWidget( row_count, col_idx, sr_item )
                wg_list.append( sr_item.line_edt )
            
            elif col_idx == 1:
                tr_item = self.gui_module.LineEditWidget()
                rn_tbl.setCellWidget( row_count, col_idx, tr_item )
                wg_list.append( tr_item.line_edt )
        
        self.rn_list.append( wg_list )
    

    def remove_item( self ):
        rn_tbl = self.ui.rename_tbl
        row_count = rn_tbl.rowCount()

        if row_count > 0:
            rn_tbl.removeRow( row_count - 1 )
            self.rn_list.pop()
    

    def rename_info( self, data_list):
        error_list = []
        for data in data_list:
            chk, file_path, _, _, ext, _ = data
            for sr, tr in self.rn_list:
                search_txt = str(sr.text())
                target_txt = str(tr.text())

                if chk:
                    if ext in FORMAT[1:]:
                        file_name = os.path.basename( file_path )
                        file_split = file_name.split('_')
                        file_name = '_'.join( file_split[:-1] )
                        ver = file_split[-1]
                    else:
                        ver = ''
                        
                    if search_txt not in file_name:
                        error_list.append( f'"{search_txt}" not in "{file_name}"')
                    
                    if not error_list:
                        file_name = file_name.replace( search_txt, target_txt)
                        if ver:
                            file_name += '_' + ver

            data[1] = file_name

        if error_list:
            error_msg = ('=' * 10) + '\n'
            error_msg += '\n'.join( error_list ) +'\n'
            error_msg += ('=' * 10)
            return { 'rename_error': error_msg }

        return data_list


                        

