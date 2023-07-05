# parks_houdini_tools
- hython이 필요합니다
- 환경변수에 houdini/bin을 PATH에 추가하세요

## fx_pipline
![캡처](https://github.com/com2144/parks_houdini_tools/assets/125478486/7a0fceee-d079-4db0-808d-bf5138e50df6)
- 사용법  
  [https://vimeo.com/841853026](https://vimeo.com/842476628)
- fx를 작업 할 때 필요한 트리구조를 만들어줍니다.
### ex) asset name: test-project_char_boy_txt.png
- asset : chareter, enviroment, property, vehicle
- shot -> fx, plate
- houdini, maya, nuke에는 각 프로젝트 파일을 저장하면 됩니다.
- review에는 랜더 후 결과물을 넣으면 됩니다.
- plate에는 배경 이미지 파일을 저장하면됩니다. (org는 exr원본을 말하며, jpg는 org이미지를 컨버팅한 이미지, mp4는 jpg를 컨버팅한 영상입니다.)



# houdini shelf tab add script

## image_converter
### jpg -> mp4 / exr -> mp4
- fx작업을 하면서 생기는 애니메이션을 확인하고 싶을 때 사용합니다.

- ffmpeg 환경변수 설정 방법  
https://www.youtube.com/watch?v=PLbijyGIAEo

## multi_renamer
- 많은 양의 데이터 이름을 한 번에 바꿀 때 사용합니다.
- 웹에서 받아온 asset의 이름을 규칙에 맞게 tree 규칙에 맞게 고칠 때 유용합니다.

## publish_working_file
- houdini를 사용하면서 보통은 ctrl + s를 사용하다가 완전 새로운 버전으로 작업을 하고 싶을 때 사용하면 좋습니다.

# houdini hda

## reserv_cache hda
- 한 번에 캐시를 할 수 있도록 돕는 hda입니다.   
  
- 최초 제작: 문건용 | email: scmstarcraft@naver.com
- 수정 베포: 박선준 | email: com2144@gmail.com

- 사용법   
https://sunjune-study-diary.notion.site/multi-cache-hda-19042fb6907849799039fa678eebbef7
