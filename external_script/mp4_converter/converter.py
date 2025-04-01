import os
import sys
import platform
import re
import subprocess
import copy


from options            import Options
from rename             import Rename
import converter_ui
from converter_model    import ConvertModel
from constant           import *

class Convert:
    def __init__( self ):
        self.ui = converter_ui.ConvertUi()
        self.model = ConvertModel()

        self.rename = Rename( self.model, converter_ui, self.ui )


        self.log = None


        self.ui.save_dir_btn.clicked.connect( self._set_save_dir )

        self.ui.data_tbl.itemsDropped.connect( self.dtl_get_content )
        self.ui.data_tbl.itemsUpdated.connect( self.dtl_update_content )

        self.ui.add_btn.clicked.connect( self.rename.add_item )
        self.ui.minus_btn.clicked.connect( self.rename.remove_item )
        self.ui.version_plus_btn.clicked.connect( self.version_add )
        self.ui.version_minus_btn.clicked.connect( self.version_subtract )

        self.ui.log_chk.toggled.connect( self.log_sig )
        self.ui.convert_btn.clicked.connect( self.convert )
        self.ui.cancel_btn.clicked.connect( self.ui.close )


    def _set_save_dir( self ):
        home_path = os.path.expanduser( '~' )
        save_dir_path = converter_ui.QFileDialog.getExistingDirectory(
            self.ui,
            'Select Directory',
            home_path
        )
        self.ui.save_dir_edt.setText( save_dir_path )

        if self.log:
            self.log.set_log( f'set save dir path :: {save_dir_path}' )
            self.log.set_log( '-' * 10)


    def dtl_get_content( self, items ):
        warning_msg = []

        pattern = r'^([\w\-]+_v\d{3})\.(\d+)$'
        items_name = []
        for item in items:
            base_name = os.path.basename( item )
            file_name = os.path.splitext( base_name )[0]
            if re.match( pattern, file_name ):
                file_name = file_name.split( '.' )[:-1]
            
            items_name.append( file_name )
        
        datas_name = []
        for data in self.model.data_list:
            base_name = os.path.basename( data )
            file_name = os.path.splitext( base_name )[0]
            if re.match( pattern, file_name ):
                file_name = file_name.split( '.' )[:-1]
            
            datas_name.append( file_name )

        duplicate_list = []
        for item_name in items_name:
            if item_name in datas_name:
                duplicate_list.append( item_name )
        
        if duplicate_list:
            msg = 'Duplicate Info\n'
            msg += ("=" * 10) + '\n'
            msg += '\n'.join( duplicate_list )

            self.ui.message_box( 'error', 'Duplicate Error', msg )
            return
        

        for item in items:
            if os.path.isdir( item ):
                warning_msg.append( f'"{item}" is Folder.' )

            elif os.path.isfile( item ):
                file = os.path.basename( item )
                ext = os.path.splitext( file )[-1]
                
                pattern = r'^([\w\-]+_v\d{3})\.(\d+)\.(\w+)$'
                match = re.match( pattern, file )

                if ext.lower() not in FORMAT:
                    warning_msg.append( f'Not support {ext} format :: {file}' )
                
                elif not match and ext in FORMAT[1:]:
                    warning_msg.append( f'Not match the file naming :: {file}')

                else:
                    self.model.data_list.append( item )
            
            else:
                self.model.data_list.append( item )
        
        if self.log:
            if warning_msg:
                self.log.set_log( warning_msg )
                self.log.set_log( '^' * 10 )

            for data in self.model.data_list:
                self.log.set_log( f'get origin data :: {data}' )
                self.log.set_log( '-' * 10 )
        
        if warning_msg:
            if len(items) == 1:
                self.ui.data_tbl.setHorizontalHeaderLabels(
                    ['Check', 'Path', 'FirstFrame', 'Count', 'Ext', 'Remove']
                )
                self.ui.data_tbl.horizontalHeader().show()
                self.ui.data_tbl.verticalHeader().hide()

            self.ui.message_box( 'warning', 'Orig Warning', '\n'.join(warning_msg) )
        
        self.ui.data_tbl.add_items( self.model.data_list )


    def dtl_update_content( self, items ):
        self.model.data_list = items
        
        if self.log:
            msg = 'now list\n'
            msg += ('=' * 10) + '\n' 
            msg += '\n'.join( self.model.data_list )
            msg += ('=' * 10) + '\n'

            self.log.set_log( msg )
    

    def log_sig( self ):
        if self.ui.log_chk.isChecked():
            self.log = converter_ui.LogListView( self.ui )
            self.log.show()
        else:
            self.log.close()
    

    def _get_ui_info( self ):
        self.model.save_dir_path = str( self.ui.save_dir_edt.text() )

        self.model.is_options = self.ui.opt_grp.isChecked()
        if self.model.is_options:
            self.model.is_resize = self.ui.resize_chk.isChecked()
            if self.model.is_resize:
                self.model.resize = str( self.ui.resize_cb.currentText() )
            else:
                self.model.resize = 'origin'

            self.model.is_fps = self.ui.fps_chk.isChecked()
            if self.model.is_fps:
                self.model.fps = str( self.ui.fps_cb.currentText() )
            else:
                self.model.fps = '23.976'
            
            self.model.is_codec = self.ui.codec_chk.isChecked()
            if self.model.is_codec:
                self.model.codec = str( self.ui.codec_cb.currentText() )
            else:
                self.model.codec = 'H.264'
        else:
            self.model.is_resize = False
            self.model.is_fps = False
            self.model.is_codec = False
            
        self.model.is_rn = self.ui.rename_grp.isChecked()

        self.model.is_sub = self.ui.sub_data_grp.isChecked()
        if self.model.is_sub:
            self.model.is_version = self.ui.version_chk.isChecked()
            if self.model.is_version:
                self.model.version = str( self.ui.version_edt.text() )
            else:
                self.model.version = ''

            self.model.is_memo = self.ui.memo_chk.isChecked()
            if self.model.is_memo:
                self.model.memo = str( self.ui.memo_edt.text() )
            else:
                self.model.memo = ''
        else:
            self.model.is_version = False
            self.model.is_memo = False


    def version_add( self ):
        version_num = self.ui.version_edt.text()

        if version_num and int( version_num ) > 0:
            version_num = int( version_num )
            version_num += 1
            version_num = str( version_num )
            
            self.ui.version_edt.setText( version_num )
        
        else:
            self.ui.message_box( 'error', 'Version Num Plus Error', 'Wrong Version Number' )
    

    def version_subtract( self ):
        version_num = self.ui.version_edt.text()

        if version_num and int( version_num ) > 1:
            version_num = int( version_num )
            version_num -= 1
            version_num = str( version_num )

            self.ui.version_edt.setText( version_num )

        elif int( version_num ) == 1:
            self.ui.message_box( 'error', 'Version Num Minus Error', 'Just more than "1" plz' )

        else:
            self.ui.message_box( 'error', 'Vesion Num Minus Error', 'Wrong Version Number' )


    def convert( self ):
        self._get_ui_info()

        if not self.model.save_dir_path:
            self.ui.message_box( 'error', 'Save Dir Error', 'Save dir path Empty' )
            return        

        data_tbl = self.ui.data_tbl
        row_count = data_tbl.rowCount()
        column_count = data_tbl.columnCount()

        if row_count == 0:
            self.ui.message_box( 'error', 'Source Empty', 'Source Data is Empty' )
            return 

        for row_idx in range( row_count ):
            row_data = []
            for column in range( column_count ):
                item = data_tbl.item( row_idx, column )
                widget = data_tbl.cellWidget( row_idx, column )

                if item:
                    row_data.append( item.text() )
                
                elif widget:
                    if isinstance( widget, converter_ui.CheckBoxWidget ):
                        row_data.append( widget.chk_box.isChecked() )

                    elif isinstance( widget, converter_ui.RemoveBtnWidget ):
                        row_data.append( 'remove_btn' )
            self.model.data_tbl_list.append( row_data )

        option_obj = Options( self.model, self.ui, self.model.data_tbl_list )

        options = option_obj._get_options()
        subs = option_obj._get_subs()

        file_path_list = [ data[1] for data in self.model.data_tbl_list ]

        if self.model.is_rn:
            tmp_list = copy.copy( self.model.data_tbl_list )
            tmp_list = self.rename.rename_info( tmp_list )

            if isinstance( tmp_list, dict):
                self.ui.message_box( 'error', 'Rename Error', tmp_list['rename_error'] )
                return
            
            self.model.data_tbl_list = tmp_list
        
        data_chk = [ data[0] for data in self.model.data_tbl_list ]
        if True not in data_chk:
            self.ui.message_box( 'error', 'Checking Error', 'Convert Data Check plz' )
            return

        success_list = []
        fail_list = []
        for idx, data in enumerate(self.model.data_tbl_list):
            if data[0]:
                cmd, output_path = self.ffmpeg_cmd( options[idx], subs[idx], file_path_list[idx], data )

                if not os.path.exists( cmd[0] ):
                    return self.ui.message_box( 'error', 'ffmpeg Error', f'ffmpeg file is not exists.\n{cmd[0]}')

                result = subprocess.run( cmd, capture_output=True, text=True, encoding='utf-8' )

                if result.returncode == 0:
                    success_list.append( f'[{idx}] - {output_path}' )
                else:
                    fail_list.append( f'[{idx}] - {output_path}' )
        
        msg = ''
        if success_list:
            msg += ('='*10) + '\n'
            msg += 'Success list' + '\n'
            msg += ('='*10) + '\n'
            msg += '\n'.join( success_list ) + '\n'

        elif fail_list:
            msg += ('='*10) + '\n'
            msg += 'Fail list' + '\n'
            msg += ('='*10) + '\n'
            msg += '\n'.join( fail_list ) + '\n'

        if self.log:
            self.log.set_log( msg )

        self.ui.message_box( 'info', 'Convert Status', msg )


    def ffmpeg_cmd( self, option, sub, orig_path, data ):
        _, file_path, first_frame, count, ext, _ = data
        resize, fps, codec = option
        version, memo = sub 

        if platform.system() == 'Windows':
            file_path = file_path.replace('/', '\\')
            orig_path = orig_path.replace('/', '\\')

        cmd = [ self.ffmpeg_executable() ]

        if ext in FORMAT[1:]:
            if ext in ['.dpx', '.exr']:
                cmd += [ '-apply_trc', 'bt709' ]
            cmd += [ '-y', '-start_number', str(first_frame) ]
            
            input_path = f'{orig_path}.%04d{ext}'
            cmd += [ '-i', input_path ]
            cmd += [ '-frames:v', str(count) ]
        
        else:
            input_path = f'{orig_path}{ext}'
            cmd += [ '-i', input_path ]
        
        if codec == 'H.264':
            cmd += [ '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'veryslow', '-crf', '18' ]
            cmd += [ '-x264opts', 'colorprim=bt709:transfer=bt709:colormatrix=bt709' ]
        
        else:
            cmd += [ '-c:v', 'libx265', '-pix_fmt', 'yuv420p', '-preset', 'veryslow', '-crf', '28' ]
            cmd += [ '-color_primaries' 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709' ]
        
        scale = "pad='ceil(iw/2)*2:ceil(ih/2)*2"
        if resize == 'half':
            scale += ', scale=iw/2:-1'
        elif resize == '2x':
            scale += ', scale=iw*2:ih*2'
        
        cmd += [ '-vf', scale ]

        cmd += [ '-r', str(fps) ]

        file_name = os.path.basename( file_path )

        pattern = r'^([\w\-]+_v\d{3})$'
        match = re.match( pattern, file_name )
        
        file_name_split = file_name.split('_')

        if match:
            ver = file_name_split[-1]
            base_name = '_'.join( file_name_split[:-1] ) if len(file_name_split) > 1 else file_name 

        else:
            ver = None
            base_name = file_name
        
        if version:
            ver = f'v{version.zfill(3)}'
        
        if memo:
            if ver:
                file_name = f'{base_name}_{memo}_{ver}'
            else:
                file_name = f'{base_name}_{memo}'

        elif ver:
            file_name = f'{base_name}_{ver}'

        output_path = os.path.join( self.model.save_dir_path.replace('/', '\\'), f'{file_name}.mp4')

        cmd.append( output_path )

        return cmd, output_path


    def ffmpeg_executable( self ):
        now_path = os.path.dirname( sys.executable )
        tool_path = os.path.join( now_path, 'tools' )

        if platform.system() == 'Windows':
            ffmpeg_cmd = os.path.join( tool_path, 'ffmpeg.exe' )
        else:
            ffmpeg_cmd = os.path.join( tool_path, 'ffmpeg' )
    
        return ffmpeg_cmd




if __name__ == '__main__':
    app = converter_ui.QApplication( sys.argv )

    rn = Convert()

    main_ui = rn.ui
    main_ui.show()

    sys.exit( app.exec_() )