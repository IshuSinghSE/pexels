import os

path = "D:\\Python\\selenium\\scraping\\pexels\\videos\\ready"
filename = "pexels"

# Two connect path of two files , directory, etc
def connect(path1, path2="D:\\Python\\selenium\\scraping\\pexels\\videos\\ready"):
    return os.path.join(path2, path1)


count = 1
for file in os.listdir(path):
    old_name = connect(file)
    new_name = connect(f"{filename}{count}.mp4")
    new_name = connect(f"{filename}{count+1}.mp4");print('file with same name already exists, fixing conflict!') if os.path.exists(new_name) else new_name 
    os.rename(old_name, new_name)
    print(f'renamed {file} as {filename}{count}.mp4')
    count+=1
