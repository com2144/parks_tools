from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *

import hou


class ExportMovUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(420, 120)
        self.setWindowTitle('Flipbook To Mov')

        font = QFont()
        font.setPointSize(13)
        font.setPixelSize(13)
        self.setFont(font)


        select_cam_lb = QLabel('Cam Path')
        self.cam_edt = QLineEdit()
        self.cam_btn = QPushButton('Select')

        select_cam_lay = QHBoxLayout()
        select_cam_lay.addWidget(select_cam_lb)
        select_cam_lay.addWidget(self.cam_edt)
        select_cam_lay.addWidget(self.cam_btn)


        save_path_lb = QLabel('Save Mov Path')
        self.save_path_edt = QLineEdit()
        self.save_path_btn = QPushButton('Browse')

        save_path_lay = QHBoxLayout()
        save_path_lay.addWidget(save_path_lb)
        save_path_lay.addWidget(self.save_path_edt)
        save_path_lay.addWidget(self.save_path_btn)


        label_width = max(select_cam_lb.sizeHint().width(),
                            save_path_lb.sizeHint().width())
        select_cam_lb.setFixedWidth(label_width)
        save_path_lb.setFixedWidth(label_width)

        btn_width = max(self.cam_btn.sizeHint().width(),
                        self.save_path_btn.sizeHint().width())
        self.cam_btn.setFixedWidth(btn_width)
        self.save_path_btn.setFixedWidth(btn_width)


        frame_range_lb = QLabel('FrameRange')
        self.start_frame = QLineEdit()
        self.start_frame.setAlignment(Qt.AlignCenter)
        range_lb = QLabel('-')
        self.end_frame = QLineEdit()
        self.end_frame.setAlignment(Qt.AlignCenter)

        frame_range_lay = QHBoxLayout()
        frame_range_lay.addSpacing(11)
        frame_range_lay.addWidget(frame_range_lb)
        frame_range_lay.addWidget(self.start_frame)
        frame_range_lay.addWidget(range_lb)
        frame_range_lay.addWidget(self.end_frame)


        self.ok_btn = QPushButton('OK')
        self.ok_btn.setFixedHeight(30)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setFixedHeight(30)

        order_btn_lay = QHBoxLayout()
        order_btn_lay.addWidget(self.ok_btn)
        order_btn_lay.addWidget(self.cancel_btn)


        main_lay = QVBoxLayout()
        main_lay.addLayout(select_cam_lay)
        main_lay.addSpacing(5)
        main_lay.addLayout(save_path_lay)
        main_lay.addSpacing(5)
        main_lay.addLayout(frame_range_lay)
        main_lay.addSpacing(5)
        main_lay.addLayout(order_btn_lay)

        self.setLayout(main_lay)


    def message_box( self, error_type, title, message, confirm=False ):
        msg_box = QMessageBox

        if error_type == 'info':
            if confirm:
                msg_box = QMessageBox( self )
                msg_box.setIcon( QMessageBox.Information )
                msg_box.setText( message )
                msg_box.setStandardButtons( QMessageBox.Yes | QMessageBox.No )

                msg_box.exec_()

                if msg_box.clickedButton() == msg_box.button( QMessageBox.Yes ):
                    return 'yes'
                elif msg_box.clickedButton() == msg_box.button( QMessageBox.No ):
                    return 'no'
            else:
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


    def cam_select_btn_func(self, func_address):
        self.cam_btn.clicked.connect(func_address)


    def browse_btn_func(self, func_address):
        self.save_path_btn.clicked.connect(func_address)


    def ok_btn_func(self, func_address):
        self.ok_btn.clicked.connect(func_address)


    def close_ui( self, func_address ):
        self.cancel_btn.clicked.connect( func_address )


    def closeEvent( self, event ):
        print( "close Export Mov tool" )


class CamNodeTreeDialog(QDialog):
    selectSignal = Signal(object)
    closeSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cam node select')
        self.resize(200, 200)

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
            root_item.setData( 0, Qt.UserRole, root_node.path() )
            self.tree_wg.addTopLevelItem( root_item )

            self._set_root_tree(root_node, root_item, 'cam')

        else:
            dummy_item = QTreeWidgetItem([root_path])
            self.tree_wg.addTopLevelItem(dummy_item)

        self._parent = parent

        if parent:
            parent.installEventFilter( self )
            self.updatePosition()
        
        self.select_btn.clicked.connect(self.on_select_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)
    

    def _set_root_tree(self, node, parent_item, expected_type):
        for child in node.children():
            if child.type().name() == expected_type:
                child_item = QTreeWidgetItem([child.name()])
                child_item.setData(0, Qt.UserRole, child.path())

                parent_item.addChild( child_item )
                self._set_root_tree(child, child_item, expected_type)


    def eventFilter( self, object, event ):
        if object == self._parent and event.type() == QEvent.Move:
            self.updatePosition()
            return False
        return False


    def updatePosition(self):
        if not self._parent:
            return
        parent_pos = self._parent.pos()
        parent_size = self._parent.size()

        new_x = parent_pos.x() + parent_size.width()
        new_y = parent_pos.y()
        
        self.move(new_x, new_y)


    def closeEvent(self, event):
        if self._parent:
            self._parent.removeEventFilter(self)
        self.closeSignal.emit()
        super().closeEvent(event)


    def on_select_clicked( self ):
        selected_item = self.tree_wg.currentItem()

        if not selected_item:
            print('Select the Node plz!')
            return

        node_path = selected_item.data(0, Qt.UserRole)
        node = hou.node(node_path)

        if node.type().name() != 'cam':
            print('Select the cam node!')
            return

        self.selectSignal.emit(node)
        self.accept()


    def on_cancel_clicked(self):
        self.closeSignal.emit()
        self.reject()