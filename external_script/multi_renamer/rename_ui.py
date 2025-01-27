import sys


from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


DEV = 0

class RenameUi( QDialog ):
    def __init__(self):
        super().__init__()
        self.resize( 500, 300 )
        self.setWindowTitle( 'Multi Renamer' )

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )


        save_dir_lb = QLabel( 'Rename Folder  ' )
        self.dir_path_line = QLineEdit()
        self.dir_path_btn = QPushButton( '...' )
        dir_path_lay = QHBoxLayout()
        dir_path_lay.addWidget( save_dir_lb )
        dir_path_lay.addWidget( self.dir_path_line )
        dir_path_lay.addWidget( self.dir_path_btn )


        self.plus_btn = QPushButton( '+' )
        self.minus_btn = QPushButton( '-' )
        pls_min_lay = QHBoxLayout()
        pls_min_lay.addWidget( self.plus_btn )
        pls_min_lay.addWidget( self.minus_btn )


        self.rename_tbl = RenameTable()


        self.run_btn = QPushButton( 'Run' )
        self.cancel_btn = QPushButton( 'Cancel' )
        run_cancel_lay = QHBoxLayout()
        run_cancel_lay.addWidget( self.run_btn )
        run_cancel_lay.addWidget( self.cancel_btn )


        main_lay = QVBoxLayout()
        main_lay.addLayout( dir_path_lay )
        main_lay.addLayout( pls_min_lay )
        main_lay.addWidget( self.rename_tbl )
        main_lay.addLayout( run_cancel_lay )

        self.setLayout( main_lay )


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


class RenameTable( QTableWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.verticalHeader().hide()
        self.setColumnCount( 3 )
        self.setHorizontalHeaderLabels(
            ['Dir', 'Source', 'Target']
        )

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 205)
        self.setColumnWidth(2, 205)


class CheckBoxWidget( QWidget ):
    def __init__( self, parent=None ):
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
        line_edt_lay = QHBoxLayout()
        line_edt_lay.addWidget( self.line_edt )
        line_edt_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout( line_edt_lay )


class FileListWidget( QDialog ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.setWindowTitle( 'Rename File List' )
        self.resize( 300, 300 )
        
        self.list_view = QListWidget()
        list_view_lay = QHBoxLayout()
        list_view_lay.addWidget( self.list_view )
        self.setLayout( list_view_lay )

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
        return super(FileListWidget, self).eventFilter(object, event)


    def updatePosition( self ):
        parent_pos = self.parent.pos()
        parent_size = self.parent.size()

        new_x = parent_pos.x() + parent_size.width() + 1
        new_y = parent_pos.y()
        
        self.move( new_x, new_y )



if __name__ == '__main__':
    if DEV:
        app = QApplication( sys.argv )

        main_win = RenameUi()
        main_win.show()

        sys.exit( app.exec_() )