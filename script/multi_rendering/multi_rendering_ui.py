import hou

from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *


DEV = 0

PREFERRED = QSizePolicy.Preferred


class MultRenderingUi( QDialog ):
    def __init__( self, parent=None ):
        super().__init__( parent )

        self.resize( 400, 400 )
        self.setWindowTitle( 'Multi Rendering' )

        font = QFont()
        font.setPointSize( 13 )
        font.setPixelSize( 13 )
        self.setFont( font )

        btn_lb = QLabel( 'Select Out/Stage Nodes  ' )
        self.pls_btn = QPushButton( '+' )
        self.mius_btn = QPushButton( '-' )

        btn_lay = QHBoxLayout()
        btn_lay.addWidget( btn_lb )
        btn_lay.addWidget( self.pls_btn )
        btn_lay.addWidget( self.mius_btn )


        render_lb = QLabel( 'Render Node List' )
        self.render_tbl = RenderTable()

        render_list_lay = QVBoxLayout()
        render_list_lay.addWidget( render_lb )
        render_list_lay.addWidget( self.render_tbl )


        updown_lb = QLabel( 'Render Up / Down' )
        self.up_btn = QPushButton( '△' )
        self.down_btn = QPushButton( '▽' )

        updown_lay = QHBoxLayout()
        updown_lay.addWidget( updown_lb )
        updown_lay.addWidget( self.up_btn )
        updown_lay.addWidget( self.down_btn )


        self.all_chk = QCheckBox( 'Render Check' )
        self.render_btn = QPushButton( 'Render' )
        self.render_btn.setFixedHeight( 30 )
        self.cancel_btn = QPushButton( 'Cancel' )
        self.cancel_btn.setFixedHeight( 30 )

        order_btn_lay = QHBoxLayout()
        order_btn_lay.addWidget( self.all_chk )
        order_btn_lay.addSpacerItem(
            QSpacerItem( 180, 200, PREFERRED, PREFERRED )
        )
        order_btn_lay.addWidget( self.render_btn )
        order_btn_lay.addWidget( self.cancel_btn )


        main_lay = QVBoxLayout()
        main_lay.addLayout( btn_lay )
        main_lay.addSpacing( 5 )
        main_lay.addLayout( render_list_lay )
        main_lay.addLayout( updown_lay )
        main_lay.addSpacing( 13 )
        main_lay.addLayout( order_btn_lay )

        self.setLayout( main_lay )

        self.close_call_back = None


    def set_close_callback( self, callback ):
        self.close_call_back = callback


    def plus_btn_func( self, func_address ):
        self.pls_btn.clicked.connect( func_address )


    def minus_btn_func( self, func_address ):
        self.mius_btn.clicked.connect( func_address )


    def up_btn_func( self, func_address ):
        self.up_btn.clicked.connect( func_address )


    def down_btn_func( self, func_address ):
        self.down_btn.clicked.connect( func_address )


    def all_render_chk_func( self, func_address ):
        self.all_chk.toggled.connect( func_address )


    def render_btn_func( self, func_address ):
        self.render_btn.clicked.connect( func_address )


    def reset_ui(self):
        self.render_tbl.clearContents()
        self.render_tbl.setRowCount(0)


    def close_ui(self, func_address):
        def slot():
            self.reset_ui()
            func_address()
        self.cancel_btn.clicked.connect( slot )


    def close_ui( self, func_address ):
        self.cancel_btn.clicked.connect( func_address )


    def closeEvent( self, event ):
        if self.close_call_back:
            self.close_call_back()
        
        print( "close Multi Rendering tool" )
        event.accept()


class NodeTreeDialog( QDialog ):
    selectSignal = Signal( object )
    closeSignal = Signal()
    
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.setWindowTitle( 'Rop or Stage out node select' )
        self.resize(400, 400)

        self.tree_wg = QTreeWidget()
        self.tree_wg.setHeaderLabels( ["Node Name"] )
        self.tree_wg.setSelectionMode( QAbstractItemView.ExtendedSelection )

        self.select_btn = QPushButton( 'Select' )
        self.cancel_btn = QPushButton( 'Cancel' )

        btn_lay = QHBoxLayout()
        btn_lay.addWidget( self.select_btn )
        btn_lay.addWidget( self.cancel_btn )

        tree_lay = QVBoxLayout()
        tree_lay.addWidget( self.tree_wg )
        tree_lay.addLayout( btn_lay )
        self.setLayout( tree_lay )

        for root_path in ['/out', '/stage']:
            expected_type = 'ifd' if root_path == '/out' else 'usdrender_rop'
            root_node = hou.node( root_path )
            if root_node:
                root_item = QTreeWidgetItem( [root_node.name()] )
                root_item.setData( 0, Qt.UserRole, root_node.path() )
                self.tree_wg.addTopLevelItem( root_item )

                self._set_root_tree( root_node, root_item, expected_type )
            else:
                dummy_item = QTreeWidgetItem( [root_path] )
                self.tree_wg.addTopLevelItem( dummy_item )
    
        if parent:
            self.parent = parent
            parent.installEventFilter( self )
            parent_pos = parent.pos()
            parent_size = parent.size()

            new_x = parent_pos.x() - parent_size.width() - 2
            new_y = parent_pos.y()
            
            self.move( new_x, new_y )

        self.select_btn.clicked.connect( self.on_select_clicked )
        self.cancel_btn.clicked.connect( self.on_cancel_clicked )


    def _set_root_tree( self, node, parent_item, expected_type ):
        for child in node.children():
            if child.type().name() == expected_type:
                child_item = QTreeWidgetItem( [child.name()] )
                child_item.setData( 0, Qt.UserRole, child.path() )

                parent_item.addChild( child_item )
                self._set_root_tree( child, child_item, expected_type )


    def eventFilter( self, object, event ):
        if object == self.parent and event.type() == QEvent.Move:
            self.updatePosition()
        return super(NodeTreeDialog, self).eventFilter(object, event)


    def updatePosition( self ):
        parent_pos = self.parent.pos()
        parent_size = self.parent.size()

        new_x = parent_pos.x() - parent_size.width() - 2
        new_y = parent_pos.y()
        
        self.move( new_x, new_y )


    def on_select_clicked( self ):
        selected_items = self.tree_wg.selectedItems()
        selected_nodes = []

        for item in selected_items:
            node_path = item.data( 0, Qt.UserRole )
            node = hou.node( node_path )
            if node:
                selected_nodes.append( node )
        
        if not selected_nodes:
            print( 'Select the Node plz!' )
            return

        self.selectSignal.emit( selected_nodes )
        self.accept()


    def on_cancel_clicked( self ):
        self.closeSignal.emit()
        self.reject()


class RenderTable( QTableWidget ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.verticalHeader().hide()
        self.setColumnCount( 3 )
        self.setHorizontalHeaderLabels(
            ['Check', 'Node Path', 'Order']
        )

        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 220)


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



if __name__ == '__main__':
    if DEV:
        import sys
        app = QApplication( sys.argv )

        main_win = MultRenderingUi()
        main_win.show()

        sys.exit( app.exec_() )