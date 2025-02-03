import os
import sys
import shutil

import copyer_ui
from copyer_model import CopyerModel


class Copyer:
    def __init__( self ):
        self.ui = copyer_ui.CopyUi()
        self.model = CopyerModel()

        self.log = None

        self.ui.orig_tbl.itemsDropped.connect( self.otl_get_content )
        self.ui.orig_tbl.itemsUpdated.connect( self.otl_update_content )

        self.ui.target_tbl.itemsDropped.connect( self.ttl_get_content )
        self.ui.target_tbl.itemsUpdated.connect( self.ttl_update_content )

        self.ui.log_chk.toggled.connect( self.log_sig )
        self.ui.orig_clear_btn.clicked.connect( self.orig_clear )
        self.ui.copy_btn.clicked.connect( self.copy_act )
        self.ui.cancel_btn.clicked.connect( self.ui.close )

    
    def otl_get_content( self, items ):
        warning_msg = []


        for item in items:
            if item in self.model.orig_path_list:
                warning_msg.append( f'Already exists :: {item}' )

            elif os.path.isdir( item ) and len( os.listdir( item ) ) == 0:
                warning_msg.append( f'Folder is empty :: {item}' )

            elif os.path.isfile( item ):
                file = os.path.basename( item )
                ext = os.path.splitext( file )[-1]

                if ext.lower() not in self.model.ext_list:
                    warning_msg.append( f'Not support {ext} format :: {item}' )

                else:
                    self.model.orig_path_list.append( item )
            
            else:
                self.model.orig_path_list.append( item )
        
        if self.log:
            if warning_msg:
                self.log.set_log( warning_msg )

            for orig_path in self.model.orig_path_list:
                self.log.set_log( f'set origin path :: {orig_path}' )
        
        if warning_msg:
            self.ui.message_box( 'warning', 'Orig Warning', '\n'.join(warning_msg) )
        
        self.ui.orig_tbl.add_items( self.model.orig_path_list )


    def otl_update_content( self, items ):
        self.model.orig_path_list = items

        if self.log:
            msg = 'source list\n'
            msg += ('=' * 10) + '\n' 
            msg += '\n'.join( self.model.orig_path_list )
            msg += ('=' * 10) + '\n'

            self.log.set_log( msg )


    def ttl_get_content( self, items ):
        self.ui.target_tbl.clear()

        if os.path.isdir( items[0] ):
            self.model.target_path_list = items

            self.ui.target_tbl.add_item( self.model.target_path_list )

            if self.log:
                for target_path in self.model.target_path_list:
                    self.log.set_log( f'set target path :: {target_path}' )
        
        else:
            if self.log:
                self.log.set_log( 'Input the Folder' )

            self.ui.message_box( 'error', 'Traget Type Error', 'Input the Folder' )

    
    def ttl_update_content( self, items ):
        self.model.target_path_list = items

        if self.log:
            msg = 'target path\n'
            msg += ('=' * 10) + '\n' 
            msg += '\n'.join( self.model.target_path_list )
            msg += ('=' * 10) + '\n'

            self.log.set_log( msg )


    def log_sig( self ):
        if self.ui.log_chk.isChecked():
            self.log = copyer_ui.LogListView( self.ui )
            self.log.show()
        else:
            self.log.close()

    
    def orig_clear( self ):
        self.ui.orig_tbl.clear()
        self.ui.orig_tbl.setRowCount( 0 )

        if self.model.orig_path_list:
            self.model.orig_path_list = []
        
        if self.log:
            self.log.set_log( 'Clear Origin Path' )


    def copy_act( self ):
        if not self.model.orig_path_list:
            if self.log:
                self.log.set_log( 'Origin info Empty' )
            return self.ui.message_box( 'error', 'Org Empth Error', 'Origin info Empty' )
        
        elif not self.model.target_path_list:
            if self.log:
                self.log.set_log( 'Target info Empty' )
            return self.ui.message_box( 'error', 'Tar Empty Error', 'Target info Empty' )

        elif not self.model.orig_path_list and not self.model.target_path_list:
            if self.log:
                self.log.set_log( 'Origin and Target info Empty' )
            return self.ui.message_box( 'error', 'Org Tar Empty Error', 'Origin and Target info Empty' )

        err_msg = []
        for idx, orig in enumerate( self.model.orig_path_list ):
            err_info = []

            try:
                shutil.copy2( orig, self.model.target_path_list[0] )
                if self.log:
                    self.log.set_log( f'"{orig}" --> "{self.model.target_path_list[0]}"' )

            except Exception as e:
                err_info.append( idx )
                err_info.append( orig )
                err_info.append( e )
            
            if err_info:
                err_msg.append( err_info )
        
        
        if not err_msg:
            if self.log:
                self.log.set_log( f'"{self.model.target_path_list[0]}"\nCopy Complete.' ) 

            self.ui.message_box( 'info', 'Copy Done', f'"{self.model.target_path_list[0]}"\nCopy Complete.')

            self.model.orig_path_list = []
            self.model.target_path_list = []
            self.ui.orig_tbl.clear()
            self.ui.target_tbl.clear()
            self.ui.orig_tbl.setRowCount(0)
            self.ui.target_tbl.setRowCount(0)

        else:
            err = ('=' * 15) + '\n'
            err += 'Error' + '\n'
            err += ('=' * 15) + '\n'
            for idx, orig_path, error in err_msg:
                err += f'[{idx}] "{orig_path}" -- {error}\n'
            
            err += ('=' * 15) + '\n'

            if self.log:
                self.log.set_log( err )

            self.ui.message_box( 'warning', 'Copy Warning', err )





if __name__ == '__main__':
    app = copyer_ui.QApplication( sys.argv )

    rn = Copyer()

    main_ui = rn.ui
    main_ui.show()

    sys.exit( app.exec_())