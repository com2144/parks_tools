import hou
import stateutils
import objecttoolutils


import attrib_spliter_ui
from attrib_spliter_model import AttribSpliterModel


class AttribSpliter:
    def __init__( self, node ):
        self.selected_node = node
        self.model = AttribSpliterModel()
        self.ui = attrib_spliter_ui.AttribSpliterUI()
        
        self.valid = self.valid_check()
        if not self.valid:
            return

        self.get_select_node()

        self.ui.run_func( lambda: self.run_action() )
        self.ui.close_ui( lambda: self.ui.close() )


    def valid_check( self ):
        if len(self.selected_node) > 1:
            hou.ui.displayMessage( 'Select the one node', 
                severity=hou.severityType.Error )
            return False

        root_info = self.selected_node[0].path().split('/')[1]
        if root_info != 'obj':
            hou.ui.displayMessage( f'Node root is not "/obj" :: you selected "/{root_info}"', 
                severity=hou.severityType.Error )
            return False
        
        return True


    def get_select_node( self ):
        self.ui.list_view.addItem( self.selected_node[0].path() )
        self.model.selected_node_info = self.selected_node[0]


    def run_action( self ):
        self.model.attirb_cls = str( self.ui.attrib_cls_cb.currentText() )
        self.model.renderer = str( self.ui.renderer_cb.currentText() )
        self.model.attrib_name = str( self.ui.attrib_name_edt.text() )
        
        if not self.model.attrib_name:
            hou.ui.displayMessage( f'Write {self.model.attirb_cls} Attribute', 
                severity=hou.severityType.Error )
            return
        
        geo = self.model.selected_node_info.geometry()

        render_set = hou.ui.displayMessage( 'You want render setting??', 
                                buttons=('OK', 'Cancel'), 
                                title='Render setting' )
        
        if self.model.attirb_cls == 'point':
            if not geo.findPointAttrib( self.model.attrib_name ):
                hou.ui.displayMessage( f'"{self.model.attrib_name}" is not exists in point attribute.', 
                    severity=hou.severityType.Error )
                return
            
            else:
                attrib_type = geo.findPointAttrib( self.model.attrib_name ).dataType()
                if attrib_type != hou.attribData.Int:
                    hou.ui.displayMessage( f'Wrtie the "int" attribute.', 
                                            severity=hou.severityType.Error )
                    return
                
                max_value = max( point.attribValue(self.model.attrib_name) for point in geo.points() )

        else:
            if not geo.findPrimAttrib( self.model.attrib_name ):
                hou.ui.displayMessage( f'"{self.model.attrib_name}" is not exists in primitive attribute.', 
                    severity=hou.severityType.Error )
                return
            
            else:
                attrib_type = geo.findPrimAttrib( self.model.attrib_name ).dataType()
                if attrib_type != hou.attribData.Int:
                    hou.ui.displayMessage( f'Wrtie the "int" attribute.', 
                                            severity=hou.severityType.Error )
                    return

                max_value = max( prim.attribValue(self.model.attrib_name) for prim in geo.prims() )

        self.node_creation( render_set, self.model.attirb_cls, max_value )


    def node_creation( self, render_set, attrib_cls, max_value ):
        parent_path = self.model.selected_node_info.parent().path()

        for i in range( max_value + 1):
            blast_node = hou.node( parent_path ).createNode( 'blast', f'blast_{self.model.attrib_name}_{i}' )
            blast_node.parm( 'group' ).set( f'@{self.model.attrib_name}=={i}' )
            if attrib_cls == 'point':
                blast_node.parm( 'grouptype' ).set( 3 )
            else:
                blast_node.parm( 'grouptype' ).set( 4 )
            blast_node.parm( 'negate' ).set( 1 )
            blast_node.setFirstInput( self.model.selected_node_info )
            blast_node.moveToGoodPosition()

            out_node = hou.node( parent_path ).createNode( 'null', f'OUT_{self.model.attrib_name}_{i}' )
            out_node.setFirstInput(blast_node)
            out_node.moveToGoodPosition()

            if render_set == 0:
                out_node_path = out_node.path()
                
                rend_geo = hou.node( '/obj' ).createNode( 'geo', f'{self.model.attrib_name}_{i}' )
                rend_geo.moveToGoodPosition()
                rend_geo_objmerge = rend_geo.createNode( 'object_merge', f'{self.model.attrib_name}_obj_{i}' )
                rend_geo_objmerge.parm( 'objpath1' ).set( out_node_path )
                rend_geo_objmerge.parm( 'xformtype' ).set( 1 )
                rend_geo_objmerge.moveToGoodPosition()
                
                objmerge_out_node = rend_geo.createNode( 'null', f'OUT_{i}' )
                objmerge_out_node.setFirstInput( rend_geo_objmerge )
                objmerge_out_node.moveToGoodPosition()
                objmerge_out_node.setRenderFlag( True )
                objmerge_out_node.setDisplayFlag( True )
                
                objmerge_out_path = objmerge_out_node.path()

                if self.model.renderer in [ 'mantra' ]:
                    if i == 0: 
                        if hou.node( '/obj/sunlight1' ) is None and hou.node( '/obj/skylight1' ) is None:
                            scene_viewer_inst = stateutils.findSceneViewer()
                            objecttoolutils.createSkyLight({'scene_viewer': scene_viewer_inst})
                        
                        if hou.node( '/obj/cam1' ) is None:
                            scene_viewer_panetab = hou.ui.paneTabOfType( hou.paneTabType.SceneViewer )
                            viewport = scene_viewer_panetab.curViewport()
                            cam_state = viewport.cameraToModelTransform()
                            cam_node = hou.node( '/obj' ).createNode( 'cam', 'cam1' )
                            cam_node.setWorldTransform( cam_state )
                            cam_node.moveToGoodPosition()
                    
                    rend_out = hou.node( '/out' ).createNode( 'ifd', f'{self.model.attrib_name}_rend_{i}' )
                    rend_out.parm( 'camera' ).set( '/obj/cam1' )
                    rend_out.parm( 'vobject' ).set('')
                    rend_out.parm( 'forceobject' ).set( objmerge_out_path )
                    rend_out.parm( 'alights' ).set('')
                    rend_out.parm( 'forcelights' ).set( '/obj/sunlight1 /obj/skylight1' )
                    rend_out.moveToGoodPosition()

                elif self.model.renderer in [ 'karma' ]:
                    sop_import = hou.node( '/stage' ).createNode( 'sceneimport::2.0', f'{self.model.attrib_name}_sceneimport_{i}')
                    sop_import.parm( 'objdestpath' ).set( '/obj' )
                    sop_import.parm( 'forceobjects' ).set( f'/obj/{self.model.attrib_name}_{i}' )
                    sop_import.moveToGoodPosition()

                    dome_light = hou.node( '/stage' ).createNode( 'domelight::3.0', f'domelight_{i}' )
                    if i > 0:
                        intens_expr = f'ch("../domelight_0/xn__inputsintensity_i0a")'
                        dome_light.parm( 'xn__inputsintensity_i0a' ).setExpression( intens_expr, language=hou.exprLanguage.Hscript )

                        expos_expr = f'ch("../domelight_0/xn__inputsexposure_vya")'
                        dome_light.parm( 'xn__inputsexposure_vya' ).setExpression( expos_expr, language=hou.exprLanguage.Hscript )

                        first_dome_light = hou.node( '/stage/domelight_0' )
                        source_light_parm_tuple = first_dome_light.parmTuple( 'xn__inputscolor_zta' )
                        target_light_parm_tuple = dome_light.parmTuple( 'xn__inputscolor_zta' )

                        for src_light_parm, tgt_light_parm in zip( source_light_parm_tuple, target_light_parm_tuple ):
                            tgt_light_parm.setExpression( f'ch("../domelight_0/{src_light_parm.name()}")', 
                                                            language=hou.exprLanguage.Hscript )

                    dome_light.setFirstInput( sop_import )
                    dome_light.moveToGoodPosition()

                    camera = hou.node( '/stage' ).createNode( 'camera', f'camera_{i}' )
                    if i == 0:
                        scene_viewer = hou.ui.paneTabOfType( hou.paneTabType.SceneViewer )
                        viewport = scene_viewer.curViewport()
                        cam_state = viewport.cameraToModelTransform()

                        translate = cam_state.extractTranslates()
                        rotate = cam_state.extractRotates()
                        scale = cam_state.extractScales()

                        camera.parmTuple( 't' ).set( translate )
                        camera.parmTuple( 'r' ).set( rotate )
                        camera.parmTuple( 's' ).set( scale )
                    else:
                        first_camera = hou.node( '/stage/camera_0' )

                        for param_name in ['t', 'r', 's']:
                            source_cam_parm_tuple = first_camera.parmTuple(param_name)
                            target_cam_parm_tuple = camera.parmTuple(param_name)

                            for src_cam_parm, tgt_cam_parm in zip( source_cam_parm_tuple, target_cam_parm_tuple ):
                                tgt_cam_parm.setExpression( f'ch("../camera_0/{src_cam_parm.name()}")', 
                                                            language=hou.exprLanguage.Hscript )
                    
                    camera.setFirstInput( dome_light )
                    camera.moveToGoodPosition()

                    karma_set = hou.node( '/stage' ).createNode( 'karmarenderproperties', f'karma_render_settings_{i}' )
                    karma_set.parm( 'camera' ).set( f'/cameras/camera_{i}' )
                    karma_set.setFirstInput( camera )
                    karma_set.moveToGoodPosition()

                    output = hou.node( '/stage' ).createNode( 'usdrender_rop', f'usdrender_rop_{i}' )
                    
                    engine_expr = f'"BRAY_HdKarma" + ifs(strmatch(chs("../karma_render_settings_{i}/engine"), "xpu"), "XPU", "")'
                    output.parm( "renderer" ).setExpression( engine_expr, language=hou.exprLanguage.Hscript )

                    render_set_expr = f'chs("../karma_render_settings_{i}/primpath")'
                    output.parm( "rendersettings" ).setExpression( render_set_expr, language=hou.exprLanguage.Hscript )

                    motion_blur_expr = f'1 - ch("../karma_render_settings_{i}/enablemblur")'
                    output.parm( "husk_instantshutter" ).setExpression( motion_blur_expr, language=hou.exprLanguage.Hscript )

                    output.setFirstInput( karma_set )
                    output.moveToGoodPosition()
        
        hou.ui.displayMessage( 'Attrib Spliter Job Done!' )