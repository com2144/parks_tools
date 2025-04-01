import os
import sys
import re


from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


from constant import *


PREFERRED = QSizePolicy.Preferred
ICON = os.path.join( os.path.dirname( os.path.abspath( sys.executable ) ), 'icon' )


DEV = 0


class ConvertUi( QDialog ):
    def __init__( self ):
        super().__init__()
        self.resize( 1150, 500 )
        self.setWindowTitle( 'Mp4 Converter' )

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )

        self.data_tbl = DataTable()

        data_lay = QVBoxLayout()
        data_lay.addWidget( self.data_tbl )


        save_dir_lb = QLabel( f'{"Save Folder":<15}' )
        self.save_dir_edt = QLineEdit()
        self.save_dir_btn = QPushButton( '...' )
        save_dir_lay = QHBoxLayout()
        save_dir_lay.addWidget( save_dir_lb )
        save_dir_lay.addWidget( self.save_dir_edt )
        save_dir_lay.addWidget( self.save_dir_btn )


        self.resize_chk = QCheckBox( 'Resize' )
        self.resize_cb = QComboBox()
        self.resize_cb.addItems( RESIZE )
        self.resize_cb.setEnabled( False )

        resize_lay = QVBoxLayout()
        resize_lay.addWidget( self.resize_chk )
        resize_lay.addWidget( self.resize_cb )
        resize_widget = QWidget()
        resize_widget.setLayout( resize_lay )

        self.fps_chk = QCheckBox( 'Fps' )
        self.fps_cb = QComboBox()
        self.fps_cb.addItems( FPS )
        self.fps_cb.setEnabled( False )

        fps_lay = QVBoxLayout()
        fps_lay.addWidget( self.fps_chk )
        fps_lay.addWidget( self.fps_cb )
        fps_widget = QWidget()
        fps_widget.setLayout( fps_lay )

        self.codec_chk = QCheckBox( 'Codec' )
        self.codec_cb = QComboBox()
        self.codec_cb.addItems( CODEC )
        self.codec_cb.setEnabled( False )

        codec_lay = QVBoxLayout()
        codec_lay.addWidget( self.codec_chk )
        codec_lay.addWidget( self.codec_cb )
        codec_widget = QWidget()
        codec_widget.setLayout( codec_lay )

        option_lay = QHBoxLayout()
        option_lay.addWidget( resize_widget )
        option_lay.addWidget( fps_widget )
        option_lay.addWidget( codec_widget )

        self.opt_grp = QGroupBox( 'Options' )
        self.opt_grp.setLayout( option_lay )
        self.opt_grp.setCheckable( True )
        self.opt_grp.setChecked( False )


        self.rename_tbl = RenameTable()

        self.add_btn = QPushButton( '+' )
        self.minus_btn = QPushButton( '-' )
        rename_btn_lay = QHBoxLayout()
        rename_btn_lay.addWidget( self.add_btn )
        rename_btn_lay.addWidget( self.minus_btn )

        rename_lay = QVBoxLayout()
        rename_lay.addWidget( self.rename_tbl )
        rename_lay.addLayout( rename_btn_lay )

        self.rename_grp = QGroupBox( 'Rename' )
        self.rename_grp.setLayout( rename_lay )
        self.rename_grp.setMinimumHeight( 200 )
        self.rename_grp.setCheckable( True )
        self.rename_grp.setChecked( False )


        self.version_chk = QCheckBox( 'Version Numbering' )
        self.version_edt = QLineEdit()
        self.version_edt.setText( '1' )
        self.version_edt.setEnabled( False )
        self.version_edt.setReadOnly( True )
        self.version_edt.setAlignment( Qt.AlignCenter )

        self.version_plus_btn = QPushButton( '+' )
        self.version_plus_btn.setFixedWidth( 40 )
        self.version_plus_btn.setEnabled( False )
        self.version_minus_btn = QPushButton ( '-' )
        self.version_minus_btn.setFixedWidth( 40 )
        self.version_minus_btn.setEnabled( False )
        version_btn_lay = QHBoxLayout()
        version_btn_lay.addWidget( self.version_plus_btn )
        version_btn_lay.addWidget( self.version_minus_btn )

        version_edt_lay = QHBoxLayout()
        version_edt_lay.addWidget( self.version_edt )
        version_edt_lay.addLayout( version_btn_lay )

        version_lay = QVBoxLayout()
        version_lay.addWidget( self.version_chk )
        version_lay.addLayout( version_edt_lay )
        version_widget = QWidget()
        version_widget.setLayout( version_lay )

        self.memo_chk = QCheckBox( 'Memo' )
        self.memo_edt = QLineEdit()
        self.memo_edt.setEnabled( False )

        memo_lay = QVBoxLayout()
        memo_lay.addWidget( self.memo_chk )
        memo_lay.addWidget( self.memo_edt )
        memo_widget = QWidget()
        memo_widget.setLayout( memo_lay )

        sub_data_lay = QHBoxLayout()
        sub_data_lay.addWidget( version_widget )
        sub_data_lay.addWidget( memo_widget )

        self.sub_data_grp = QGroupBox( 'Sub Data' )
        self.sub_data_grp.setLayout( sub_data_lay )
        self.sub_data_grp.setCheckable( True )
        self.sub_data_grp.setChecked( False )


        self.log_chk = QCheckBox( 'Convert Log' )
        self.log_chk.setEnabled( True )
        self.log_chk.setChecked( False )

        self.convert_btn = QPushButton( 'Convert' )
        self.cancel_btn = QPushButton( 'Cancel' )
        self.convert_btn.setFixedWidth( 80 )
        self.convert_btn.setFixedHeight( 40 )
        self.cancel_btn.setFixedWidth( 80 )
        self.cancel_btn.setFixedHeight( 40 )

        convert_cancel_lay = QHBoxLayout()
        convert_cancel_lay.addWidget( self.log_chk )
        convert_cancel_lay.addSpacerItem(
            QSpacerItem( 180, 200, PREFERRED, PREFERRED )
        )
        convert_cancel_lay.addWidget( self.convert_btn )
        convert_cancel_lay.addWidget( self.cancel_btn )


        order_lay = QVBoxLayout()
        order_lay.addLayout( save_dir_lay )
        order_lay.addSpacing( 5 )
        order_lay.addWidget( self.opt_grp )
        order_lay.addSpacing( 5 )
        order_lay.addWidget( self.rename_grp )
        order_lay.addSpacing( 5 )
        order_lay.addWidget( self.sub_data_grp )
        order_lay.addSpacing( 5 )
        order_lay.addLayout( convert_cancel_lay )

        main_lay = QHBoxLayout()
        main_lay.addLayout( data_lay, stretch=3 )
        main_lay.addLayout( order_lay, stretch=2 )

        self.setLayout( main_lay )

        self.resize_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.resize_cb ) )
        self.fps_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.fps_cb ) )
        self.codec_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.codec_cb ) )
        self.memo_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.memo_edt ) )
        self.version_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.version_edt ) )
        self.version_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.version_plus_btn ) )
        self.version_chk.toggled.connect( lambda state : self.toggle_widget_sig( state, self.version_minus_btn ) )


    def toggle_widget_sig( self, state, widget ):
        widget.setEnabled( state )


    def message_box( self, error_type, title, message, confirm=False ):
        msg_box = QMessageBox

        if error_type == 'info':
            return msg_box.information( self, title, message )
        
        elif error_type == 'warning':
            if confirm:
                msg_box = QMessageBox( self )
                msg_box.setIcon( QMessageBox.Warning )
                msg_box.setText( message )
                msg_box.setStandardButtons( QMessageBox.Yes | QMessageBox.No )

                msg_box.exec_()

                if msg_box.clickedButton() == msg_box.button( QMessageBox.Yes ):
                    return 'yes'
                elif msg_box.clickedButton() == msg_box.button( QMessageBox.No ):
                    return 'no'
                
            else:
                return msg_box.warning( self, title, message )
        
        elif error_type == 'error':
            return msg_box.critical( self, title, message )


