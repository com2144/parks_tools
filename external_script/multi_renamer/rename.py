import os
import sys
import shutil
import copy

from rename_model import RenameModel
import rename_ui


class Rename:
    def __init__(self):
        self.ui = rename_ui.RenameUi()
        self.file_list = None
        
        self.model = RenameModel() 
        
        self.ui.dir_path_btn.clicked.connect( self._set_rename_path )
        self.ui.plus_btn.clicked.connect( self.add_item )
        self.ui.minus_btn.clicked.connect( self.remove_item )
        self.ui.run_btn.clicked.connect( self.rename_run )
        self.ui.cancel_btn.clicked.connect( self.ui.close )
    

    def _set_rename_path( self ):
        home_path = os.path.expanduser( '~' )
        self.model.save_path = rename_ui.QFileDialog.getExistingDirectory(
            self.ui,
            'Select Directory',
            home_path
        )

        self.ui.dir_path_line.setText( self.model.save_path )

        if self.model.save_path:
            file_list = [ file for file in os.listdir(self.model.save_path)
                            if os.path.splitext(file)[-1].lower() in self.model.filter_ext ]
        else:
            self.ui.message_box( 'error', 'Empty save path', 'Select the save path.')
            return

        if not self.file_list: 
            self.file_list = rename_ui.FileListWidget( self.ui )
            self.file_list.list_view.addItems( file_list )
            self.file_list.show()
            self.file_list.setAttribute( rename_ui.Qt.WA_DeleteOnClose )
            self.file_list.destroyed.connect( lambda : setattr(self, 'file_list', None) )
        elif self.file_list.isVisible():
            self.file_list.close()
            self.file_list = rename_ui.FileListWidget( self.ui )
            self.file_list.list_view.addItems( file_list )
            self.file_list.show()


    def add_item( self ):
        if self.model.save_path:
            rn_tbl = self.ui.rename_tbl
            row_count = rn_tbl.rowCount()
            column_count = rn_tbl.columnCount()

            rn_tbl.setRowCount( row_count + 1 )

            wg_list = []
            for col_idx in range( column_count ):
                if col_idx == 0:
                    chkbox_item = rename_ui.CheckBoxWidget()
                    chkbox_item.chk_box.setCheckable( True )
                    chkbox_item.chk_box.setChecked( False )
                    rn_tbl.setCellWidget( row_count, col_idx, chkbox_item )
                    wg_list.append( chkbox_item.chk_box )
                
                elif col_idx == 1:
                    source_item = rename_ui.LineEditWidget()
                    rn_tbl.setCellWidget( row_count, col_idx, source_item )
                    wg_list.append( source_item.line_edt )
                
                elif col_idx == 2:
                    target_item = rename_ui.LineEditWidget()
                    rn_tbl.setCellWidget( row_count, col_idx, target_item )
                    wg_list.append( target_item.line_edt )
            
            self.model.rn_list.append( wg_list )
        
        else:
            self.ui.message_box( 'error', 'Add Rename item error', 'Set the directory path.')


    def remove_item( self ):
        if self.model.save_path:
            rn_tbl = self.ui.rename_tbl
            row_count = rn_tbl.rowCount()

            if row_count > 0:
                rn_tbl.removeRow( row_count -1 )
                self.model.rn_list.pop()
        
        else:
            self.ui.message_box( 'error', 'Remove Rename item error', 'Set the directory path.')


    def rename_run( self ):
        origin_path_list = [ os.path.join(self.model.save_path, file).replace('/', '\\') 
                            for file in os.listdir(self.model.save_path)
                            if os.path.splitext(file)[-1].lower() in self.model.filter_ext ]

        target_path_list = self.rename_info( origin_path_list, self.model.rn_list )

        if isinstance( target_path_list, dict ):
            self.ui.message_box( 'error', 'Rename Info Error', target_path_list['rename_error'] )
            return
        
        elif len(origin_path_list) > 1000:
            tmp_count = 0

            for origin_path, target_path in zip(origin_path_list, target_path_list):
                origin_path_dir = os.path.dirname( origin_path )
                target_path_dir = os.path.dirname( target_path )
         
                if origin_path_dir != target_path_dir:
                    if not os.path.exists( target_path_dir ):
                        os.makedirs( target_path_dir, 0o755 )
                    
                    shutil.move( origin_path, target_path )
                    
                    if len( os.listdir(origin_path_dir) ) == 0:
                        os.rmdir( origin_path_dir )

                else:
                    target_path_tmp_dir = target_path_dir + '_tmp'
                    target_file_name, ext = os.path.splitext(target_path)
                    target_tmp_file = target_file_name + '_tmp' + ext

                    target_tmp_path = os.path.join( target_path_tmp_dir, target_tmp_file )

                    if not os.path.exists( target_path_tmp_dir ):
                        os.makedirs( target_path_tmp_dir, 0o755 )
                    
                    shutil.move( origin_path, target_tmp_path )

                    if len( os.listdir(origin_path_dir) ) == 0:
                        os.rmdir( origin_path_dir )

                    tmp_count += 1

                    if tmp_count == len( os.listdir(target_path_tmp_dir) ):
                        shutil.copy2( target_tmp_path, target_path )

                        if len( os.listdir(target_path_tmp_dir) ) == len( os.listdir(target_path_dir) ):
                            os.rmdir( target_path_tmp_dir )
                    
        else:
            for origin_path, target_path in zip(origin_path_list, target_path_list):
                origin_path_dir = os.path.dirname( origin_path )
                target_path_dir = os.path.dirname( target_path )

                if origin_path_dir != target_path_dir:
                    if not os.path.exists( target_path_dir ):
                        os.makedirs( target_path_dir, 0o755 )
                    
                    shutil.move( origin_path, target_path )
                    
                    if len( origin_path_list ) == 0:
                        os.rmdir( origin_path_dir )

                else:
                    shutil.move( origin_path, target_path )
        
        self.ui.message_box( 'info', 'Rename Info', 'Rename is success' )
        self.init_ui_set()


    def rename_info( self, origin_info, rn_list ):
        error_list = []
        updated_list = copy.copy( origin_info )
        for dir_chk, sr, tr in rn_list:
            is_dir_chk = dir_chk.isChecked()
            source_txt = str(sr.text())
            target_txt = str(tr.text())

            for idx, origin_path in enumerate( updated_list ):
                parent_dir = os.path.dirname( os.path.dirname(origin_path) )
                parent_dir_name = origin_path.split( os.sep )[-2]
                origin_file_name, ext = os.path.splitext( os.path.basename(origin_path) )

                if not source_txt and not target_txt:
                    error_list.append( f'[{idx}] source and target input the letter.')

                if source_txt not in origin_path:
                    error_list.append( f'[{idx}] "{source_txt}" not in {origin_path}' )
                
                if not error_list:
                    if is_dir_chk:
                        new_path = os.path.join(
                            parent_dir,
                            parent_dir_name.replace( source_txt, target_txt ),
                            origin_file_name.replace( source_txt, target_txt ) + ext
                        )

                    else:
                        new_path = os.path.join(
                            os.path.dirname( origin_path ),
                            origin_file_name.replace( source_txt, target_txt ) + ext
                        )
                    
                    updated_list[idx] = new_path.replace('/','\\')
        
        if error_list:
            error_msg = ('=' * 10) + '\n'
            error_msg += '\n'.join( error_list ) + '\n'
            error_msg += ('=' * 10)
            return { 'rename_error': error_msg }
        else:
            return updated_list


    def init_ui_set( self ):
        self.ui.dir_path_line.setText('')
        self.model.save_path = ''

        rn_tbl = self.ui.rename_tbl
        row_count = rn_tbl.rowCount()

        if row_count > 0:
            rn_tbl.clearContents()
            rn_tbl.setRowCount(0)
            self.model.rn_list = []

        self.file_list.close()        



if __name__ == '__main__':
    app = rename_ui.QApplication( sys.argv )

    rn = Rename()

    main_ui = rn.ui
    main_ui.show()

    sys.exit( app.exec_())