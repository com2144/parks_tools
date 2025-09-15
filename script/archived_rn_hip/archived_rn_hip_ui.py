import hou

from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


class ArchivedUI(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500,400)
        self.setWindowTitle('Archieved Hipfile (Sop Node)')


        select_lb = QLabel(f'{"Geometry Path":<20}')
        self.select_edt = QLineEdit()
        self.select_btn = QPushButton('Select')

        select_lay = QHBoxLayout()
        select_lay.addWidget(select_lb)
        select_lay.addWidget(self.select_edt)
        select_lay.addWidget(self.select_btn)


        table_lb = QLabel(f'{"Node Info":<50}')
        self.whole_check = QCheckBox('All Check')
        self.whole_check.setCheckable(True)
        self.whole_check.setChecked(True)

        table_hlay = QHBoxLayout()
        table_hlay.addWidget(table_lb)
        table_hlay.addWidget(self.whole_check, 0, Qt.AlignRight)

        self.table_wg = ArchievedTable()

        table_lay = QVBoxLayout()
        table_lay.addLayout(table_hlay)
        table_lay.addWidget(self.table_wg)


        rn_src_lb = QLabel('Src Info')
        self.rn_src_edt = QLineEdit()
        self.rn_src_edt.setFixedHeight(25)

        rn_src_vlay = QVBoxLayout()
        rn_src_vlay.addWidget(rn_src_lb)
        rn_src_vlay.addWidget(self.rn_src_edt)

        rn_arrow_lb = QLabel('➡')
        arrow_font = QFont()
        arrow_font.setPointSize(15)
        rn_arrow_lb.setFont(arrow_font)

        rn_tr_lb = QLabel('Target Info')
        self.rn_tr_edt = QLineEdit()
        self.rn_tr_edt.setFixedHeight(25)

        rn_tr_vlay = QVBoxLayout()
        rn_tr_vlay.addWidget(rn_tr_lb)
        rn_tr_vlay.addWidget(self.rn_tr_edt)

        rn_lay = QHBoxLayout()
        rn_lay.addLayout(rn_src_vlay)
        rn_lay.addSpacing(3)
        rn_lay.addWidget(rn_arrow_lb, 0, Qt.AlignBottom)
        rn_lay.addSpacing(3)
        rn_lay.addLayout(rn_tr_vlay)


        self.convert_btn = QPushButton('Convert')
        self.convert_btn.setFixedHeight(30)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setFixedHeight(30)

        order_lay = QHBoxLayout()
        order_lay.addSpacing(350)
        order_lay.addWidget(self.convert_btn)
        order_lay.addWidget(self.cancel_btn)


        main_lay = QVBoxLayout()
        main_lay.addLayout(select_lay)
        main_lay.addSpacing(8)
        main_lay.addLayout(table_lay)
        main_lay.addSpacing(5)
        main_lay.addLayout(rn_lay)
        main_lay.addSpacing(5)
        main_lay.addLayout(order_lay)

        self.setLayout(main_lay)


    def select_btn_func(self, func_address):
        self.select_btn.clicked.connect(func_address)
    

    def whole_chk_func(self, func_address):
        self.whole_check.toggled.connect(func_address)
    

    def rn_func(self, func_address):
        self.convert_btn.clicked.connect(func_address)


    def close_ui(self, func_address):
        self.cancel_btn.clicked.connect(func_address)


    def closeEvent( self, event ):
        print( "Close Archived Rename Hip tool" )
        return


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


class ArchievedTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(
            ['Check', 'NodeName', 'BasePath']
        )

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 100)


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


class GeoTreeDialog(QDialog):
    selectSignal = Signal(hou.Node)
    closeSignal = Signal()

    def __init__( self, parent=None ):
        super().__init__(parent)
        self.setWindowTitle('Geometry node select')
        self.resize(500, 400)

        self.tree_wg = QTreeWidget()
        self.tree_wg.setHeaderLabels(["Node Name"])
        self.tree_wg.setSelectionMode(QAbstractItemView.SingleSelection)

        self.select_btn = QPushButton('Select')
        self.cancel_btn = QPushButton('Cancel')

        btn_lay = QHBoxLayout()
        btn_lay.addWidget(self.select_btn)
        btn_lay.addWidget(self.cancel_btn)

        tree_lay = QVBoxLayout()
        tree_lay.addWidget(self.tree_wg)
        tree_lay.addLayout(btn_lay)

        self.setLayout(tree_lay)

        root_path = '/obj'
        root_node = hou.node(root_path)
        if root_node:
            root_item = QTreeWidgetItem([root_node.name()])
            root_item.setData(0, Qt.UserRole, root_node.path())
            self.tree_wg.addTopLevelItem(root_item)

            self._set_root_tree(root_node, root_item)
        else:
            dummy_item = QTreeWidgetItem([root_path])
            self.tree_wg.addTopLevelItem(dummy_item)

        if parent:
            self.parent = parent
            parent.installEventFilter(self)
            pfg = parent.frameGeometry() 
            mfg = self.frameGeometry()

            new_x = pfg.left() - mfg.width()
            new_y = pfg.top()
            
            self.move(new_x, new_y)

        self.select_btn.clicked.connect(self.on_select_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)


    def _set_root_tree(self, node, parent_item):
        for child in node.children():
            if child.type().name() == 'geo':
                child_item = QTreeWidgetItem( [child.name()] )
                child_item.setData( 0, Qt.UserRole, child.path() )

                parent_item.addChild(child_item)
                self._set_root_tree(child, child_item)


    def eventFilter(self, object, event):
        if object == self.parent and event.type() == QEvent.Move:
            self.updatePosition()
        return super(GeoTreeDialog, self).eventFilter(object, event)


    def updatePosition( self ):
        pfg = self.parent.frameGeometry() 
        mfg = self.parent.frameGeometry()

        new_x = max(0, pfg.left() - mfg.width() - 1)
        new_y = pfg.top()
        
        self.move(new_x, new_y)


    def on_select_clicked(self):
        item = self.tree_wg.currentItem()
        if not item:
            print( 'Select the Node plz!' )
            return
        
        node_path = item.data(0, Qt.UserRole)
        node = hou.node(node_path)
        if node:
            self.selectSignal.emit(node)
            self.accept()


    def on_cancel_clicked( self ):
        self.closeSignal.emit()
        self.reject()