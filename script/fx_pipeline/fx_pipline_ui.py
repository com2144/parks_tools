from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


PREFERRED = QSizePolicy.Preferred


class PipelineSetupUi( QWidget ):
    def __init__(self):
        super().__init__()
        self.resize( 400, 100 )
        self.setWindowTitle('Project Setup')

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )


        save_dir_lb = QLabel( f'{"Save Folder":<13}' )
        self.save_dir_edt = QLineEdit()
        self.save_dir_edt.setPlaceholderText("Enter the root path")

        self.save_dir_btn = QPushButton( '...' )
        self.save_dir_btn.setFixedWidth( 50 )

        save_dir_lay = QHBoxLayout()
        save_dir_lay.addWidget( save_dir_lb )
        save_dir_lay.addWidget( self.save_dir_edt )
        save_dir_lay.addWidget( self.save_dir_btn )


        project_edt_lb = QLabel( f'{"Project Name":<10}' )
        self.project_edt = QLineEdit()
        self.project_edt.setPlaceholderText("Enter the Project name")

        self.ext_cb = QComboBox()
        self.ext_cb.addItems( ['hip', 'hiplc', 'hipnc'] )

        project_lay = QHBoxLayout()
        project_lay.addWidget( project_edt_lb )
        project_lay.addWidget( self.project_edt )
        project_lay.addWidget( self.ext_cb )


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
        main_lay.addLayout( save_dir_lay )
        main_lay.addSpacing( 3 )
        main_lay.addLayout( project_lay )
        main_lay.addSpacing( 3 )
        main_lay.addLayout( btn_lay )

        self.setLayout( main_lay )

    
    def set_save_dir_fun( self, func_address ):
        self.save_dir_btn.clicked.connect( func_address )


    def set_fx_pipeline_fun( self, func_address ):
        self.run_btn.clicked.connect( func_address )


    def close_ui( self, func_address ):
        self.cancel_btn.clicked.connect( func_address )
    

    def closeEvent( self, event ):
        print( "close FX Pipeline tool" )