class DataTable( QTableWidget ):
    itemsDropped = Signal( list )
    itemsUpdated = Signal( list )

    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.setSelectionMode( QAbstractItemView.SingleSelection )
        self.setAcceptDrops( True )
        self.setDragEnabled( True )
        self.viewport().setAcceptDrops( True )
        self.setDropIndicatorShown( True )
        self.verticalHeader().hide()

        self.setColumnCount( 6 )
        self.setHorizontalHeaderLabels(
            ['Check', 'Path', 'FirstFrame', 'Count', 'Ext', 'Remove']
        )

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 360)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 50)

        self.items = []


    def dragEnterEvent( self, event ):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    

    def dragMoveEvent( self, event ):
        if event.mimeData().hasUrls():
            event.setDropAction( Qt.CopyAction )
            event.accept()
        else:
            event.ignore()

    
    def dropEvent( self, event ):
        if event.mimeData().hasUrls():
            event.setDropAction( Qt.CopyAction )
            event.accept()
            links = [ str( url.toLocalFile() ) for url in event.mimeData().urls() ]
            self.itemsDropped.emit( links )
        else:
            new_order = []
            for row in range( self.rowCount() ):
                item = self.item( row, 0 )
                if item:
                    new_order.append( item.text() )
            
            self.itemsDropped.emit( new_order )


    def add_items( self, items ):
        if not items:
            return
        else:
            self.items = items
       
        self.setRowCount( len(items) )

        for row, item_text in enumerate( items ):
            chk_widget = CheckBoxWidget( self )
            chk_widget.chk_box.setChecked( True )
            self.setCellWidget( row, 0, chk_widget)

            file_path, ext = os.path.splitext( item_text )

            if ext.lower() in FORMAT[:1]:
                self.setItem( row, 1, QTableWidgetItem(file_path) )
                self.setItem( row, 2, QTableWidgetItem( '-' ))
                self.setItem( row, 3, QTableWidgetItem( '-' ))

            elif ext.lower() in FORMAT[1:]:
                file_dir = os.path.dirname( item_text )
                file_name = os.path.basename( file_path )
                file_name_list = file_name.split( '.' )   

                if re.match(r'^\d{4}$', file_name_list[-1]):
                    cleanup_file_name = '.'.join( file_name_list[:-1] )
                    cleanup_file_path = file_dir + '/' + cleanup_file_name

                    file_list = [ f for f in os.listdir(file_dir) 
                                 if os.path.splitext(f)[-1].lower() in FORMAT[1:]
                                 and cleanup_file_name in os.path.splitext(f)[0] ]
                    
                    sorted_frame_list = sorted(file_list, key=lambda x: int(x.split('.')[-2]))
                    first_frame = str(sorted_frame_list[0].split('.')[-2])

                else:
                    cleanup_file_path = file_path
                    file_list = []
                    first_frame = 0
                
                self.setItem( row, 1, QTableWidgetItem(cleanup_file_path) )
                self.setItem( row, 2, QTableWidgetItem(first_frame) )
                self.setItem( row, 3, QTableWidgetItem(str( len(file_list) )) )

            self.setItem( row, 4, QTableWidgetItem( ext ) )

            rm_widget = RemoveBtnWidget( row, self )
            rm_widget.removeClicked.connect( self.remove_item )
            self.setCellWidget( row, 5, rm_widget )

        self.setHorizontalHeaderLabels(
            ['Check', 'Path', 'FirstFrame', 'Count', 'Ext', 'Remove']
        )
        self.horizontalHeader().show()
        self.verticalHeader().hide()
    

    def remove_item( self, row ):
        self.removeRow( row )

        if row < len( self.items ):
            self.items.pop( row )
            self.itemsUpdated.emit( self.items )
            for i in range( self.rowCount() ):
                rm_widget = self.cellWidget(i, 4)
                if rm_widget:
                    rm_widget.row = i        


