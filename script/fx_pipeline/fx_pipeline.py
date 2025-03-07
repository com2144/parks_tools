import os
import platform
import json
import imp

import hou

import fx_pipeline_model
import fx_pipline_ui

imp.reload( fx_pipeline_model )
imp.reload( fx_pipline_ui )


NOW_PATH = os.path.dirname( os.path.abspath(__file__) )


class PipelineSetup:
    def __init__( self ):
        self.model = fx_pipeline_model.PipelineSetupModel()
        self.ui = fx_pipline_ui.PipelineSetupUi()

        self.preset_init()

        self.ui.set_save_dir_fun( lambda: self.set_save_dir() )
        self.ui.set_fx_pipeline_fun( lambda: self.set_fx_pipeline() )
        self.ui.close_ui( lambda: self.ui.close() )


    def set_save_dir( self ):
        home_path = os.path.expanduser( '~' )
        self.model.save_dir_path = fx_pipline_ui.QFileDialog.getExistingDirectory(
            self.ui,
            'Select Directory',
            home_path
        )
        self.ui.save_dir_edt.setText( self.model.save_dir_path )
    

    def set_fx_pipeline( self ):
        if platform.system == 'Windows':
            self.model.save_dir_path = self.model.save_dir_path.replace('/', '\\')
        if not self.model.save_dir_path:
            hou.ui.displayMessage( 'Choose the save Directory.', 
                                    severity=hou.severityType.Error )
            return
        
        self.model.project_name = self.ui.project_edt.text()
        if not self.model.project_name:
            hou.ui.displayMessage( 'Write the Project name.', 
                                    severity=hou.severityType.Error )
            return

        if ' ' in self.model.project_name:
            self.model.project_name = self.model.project_name.replace(' ', '_')
        
        self.model.asset_path = os.path.join( self.model.save_dir_path,
                                             self.model.project_name,
                                             'asset' )
        self.model.shot_path = os.path.join( self.model.save_dir_path,
                                            self.model.project_name,
                                            'shot' )
        
        if not os.path.exists( self.model.asset_path ):
            self.path_tree_init_set( 'asset' )
        
        if not os.path.exists( self.model.shot_path ):
            self.path_tree_init_set( 'shot' )

            if os.path.exists( self.model.houdini_dir_path ):
                ext = str( self.ui.ext_cb.currentText() )
                self.init_houdini_set( self.model.houdini_dir_path, ext )
        
        self.model.preset_dict['home'] = self.model.save_dir_path
        with open( self.model.preset_json, 'w' ) as file:
            json.dump( self.model.preset_dict, file)
        
        self.ui.close()


    def path_tree_init_set( self, tree_type ):
        if tree_type == 'shot':
            task_list = ['fx', 'plate']

            for task_item in task_list:
                if task_item == 'fx':
                    shot_list = ['work', 'ref', 'keep']

                    work_list = ['houdini', 'nuke', 'maya', 'cam', 'review']
                    ref_list = ['artwork', 'footage']

                    houdini_list = ['cache', 'script', 'tmp']
                    nuke_list = ['stock', 'script', 'tmp']
                    review_list = ['exr', 'png', 'mov', 'mp4', 'tmp', 'jpg']

                    for shot_item in shot_list:
                        if shot_item == 'work':
                            for work_item in work_list:
                                work_item_path = os.path.join( self.model.shot_path,
                                                            task_item,
                                                            shot_item,
                                                            work_item )
                                if not os.path.exists( work_item_path ):
                                    os.makedirs( work_item_path )
                                
                                if work_item == 'review':
                                    for review_item in review_list:
                                        review_item_path = os.path.join( work_item_path,
                                                                        review_item )
                                        if not os.path.exists( review_item_path ):
                                            os.makedirs( review_item_path )
                                
                                elif work_item == 'houdini':
                                    self.model.houdini_dir_path = work_item_path
                                    
                                    for houdini_item in houdini_list:
                                        houdini_item_path = os.path.join( work_item_path,
                                                                         houdini_item )
                                        if not os.path.exists( houdini_item_path ):
                                            os.makedirs( houdini_item_path )
                                
                                elif work_item == 'nuke':
                                    for nuke_item in nuke_list:
                                        nuke_item_path = os.path.join( work_item_path,
                                                                      nuke_item )
                                        if not os.path.exists( nuke_item_path ):
                                            os.makedirs( nuke_item_path )
                        
                        elif shot_item == 'ref':
                            for ref_item in ref_list:
                                ref_item_path = os.path.join( self.model.shot_path,
                                                            task_item,
                                                            shot_item,
                                                            ref_item )
                                if not os.path.exists( ref_item_path ):
                                    os.makedirs( ref_item_path )
                        
                        else:
                            keep_path = os.path.join( self.model.shot_path,
                                                        task_item,
                                                        shot_item)
                            if not os.path.exists( keep_path ):
                                os.makedirs( keep_path )
                
                else:
                    plate_list = ['jpg', 'png', 'mov', 'mp4']

                    for plate_item in plate_list:
                        plate_item_path = os.path.join( self.model.shot_path,
                                                       task_item,
                                                       plate_item )
                        if not os.path.exists( plate_item_path ):
                            os.makedirs( plate_item_path )

        elif tree_type == 'asset':
            asset_list = ['char', 'env', 'prop', 'veh', 'txt', 'hdr']

            for asset_item in asset_list:
                asset_item_path = os.path.join( self.model.asset_path,
                                               asset_item )
                if not os.path.exists( asset_item_path ):
                    os.makedirs( asset_item_path )


    def init_houdini_set( self, dir_path, ext ):
        houdini_file_name = os.path.join( dir_path, f'{self.model.project_name}_shot_work_fx_v001.{ext}' )
        if not os.path.exists( houdini_file_name ):
            hou.hipFile.save( houdini_file_name, save_to_recent_files=False )
            hou.hipFile.load( houdini_file_name )
            playbar = hou.playbar
            first_frame = 1001
            playbar.setFrameRange( first_frame, first_frame + 240 - 1 )


    def preset_init( self ):
        preset_dir = os.path.join( NOW_PATH, '.preset')
        if not os.path.exists( preset_dir ):
            os.makedirs( preset_dir )
        
        self.model.preset_json = os.path.join( preset_dir, 'user_preset.json' )
        if not os.path.exists( self.model.preset_json ):
            self.model.preset_dict = { 'home': '' }

            with open( self.model.preset_json, 'w' ) as file:
                json.dump( self.model.preset_dict, file )
        
        else:
            with open( self.model.preset_json, 'r' ) as file:
                self.model.preset_dict = json.load( file )

            if self.model.preset_dict['home']:
                sig_msg = 'Initial path is already exists.' + '\n'
                sig_msg += self.model.preset_dict['home'] + '\n'
                sig_msg += 'Do you want setting save path??'
                
                preset_sig = hou.ui.displayMessage(sig_msg, 
                                buttons=('OK', 'Cancel'),
                                severity=hou.severityType.ImportantMessage, 
                                title='Preset Exists')
                
                if preset_sig == 0:
                    self.ui.save_dir_edt.setText( self.model.preset_dict['home'] )
                    self.model.save_dir_path = self.model.preset_dict['home']

