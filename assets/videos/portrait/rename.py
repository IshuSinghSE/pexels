import os
 
path = os.getcwd()
 
for i in os.listdir(path):
    name = (path+'\\temp\\'+i.strip('.mp4')+'_resize.mp4')
    input = path+'\\temp\\'+i
    os.system(f'ffmpeg -i "{input}" -vf "crop=1080:1920" "{name}" ')
    break