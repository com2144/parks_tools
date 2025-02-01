

class Options:
    def __init__( self, model, ui, data_list):
        self.model = model
        self.ui = ui
        self.data_list = data_list
    

    def _get_options( self ):
        options_list = []
        for data in self.data_list:
            item_list = []

            if self.model.is_options and data[0]:
                if self.model.is_resize:
                    item_list.append( self.model.resize )
                else:
                    item_list.append( 'origin' )
                
                if self.model.is_fps:
                    item_list.append( self.model.fps )
                else:
                    item_list.append( '23.976' )
                
                if self.model.is_codec:
                    item_list.append( self.model.codec )
                else:
                    item_list.append( 'H.264' )
            
            else:
                item_list = [
                    'origin',
                    '23.976',
                    'H.264'
                ]
            options_list.append( item_list )
        
        return options_list

    
    def _get_subs( self ):
        sub_list = []
        for data in self.data_list:
            item_list = []
            
            if self.model.is_sub and data[0]:
                if self.model.is_version:
                    item_list.append( self.model.version)
                else:
                    item_list.append( '' )

                if self.model.is_memo:
                    item_list.append( self.model.memo )
                else:
                    item_list.append( '' )

            else:
                item_list = [
                    '',
                    ''
                ]
            sub_list.append( item_list )
        
        return sub_list