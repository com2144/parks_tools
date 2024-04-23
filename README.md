# parks_tools
## houdini otls, script, pipeline_tool
- You need the 'hython'
- ```shell
pip install PySide2
``` 
- Add to environment variable 'houdini-version/bin' to 'PATH'.


# houdini shelf tab add script

## before_render_memory_clear
- When you render or caching work, clearing tmporary memory.
- This script save current scene file and restart hip file.

## center_pivot_transform
- Automatic set center pivot to transform node. 

## image_converter
### jpg -> mp4 / exr -> mp4
- You cofirmed flipboox image. 

- How to set ffmpeg environment path.  
https://www.youtube.com/watch?v=PLbijyGIAEo

## multi_cache_script
- below the multi_cache_hda method in this script.

## path_spilt
- If you want to split the 'path' attribute, you can do split by the '/' information.

## publish_working_file
- If you split the version, like v001, v002 two different hip file, This script save split the version secne files.

## select_node_render_setting
- If you rendering instancing point to geometry, This script help to point by point to make mantra node.


# pipeline tool
## excel_convert_uploader
- When you use the shotgrid, This tool help the wrrited by many excel data to shotgrid project, sequence, shot upload the informations.

## fx_pipline
![캡처](https://github.com/com2144/parks_houdini_tools/assets/125478486/7a0fceee-d079-4db0-808d-bf5138e50df6)
- How to use  
  [https://vimeo.com/841853026](https://vimeo.com/842476628)
- You worked fx, that make to folder tree.
### ex) asset name: test-project_char_boy_txt.png
- asset : chareter, enviroment, property, vehicle
- shot -> fx, plate
- houdini, maya, nuke (You save the scene file.)
- review folder use to render or mov file. 
- At the plate directory, you save the background image. (org is original exr or dpx file. jpg is org image converting, mp4 is jpg converting to video.)

## mp4_downloader
- When you used to shotgrid action menu items, This tool can help the image to video data.

## multi_renamer
- When you use to many data's renaming.
- If you worng about asset name or shot name, This tool help multiple renaming file name.


# otls - houdini hda

## multi_cache_hda(reserv_cache hda)
- This hda help to execute many file cache node.
  
- first made by 문건용 | email: scmstarcraft@naver.com
- edit relese by 박선준 | email: com2144@gmail.com

- How to use   
https://sunjune-study-diary.notion.site/multi-cache-hda-19042fb6907849799039fa678eebbef7
