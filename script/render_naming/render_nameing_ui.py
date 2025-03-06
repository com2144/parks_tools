from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


DEV = 0


class RenderNamingUI( QDialog ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.resize( 400, 250 )
        self.setWindowTitle( 'Rendering Namer' )

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )


        render_lb = QLabel( 'Render Node List' )
        self.render_tbl = RenderNodeTable()

        render_lay = QVBoxLayout()
        render_lay.addWidget( render_lb )
        render_lay.addWidget( self.render_tbl )


        self.write_btn = QPushButton( 'Write' )
        self.cancel_btn = QPushButton( 'Cancel' )

        btn_lay = QHBoxLayout()
        btn_lay.addWidget( self.write_btn )
        btn_lay.addWidget( self.cancel_btn )


        main_lay = QVBoxLayout()
        main_lay.addLayout( render_lay )
        main_lay.addLayout( btn_lay )

        self.setLayout( main_lay )


    def write_func( self, func_address ):
        self.write_btn.clicked.connect( func_address )


    def close_ui( self, func_address ):
        self.cancel_btn.clicked.connect( func_address )


    def closeEvent( self, event ):
        print( "close Render Naming tool" )


class RenderNodeTable( QTableWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.verticalHeader().hide()
        self.setColumnCount( 3 )
        self.setHorizontalHeaderLabels(
            ['Check', 'Path', 'Element']
        )

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 215)


class CheckBoxWidget( QWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.chk_box = QCheckBox()
        chk_lay = QHBoxLayout()
        chk_lay.addWidget( self.chk_box )
        chk_lay.setAlignment( Qt.AlignCenter )
        chk_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout( chk_lay )


class LabelWidget( QWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.lb = QLabel()
        lb_lay = QHBoxLayout()
        lb_lay.addWidget( self.lb )
        lb_lay.setAlignment( Qt.AlignCenter )
        lb_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout( lb_lay )


class LineEditWidget( QWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.line_edt = QLineEdit()
        self.line_edt.setAlignment( Qt.AlignCenter )
        line_edt_lay = QHBoxLayout()
        line_edt_lay.addWidget( self.line_edt )
        line_edt_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout( line_edt_lay )



if __name__ == '__main__':
    if DEV:
        import sys
        app = QApplication( sys.argv )

        main_win = RenderNaming()
        main_win.show()

        sys.exit( app.exec_() )