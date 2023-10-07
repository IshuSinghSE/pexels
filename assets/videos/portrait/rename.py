import os, glob, re
 
path = os.getcwd()
count = 2
 
def rename(file):
    global count
    filename = os.path.basename(file)
    dirname = os.path.dirname(file) 
    new_name = os.path.join(dirname, f'pexels{str(count)}.mp4')
    if True:
        # os.rename(file, new_name)
        print(file, new_name)
        count +=1

    else:
        count +=1
        
for file in os.listdir(path):
       filename = os.path.basename(file)
       
       if filename.endswith('.mp4') and not filename.startswith('pexels\d+') and  len(filename) > 15:

        name = os.path.join(path,file.strip('.mp4')+'_resize.mp4')
        input = os.path.join(path ,file)
        os.system(f'ffmpeg -i "{input}" -vf "scale=1080:1920"  -c:v libx264 -c:a aac -crf 30 -preset slow "{name}" ')