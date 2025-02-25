from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


PREFERRED = QSizePolicy.Preferred


DEV = 0


class ImportRepathUi( QDialog ):
    def __init__( self, parent=None ):
        super().__init__( parent )

        self.resize( 500, 500 )
        self.setWindowTitle( 'Import Repather' )

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )

        self.sel_tbl = SelectedTable()

        sel_lb = QLabel( 'Selected Nodes' )

        sel_tbl_lay = QVBoxLayout()
        sel_tbl_lay.addWidget( sel_lb )
        sel_tbl_lay.addWidget( self.sel_tbl )

        self.rn_tbl = RenameTable()

        rn_lb = QLabel( 'Rename Path Info' )

        self.rn_pls_btn = QPushButton( '+' )
        self.rn_mius_btn = QPushButton( '-' )
        rn_btn_lay = QHBoxLayout()
        rn_btn_lay.addWidget( self.rn_pls_btn )
        rn_btn_lay.addWidget( self.rn_mius_btn )

        rn_lay = QVBoxLayout()
        rn_lay.addWidget( rn_lb )
        rn_lay.addWidget( self.rn_tbl )
        rn_lay.addLayout( rn_btn_lay )


        self.replace_btn = QPushButton( 'Replace' )
        self.replace_btn.setFixedHeight( 35 )
        self.cancel_btn = QPushButton( 'Cancel' )
        self.cancel_btn.setFixedHeight( 35 )
        order_btn_lay = QHBoxLayout()
        order_btn_lay.addSpacerItem(
            QSpacerItem( 180, 200, PREFERRED, PREFERRED )
        )
        order_btn_lay.addWidget( self.replace_btn )
        order_btn_lay.addWidget( self.cancel_btn )


        main_lay = QVBoxLayout()
        main_lay.addLayout( sel_tbl_lay, 3)
        main_lay.addSpacing( 5 )
        main_lay.addLayout( rn_lay, 2 )
        main_lay.addSpacing( 15 )
        main_lay.addLayout( order_btn_lay, 1 )

        self.setLayout( main_lay )


    def add_rn_item_func( self, func_address ):
        self.rn_pls_btn.clicked.connect( func_address )


    def minus_rn_item_func( self, func_address ):
        self.rn_mius_btn.clicked.connect( func_address )


    def replace_func( self, func_address ):
        self.replace_btn.clicked.connect( func_address )
    


    def close_ui( self, func_address ):
        self.cancel_btn.clicked.connect( func_address )


    def closeEvent( self, event ):
        print( "close Repather tool" )


class SelectedTable( QTableWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.verticalHeader().hide()
        self.setColumnCount( 3 )
        self.setHorizontalHeaderLabels(
            ['Check', 'Node name', 'File Path']
        )

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 100)


class RenameTable( QTableWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.verticalHeader().hide()
        self.setColumnCount( 2 )
        self.setHorizontalHeaderLabels(
            ['Origin', 'Target']
        )

        self.setColumnWidth(0, 222)
        self.setColumnWidth(1, 222)


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

        main_win = ImportRepathUi()
        main_win.show()

        sys.exit( app.exec_() )