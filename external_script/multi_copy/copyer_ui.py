import os
import sys


from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


ICON = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), 'icon' )


DEV = 0


class CopyUi( QDialog ):
    def __init__( self ):
        super().__init__()
        self.resize( 900, 300 )
        self.setWindowTitle( 'Multi Copy' )

        self.log_chk = QCheckBox( 'Copy Log List' )
        self.log_chk.setEnabled( True )
        self.log_chk.setChecked( False )


        orig_lb = QLabel( f'{"Orig":<10}' )
        self.orig_clear_btn = QPushButton( 'Clear' )
        self.orig_clear_btn.setFixedWidth( 70 )

        orig_info_lay = QHBoxLayout()
        orig_info_lay.addWidget( orig_lb )
        orig_info_lay.addWidget( self.orig_clear_btn )

        self.orig_tbl = OrigTable()
        self.orig_tbl.setMinimumWidth( 100 )

        orig_lay = QVBoxLayout()
        orig_lay.addLayout( orig_info_lay )
        orig_lay.addWidget( self.orig_tbl )

        copy_lb = QLabel( f'{">>>":^13}' )


        target_lb = QLabel( f'{"Target":<10}' )
        self.target_tbl = TargetTable()

        target_lay = QVBoxLayout()
        target_lay.addWidget( target_lb )
        target_lay.addWidget( self.target_tbl )


        self.copy_btn = QPushButton( 'Copy' )
        self.cancel_btn = QPushButton( 'Cancel' )
        self.copy_btn.setMinimumHeight( 30 )
        self.cancel_btn.setMinimumHeight( 30 )

        btn_lay = QHBoxLayout()
        btn_lay.addWidget( self.copy_btn )
        btn_lay.addWidget( self.cancel_btn )


        table_lay = QHBoxLayout()
        table_lay.addLayout( orig_lay )
        table_lay.addWidget( copy_lb )
        table_lay.addLayout( target_lay )


        main_lay = QVBoxLayout()
        main_lay.addWidget( self.log_chk )
        main_lay.addLayout( table_lay )
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


class OrigTable( QTableWidget ):
    itemsDropped = Signal( list )
    itemsUpdated = Signal( list )

    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.setSelectionMode( QAbstractItemView.SingleSelection )
        self.setAcceptDrops( True )
        self.setDragEnabled( True )
        self.viewport().setAcceptDrops( True )
        self.setDropIndicatorShown( True )
        self.horizontalHeader().setVisible( False )

        self.items = []

    
    def dragEnterEvent( self, event ):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    

    def dragMoveEvent( self, event ):
        if event.mimeData().hasUrls():
            event.setDropAction( Qt.CopyAction )
            event.accept()
        else:
            event.ignore()

    
    def dropEvent( self, event ):
        if event.mimeData().hasUrls():
            event.setDropAction( Qt.CopyAction )
            event.accept()
            links = [ str( url.toLocalFile() ) for url in event.mimeData().urls() ]
            self.itemsDropped.emit( links )
        else:
            new_order = []
            for row in range( self.rowCount() ):
                item = self.item( row, 0 )
                if item:
                    new_order.append( item.text() )
            
            self.itemsDropped.emit( new_order )


    def add_items( self, items ):
        if not items:
            return
        else:
            self.items = items
        
        self.verticalHeader().hide()
        self.setColumnCount( 2 )
        self.setRowCount( len(items) )

        self.setColumnWidth( 0, 50 )

        for row, item_text in enumerate( items ):
            self.setItem( row, 1, QTableWidgetItem( item_text ))
            rm_widget = RemoveBtnWidget( row, self )
            rm_widget.removeClicked.connect( self.remove_item )
            self.setCellWidget( row, 0, rm_widget )
    

    def remove_item( self, row ):
        self.removeRow( row )

        if row < len( self.items ):
            self.items.pop( row )
            self.itemsUpdated.emit( self.items )
            for i in range( self.rowCount() ):
                rm_widget = self.cellWidget(i, 0)
                if rm_widget:
                    rm_widget.row = i


