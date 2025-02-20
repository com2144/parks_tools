import os
import re
from datetime import datetime
import platform
import shutil

import hou

def load():
    current_path = hou.hipFile.path()
    if platform.system == 'Windows':
        current_path = current_path.replace('/', '\\')

    if not os.path.exists( current_path ):
        hou.ui.displayMessage( f'"{current_path}" is not exists.',
                              severity=hou.severityType.Error,
                              title='Path not Exists' )
        return
    
    memo_sig = hou.ui.displayMessage( 'Do you want to write the memo?', 
                                    buttons=('OK', 'Cancel'), 
                                    title='Write the memo question' )
    
    if memo_sig == 0 :
        memo = hou.ui.readInput( 'Write the memo' )
        memo = memo[1]
    else:
        memo = ''
    
    now = datetime.now()
    now = now.strftime( '%Y-%m-%d' )

    current_file_name, ext = os.path.splitext( os.path.basename(current_path) )
    current_file_name_split = current_file_name.split('.')
    current_ver = current_file_name_split[1]

    match = re.match( r"v\d{3}$", current_ver )

    houdini_dir = os.path.dirname( current_path )
    fx_dir = os.path.dirname( os.path.dirname( houdini_dir ) )

    keep_path = os.path.join( fx_dir, 'keep', f'{current_file_name}{ext}' )

    if os.path.exists( keep_path ):
        keep_path = os.path.join( fx_dir, 'keep', f'{current_file_name}_{now}{ext}' )
    
    shutil.copyfile( current_path, keep_path )

    if match:
        ver_num = int(match.group(0)[1:])
        new_ver = f'v{ver_num+1:03d}'

        if memo:
            new_file_name = f'{current_file_name_split[0]}_{memo}.{new_ver}{ext}'
        else:
            new_file_name = f'{current_file_name_split[0]}.{new_ver}{ext}'
        
        new_file_path = os.path.join( houdini_dir, new_file_name )
    
    else:
        if memo:
            new_file_name = f'{current_file_name_split[0]}_{now}_{memo}.{new_ver}{ext}'
        else:
            new_file_name = f'{current_file_name_split[0]}_{now}.{new_ver}{ext}'
        
        new_file_path = os.path.join( houdini_dir, new_file_name )

    if not os.path.exists( new_file_path ):
        hou.hipFile.save( new_file_path )
        hou.hipFile.load( new_file_path )

    success_msg = 'success copy and version up hip file\n'
    success_msg += ('=' * 70) + '\n'
    success_msg += f'Copy file path :: {keep_path}\n'
    success_msg += f'Version up path :: {new_file_path}\n'

    hou.ui.displayMessage( success_msg )