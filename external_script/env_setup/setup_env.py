import os
import re
import platform
import sys


import setup_gui
from setup_model import EnvSetupModel


NOW_PATH = os.path.dirname( os.path.abspath(sys.argv[0]) )


class EnvSetup:
    def __init__(self):
        self.ui = setup_gui.EnvSetupUi()
        self.model = EnvSetupModel()

        self.add_env_list()

        self.ui.add_btn.clicked.connect( self._set_env_data )
        self.ui.reset_btn.clicked.connect( self._set_reset_env )
        self.ui.cancel_btn.clicked.connect( self.ui.close )


    def add_env_list(self):
        home_dir = os.path.expanduser('~')
        system = platform.system()

        if system == 'Windows':
            hou_dir = os.path.join(home_dir, 'Documents')
        elif system == 'Darwin':
            hou_dir = os.path.join(home_dir, 'Library', 'Perferences', 'houdini')
        else:
            hou_dir = home_dir

        for item in os.listdir( hou_dir ):
            child_path = os.path.join( hou_dir, item )
            if system != 'Darwin':
                if os.path.isdir( child_path ) and 'houdini' in item:
                    match = re.match(r"([a-zA-Z]+)([0-9.]+)", item)

                    version = match.group(2)

                    self.ui.env_cb.addItem( version )
                    self.model.version_env_dict[version] = os.path.join( child_path, 'houdini.env' )
            else:
                if os.path.isdir( child_path ) and re.match(r'^(\d+).(\d+)$', child_path):
                    self.ui.env_cb.addItem( version )
                    self.model.version_env_dict[version] = os.path.join( child_path, 'houdini.env' )


    def _set_env_data(self):
        parks_tool_dir = NOW_PATH
        for i in range(2):
            parks_tool_dir = os.path.dirname( parks_tool_dir )
        
        parks_tool_dir = parks_tool_dir.replace('\\', '/')

        parks_tool_site = '$PSJ_SITE'

        parks_otls = parks_tool_site + '/otls'
        parks_tool_bar = parks_tool_site + '/toolbar'

        houdini_version = str(self.ui.env_cb.currentText())
        env_file = self.model.version_env_dict[ houdini_version ]
        
        env_data = open( env_file, 'r' )
        env_data = env_data.read()

        if platform.system() == 'Windows':
            divide = ';'
        else:
            divide = ':'

        content = '\n#PSJ_SITE\n'
        content += f'PSJ_SITE = {parks_tool_dir}\n'

        content += '\n#PSJ_OTLS\n'
        content += f'HOUDINI_OTLSCAN_PATH = @/otls{divide}{parks_otls}\n'

        content += '\n#PSJ_TOOLBAR\n'
        content += f'HOUDINI_TOOLBAR_PATH = @/toolbar{divide}{parks_tool_bar}\n'
        
        if content not in env_data:
            try:
                with open( env_file, 'w' ) as file:
                    file.write( env_data + content )
                
                self.ui.message_box( 'info', 'Env Save', f'"{houdini_version}-houdini.env" file save.')
            
            except:
                self.ui.message_box( 'error', 'Env Save Error', f'"{houdini_version}-houdini.env" file save failed.')

        else:
            self.ui.message_box( 'warning', 'Env already Exists', 'env-set already Exist.' )


    def _set_reset_env( self ):
        parks_tool_dir = NOW_PATH
        for i in range(2):
            parks_tool_dir = os.path.dirname( parks_tool_dir )

        houdini_version = str(self.ui.env_cb.currentText())
        

        reset_sig = self.ui.message_box( 'warning', 'Reset Warning', 
                            f'You really reset the "{houdini_version}" version env file?', confirm=True )

        if reset_sig == 'yes':
            env_file = self.model.version_env_dict[ houdini_version ]
            env_data = open( env_file, 'r' )
            env_data = env_data.readlines()

            content = ''
            for env_content in env_data:      
                if '#PSJ_SITE\n' == env_content:
                    break
                else:
                    content += env_content

            try:
                with open( env_file, 'w' ) as file:
                    file.write( content )

                self.ui.message_box( 'info', 'Reset env complete', f'Reset "{houdini_version}" version env file complete')
                
            except:
                self.ui.message_box( 'error', 'Reset env error', f'Reset "{houdini_version}" version env file error')
            
        

if __name__ == '__main__':
    app = setup_gui.QApplication( sys.argv )

    env_setup = EnvSetup()
    
    main_ui = env_setup.ui
    main_ui.show()

    sys.exit( app.exec_() )