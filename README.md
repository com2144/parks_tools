# parks_tools (Pipeline and Houdini tool )
## External_script
##### On the Windows operating system, you can simply run it as a `.exe` file.

##### If you are not using Windows, you need to enter the following command in Python.

```shell
pip install PySide2
```


### 1. env_setup
- This tool sets up the environment variables required to use the Parks tool.

##### How to use   
<a href="https://sunjune-study-diary.notion.site/env_setup-1aa19d11eb3f80318b9bcd837f9eb407" target="_blank">
    Env Setup Manual
</a>
<br></br>

### 2. mp4_converter
- This tool converts files in `mp4`, `mov`, `png`, `jpg`, `jpeg`, `exr`, `dpx` formats into mp4.
- To use this tool, `ffmpeg` must be installed in `mp4_converter/tools`.

##### How to use   
<a href="https://sunjune-study-diary.notion.site/mp4_converter-1aa19d11eb3f80d28e46c62823ff8cc4" target="_blank">
    Mp4 Converter
</a>
<br></br>

### 3. multi_copy
- This tool allows multiple files and directory to be copied into a single directory.
- Supported files formats: `mov`, `mp4`, `dpx`, `exr`, `jpg`, `jpeg`, `png`, `tiff`.

##### How to use   
<a href="https://sunjune-study-diary.notion.site/multi_copy-1aa19d11eb3f80ac958aede7fe198798" target="_blank">
    Multi Copy
</a>
<br></br>

### 4. multi_renamer
- Allows selecting a folder and renaming the files within it.
- Renaming follows a sequential process.
    - Example: `foo → test`, `test → poo` Final name: `poo`.
- Supported files formats: `mov`, `mp4`, `dpx`, `exr`, `jpg`, `jpeg`, `png`, `tiff`
<br></br>

## Otls - Houdini HDA
### 1. multi_cache_hda(reserv_cache hda)
- This hda help to execute multi file cache node.
<br></br>
- first made by 문건용 | email: scmstarcraft@naver.com
- edit relese by 박선준 | email: com2144@gmail.com

##### How to use   
<a href="https://sunjune-study-diary.notion.site/reserv_cache-hda-19042fb6907849799039fa678eebbef7" target="_blank">
    Multi Cache Manual
</a>
<br></br>

## Script
- When running in Houdini, this can be executed through `psj_fx_tool` and `psj_pipeline` tools.
    - `psj_fx_tool`
        - ![Image](https://github.com/user-attachments/assets/02ea766b-3ca7-4dc3-9636-e29d9e0c0e6f)
    - `psj_pipeline`
        - ![Image](https://github.com/user-attachments/assets/cf708d7e-961c-4698-bba8-e45047961046)
<br></br>

### psj_fx_tool
#### 1. memory_clear
- It is recommended to use this tool before `caching` or `rendering`.
- It helps clear background memory while working with hip files.
<br></br>

#### 2. center_pivot_extract
- When selecting and executing the `transform` node, the Pivot and Pivot Rotate values for X, Y, and Z are set to `$CEX`, `$CEY`, `$CEZ`, respectively.
<br></br>

#### 3. attrib_spliter
<img src="https://github.com/user-attachments/assets/3ac79e29-5388-4307-a7ba-e31ba63efce7" width="40%" height="auto">

- When specifying `Point` and `Prim` attributes, the tool divides the area into clusters based on the given attribute.
- If rendering is required, it automatically creates separate `Mantra` or `Karma` nodes for each clustered area. (add lights and viewport based camera)
- The cluster-related attribute must be an `int` value.
<br></br>

#### 4. multi_rendering
<img src="https://github.com/user-attachments/assets/f1e9d7e6-5c38-487e-99a7-75b18f577c8e" width="30%" height="auto">
<img src="https://github.com/user-attachments/assets/dad5480b-2147-42c9-96d7-66ac0e0615a0" width="30%" height="auto">
<img src="https://github.com/user-attachments/assets/6ce75f3a-ea47-45f6-8f72-b4cb8d87049e" width="30%" height="auto">

- Click the `+` button to load `Mantra` and `USD Render ROP` nodes related to rendering from `/out` and `/stage`.
Use the Up/Down buttons to adjust the render order.
- Checked nodes will be rendered; rendering will not proceed for unchecked nodes.
- Enabling `Render Check` selects all render nodes at once.
- After rendering, a preset is saved in the current hip file, so the next time you open it, the render nodes will automatically be loaded in the correct order.
<br></br>

#### 5. import_repath
<img src="https://github.com/user-attachments/assets/2ce47c41-5985-4eca-85ef-e1f27ab3825f" width="40%" height="auto">

- You can rename the file paths of `File`, `Alembic`, and `USD Import` nodes when importing files.
- Renaming follows a sequential process.
    - Example: `foo → test`, `test → poo` Final name: `poo`.
<br></br>

#### 6. bg_rendering
<img src="https://github.com/user-attachments/assets/8ec7eb38-e9b1-49f5-8097-7f160f972f13" width="40%" height="auto">
<img src="https://github.com/user-attachments/assets/10deb84b-26b3-4d6a-9492-0668b3fbf261" width="55%" height="auto">

- Before using this tool, You have to run `env_setup` first.
    - Please refer to the manual above for more details on `env_setup`.
- On `Windows`, run the `.bat` and `macOS` or `Linux`, run the `.sh`.
- Click the `Browse` button to load a `.hip` file.
- You can freely set the `save path`, `start frame`, and `end frame` of the render nodes within the `.hip` file.
    - You can selectively render based on the checkBoxes.
- Click Rendering to start the render process.
    - During rendering, you can check the render status via the terminal.
<br></br>
<br></br>

### psj_pipeline
#### 1. fx_pipeline
<img src="https://github.com/user-attachments/assets/c3fbc30c-9fc1-4792-b0d3-de2893c4e3ef" width="50%" height="auto">

- When you set the `Project Name` and `Houdini File Format`, a directory with the specified Project Name is created in the Save Folder.
- It follows the folder tree structure as shown below.
- The parent directory of the saved project is loaded as a preset the next time the tool is executed.
<br></br>
<img src="https://github.com/user-attachments/assets/e8b3d1c4-d08e-4f10-807f-83f5f88db38f" width="25%" height="auto">
<br></br>

#### 2. keep_working_file
- Before using this tool, you must first create a project through `fx_pipeline` and then open the hip file.
- The currently opened hip file is copied to the `keep` folder, and a new version of the hip file is created.
<br></br>

#### 3. render_naming
<img src="https://github.com/user-attachments/assets/baec1a80-7b72-475c-834a-35b59641f2c1" width="50%" height="auto">

- You can create a project using psj_fx_pipeline and use it afterward.
- This tool allows you to name render output files and supports version upgrades.