class TargetTable( QTableWidget ):
    itemsDropped = Signal( list )
    itemsUpdated = Signal( list )

    def __init__( self, parent=None ):
        super().__init__( parent )
        self.horizontalHeader().setStretchLastSection( True )
        self.setEditTriggers( QAbstractItemView.NoEditTriggers )
        self.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.setSelectionMode( QAbstractItemView.SingleSelection )
        self.setAcceptDrops( True )
        self.setDragEnabled( True )
        self.viewport().setAcceptDrops( True )
        self.setDropIndicatorShown( True )
        self.horizontalHeader().setVisible( False )

        self.items = []

    
    def dragEnterEvent( self, event ):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    

    def dragMoveEvent( self, event ):
        if event.mimeData().hasUrls():
            event.setDropAction( Qt.CopyAction )
            event.accept()
        else:
            event.ignore()

    
    def dropEvent( self, event ):
        if event.mimeData().hasUrls():
            event.setDropAction( Qt.CopyAction )
            event.accept()
            links = [ str( url.toLocalFile() ) for url in event.mimeData().urls() ]
            self.itemsDropped.emit( links )
        else:
            new_order = []
            for row in range( self.rowCount() ):
                item = self.item( row, 0 )
                if item:
                    new_order.append( item.text() )
            
            self.itemsDropped.emit( new_order )


    def add_item( self, items ):
        if not items:
            return
        
        self.items = items

        self.verticalHeader().hide()
        self.setColumnCount( 2 )
        self.setRowCount( 1 )

        self.setColumnWidth( 0, 50 )

        self.setItem( 0, 1, QTableWidgetItem( self.items[0] ) )
        rm_widget = RemoveBtnWidget( 0, self )
        rm_widget.removeClicked.connect( self.remove_item )
        self.setCellWidget( 0, 0, rm_widget )
        self.itemsUpdated.emit( self.items )
    

    def remove_item( self ):
        if self.rowCount() > 0:
            self.removeRow()
            self.items = []
            self.itemsUpdated.emit( self.items )


class LogListView( QDialog ):
    def __init__( self, parent=None ):
        super().__init__( parent )
        self.setWindowTitle( 'Copy History Log' )
        self.resize( 900, 200 )

        self.list_widget = QListWidget()

        list_lay = QHBoxLayout()
        list_lay.addWidget( self.list_widget )

        self.setLayout( list_lay )

        if parent:
            self.parent = parent
            parent.installEventFilter( self )
            parent_pos = parent.pos()
            parent_size = parent.size()

            new_x = parent_pos.x()
            new_y = parent_pos.y() + parent_size.height() + 30

            self.move( new_x, new_y )


    def eventFilter( self, object, event ):
        if object == self.parent and event.type() == QEvent.Move:
            self.updatePosition()
        return super(LogListView, self).eventFilter( object, event)    


    def updatePosition(self):
        parent_pos = self.parent.pos()
        parent_size = self.parent.size()

        new_x = parent_pos.x()
        new_y = parent_pos.y() + parent_size.height() + 30

        self.move( new_x, new_y )    


    def set_log( self, log_item ):
        if isinstance( log_item, str ):
            self.list_widget.addItem( log_item )

        elif isinstance( log_item, list ):
            self.list_widget.addItems( log_item )


class RemoveBtnWidget( QWidget ):
    removeClicked = Signal( int )

    def __init__(self, row, parent=None ):
        super().__init__( parent )
        self.row = row

        rm_btn = QPushButton( '−' )
        # rm_btn.setIcon( QIcon( os.path.join( ICON, 'minus.png' ) ) )
        # rm_btn.setFlat( True )
        rm_btn.setMinimumSize( QSize( 50, 30 ) )
        rm_btn.setMaximumSize( QSize( 50, 30 ) )

        rm_lay = QHBoxLayout()
        rm_lay.addWidget( rm_btn )
        rm_lay.setAlignment( Qt.AlignCenter )
        rm_lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout( rm_lay )

        rm_btn.clicked.connect( self.remove_clicked )


    def remove_clicked( self ):
        self.removeClicked.emit( self.row )


if __name__ == '__main__':
    if DEV:
        app = QApplication( sys.argv )

        main_win = CopyUi()
        main_win.show()

        sys.exit( app.exec_() )