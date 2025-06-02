from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


class BGrenderUI(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600,400)
        self.setWindowTitle('Background Rendering')


        browse_lb = QLabel(f'{"Hip File Path":<20}')
        self.browse_edt = QLineEdit()
        self.browse_btn = QPushButton('Browse')

        browse_lay = QHBoxLayout()
        browse_lay.addWidget(browse_lb)
        browse_lay.addWidget(self.browse_edt)
        browse_lay.addWidget(self.browse_btn)


        table_lb = QLabel(f'{"Render Tasks":<50}')
        self.table_wg = BGListTable()

        table_lay = QVBoxLayout()
        table_lay.addWidget(table_lb)
        table_lay.addWidget(self.table_wg)


        self.render_btn = QPushButton('Render')
        self.render_btn.setFixedHeight(30)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setFixedHeight(30)

        order_lay = QHBoxLayout()
        order_lay.addSpacing(350)
        order_lay.addWidget(self.render_btn)
        order_lay.addWidget(self.cancel_btn)


        main_lay = QVBoxLayout()
        main_lay.addLayout(browse_lay)
        main_lay.addSpacing(8)
        main_lay.addLayout(table_lay)
        main_lay.addSpacing(5)
        main_lay.addLayout(order_lay)


        self.setLayout(main_lay)

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


class BGListTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(
            ['Check', 'Node Name', 'Save Path', 'Start Frame', 'End Frame']
        )
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 275)
        self.setColumnWidth(3, 75)
        self.setColumnWidth(4, 75)


class CheckBoxWidget( QWidget ):
    def __init__(self, parent=None ):
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