from api import main, upload, get_authenticated_service
import googleapiclient.errors
import os
import glob
import shutil
import datetime


date = datetime.datetime.now().strftime("%d-%m-%Y")
dir = os.path.join('upload', date)

for video in glob.glob(f"{dir}\*.mp4"):

    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(os.path.join(dir, 'uploaded')):
        os.makedirs(os.path.join(dir, 'uploaded'))

    try:
        upload(video)
        shutil.move(os.path.join(dir, video),
                    os.path.join(dir, 'uploaded', video))
        print("\033[0;36m", os.path.basename(video), "\033[0;32m uploaded 💕")

    except googleapiclient.errors.ResumableUploadError:
        print('\033[0;36m >\033[0;31m Quota exceeded 🥺,\033[0;35m try again later.')
        break