class RenameTable( QTableWidget ):
    def __init__( self ):
        super().__init__()
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.verticalHeader().hide()
        self.setColumnCount( 2 )
        self.setHorizontalHeaderLabels(
            ['Search', 'Replace']
        )

        self.setColumnWidth(0, 207)
        self.setColumnWidth(1, 207) 


class LogListView( QDialog ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.setWindowTitle( 'Copy History Log' )
        self.resize( 400, 520 )

        self.list_widget = QListWidget()

        list_lay = QHBoxLayout()
        list_lay.addWidget( self.list_widget )

        self.setLayout( list_lay )

        if parent:
            self.parent = parent
            parent.installEventFilter( self )
            parent_pos = parent.pos()
            parent_size = parent.size()

            new_x = parent_pos.x() + parent_size.width() + 1
            new_y = parent_pos.y()

            self.move( new_x, new_y )


    def eventFilter( self, object, event ):
        if object == self.parent and event.type() == QEvent.Move:
            self.updatePosition()
        return super(LogListView, self).eventFilter( object, event)    


    def updatePosition(self):
        parent_pos = self.parent.pos()
        parent_size = self.parent.size()

        new_x = parent_pos.x() + parent_size.width() + 1
        new_y = parent_pos.y()

        self.move( new_x, new_y )    


    def set_log( self, log_item ):
        if isinstance( log_item, str ):
            self.list_widget.addItem( log_item )

        elif isinstance( log_item, list ):
            self.list_widget.addItems( log_item )



class CheckBoxWidget( QWidget ):
    def __init__(self, parent=None ):
        super().__init__( parent )
        self.chk_box = QCheckBox()
        chk_lay = QHBoxLayout()
        chk_lay.addWidget( self.chk_box )
        chk_lay.setAlignment( Qt.AlignCenter )
        chk_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout( chk_lay )


class LineEditWidget( QWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.line_edt = QLineEdit()
        self.line_edt.setAlignment( Qt.AlignCenter )
        line_edt_lay = QHBoxLayout()
        line_edt_lay.addWidget( self.line_edt )
        line_edt_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout( line_edt_lay )


class RemoveBtnWidget( QWidget ):
    removeClicked = Signal( int )

    def __init__(self, row, parent=None ):
        super().__init__( parent )
        self.row = row

        self.rm_btn = QPushButton()
        self.rm_btn.setIcon( QIcon( os.path.join( ICON, 'minus.png' ) ) )
        self.rm_btn.setFlat( True )
        self.rm_btn.setMinimumSize( QSize( 50, 30 ) )
        self.rm_btn.setMaximumSize( QSize( 50, 30 ) )

        rm_lay = QHBoxLayout()
        rm_lay.addWidget( self.rm_btn )
        rm_lay.setAlignment( Qt.AlignCenter )
        rm_lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout( rm_lay )

        self.rm_btn.clicked.connect( self.remove_clicked )


    def remove_clicked( self ):
        self.removeClicked.emit( self.row )


if __name__ == '__main__':
    if DEV:
        app = QApplication( sys.argv )

        main_win = ConvertUi()
        main_win.show()

        sys.exit( app.exec_() )