import os
 
path = os.getcwd()
 
for file in os.listdir(path):
    if file.endswith('.mp4'):
        name = os.path.join(path,file.strip('.mp4')+'_resize.mp4')
        input = os.path.join(path ,file)
        os.system(f'ffmpeg -i "{input}" -vf "scale=1080:1920"  -c:v libx264 -c:a aac -crf 30 -preset slow "{name}" ')
        # break