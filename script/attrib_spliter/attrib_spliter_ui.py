import sys

from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


PREFERRED = QSizePolicy.Preferred


DEV = 0


class AttribSpliterUI( QDialog ):
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.resize( 400, 150 )
        self.setWindowTitle('Attrib Spliter')

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )


        list_lb = QLabel( 'Target Node' )
        self.list_view = QListWidget()
        self.list_view.setFixedHeight( 40 )

        list_lay = QVBoxLayout()
        list_lay.addWidget( list_lb )
        list_lay.addWidget( self.list_view )


        attrib_cls_lb = QLabel( 'Attrib Class' )
        self.attrib_cls_cb = QComboBox()
        self.attrib_cls_cb.addItems( ['point', 'prim'] )

        attrib_cls_lay = QVBoxLayout()
        attrib_cls_lay.addWidget( attrib_cls_lb )
        attrib_cls_lay.addWidget( self.attrib_cls_cb )

        renderer_lb = QLabel( 'Render Select' )
        self.renderer_cb = QComboBox()
        self.renderer_cb.addItems( ['mantra', 'karma'] )

        renderer_lay = QVBoxLayout()
        renderer_lay.addWidget( renderer_lb )
        renderer_lay.addWidget( self.renderer_cb )

        select_lay = QHBoxLayout()
        select_lay.addLayout( attrib_cls_lay )
        select_lay.addLayout( renderer_lay )


        attrib_name_lb = QLabel( 'Attrib Name' )
        self.attrib_name_edt = QLineEdit()

        attrib_name_lay = QHBoxLayout()
        attrib_name_lay.addWidget( attrib_name_lb )
        attrib_name_lay.addWidget( self.attrib_name_edt )


        self.run_btn = QPushButton( 'Run' )
        self.run_btn.setFixedHeight( 30 )
        self.cancel_btn = QPushButton( 'Cancel' )
        self.cancel_btn.setFixedHeight( 30 )
        
        btn_lay = QHBoxLayout()
        btn_lay.addSpacerItem(
            QSpacerItem( 180, 200, PREFERRED, PREFERRED )
        )
        btn_lay.addWidget( self.run_btn )
        btn_lay.addWidget( self.cancel_btn )


        main_lay = QVBoxLayout()
        main_lay.addLayout( list_lay )
        main_lay.addSpacing( 5 )
        main_lay.addLayout( select_lay )
        main_lay.addLayout( attrib_name_lay )
        main_lay.addSpacing( 5 )
        main_lay.addLayout( btn_lay )

        self.setLayout( main_lay )


    def run_func( self, func_address ):
        self.run_btn.clicked.connect( func_address )


    def close_ui( self, func_address ):
        self.cancel_btn.clicked.connect( func_address )


    def closeEvent( self, event ):
        print( "close Attrib Spliter tool" )




if __name__ == '__main__':
    if DEV:
        app = QApplication( sys.argv )

        main_win = AttribSpliterUI()
        main_win.show()

        sys.exit( app.exec_() )