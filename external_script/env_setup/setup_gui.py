import sys


from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


DEV = 0


class EnvSetupUi( QDialog ):
    def __init__(self):
        super().__init__()
        self.resize( 200, 100 )
        self.setWindowTitle( 'Houdini EnvSetup' )

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )

        self.env_cb = QComboBox()
        
        self.add_btn = QPushButton( 'Add' )
        self.reset_btn = QPushButton( 'Reset' )
        self.cancel_btn = QPushButton( 'Cancel' )

        btn_lay = QHBoxLayout()
        btn_lay.addWidget( self.add_btn )
        btn_lay.addWidget( self.reset_btn )
        btn_lay.addWidget( self.cancel_btn )

        main_lay = QVBoxLayout()
        main_lay.addWidget( self.env_cb )
        main_lay.addLayout( btn_lay )

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

        

if __name__ == '__main__':
    if DEV:
        app = QApplication( sys.argv )

        main_win = EnvSetupUi()
        main_win.show()

        sys.exit( app.exec_() )