# System modules

import re
import os
import csv
import time
import json
import random
import psutil
import glob
import pickle
import subprocess

from tqdm import tqdm
from PIL import ImageFont
from datetime import datetime

# selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# youtube-api modules
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload


def browser():
    if ("chrome.exe" in (i.name() for i in psutil.process_iter())):
        os.system("taskkill /im chrome.exe /f")

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")
    options.add_argument(
        "user-data-dir=C:/Users/Ishu1/AppData/Local/Google/Chrome Beta/User Data/")
    options.add_argument("profile-directory=Default")
    options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"

    return webdriver.Chrome(options=options, service=Service('C:/Users/Ishu1/OneDrive - Tech Outbox/zzz/chromedriver.exe'))


def getData():
    driver = browser()
    driver.get("https://chat.openai.com/c/083f5d0b-0609-4431-a82d-d638c836a81f")
    time.sleep(5)

    tables = driver.find_elements(By.CSS_SELECTOR, 'table')

    if not os.path.exists('tables'):
        os.mkdir('tables')

    for table in range(len(tables)):
        with open('tables/table{}.txt'.format(table+1), 'w') as f:
            f.write(tables[table].text)
        print('Got {} table!'.format(table+1))

    driver.quit()


def get_authenticated_service():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "assets/client_secret.json"

    if os.path.exists('assets/auth.bin'):
        with open('assets/auth.bin', 'rb') as f:
            credentials = pickle.load(f)
    else:
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        with open('assets/auth.bin', 'wb') as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


def upload(file):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    title = os.path.basename(file).strip('.mp4')

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "24",
                "description": f"{title.strip('.')} 💕  #crush #love #lovefacts #crushfacts #facts #psychology #psychologyfacts #relationship #relationshipfacts",
                "title": f"{title} 💕 ",
                "tags": ['crush', 'love', 'lovefacts', 'crushfacts', 'facts', 'psychology', 'psychologyfacts', 'relationship', 'relationshipfacts']
            },
            "status": {
                "privacyStatus": "private",
                # "publistAt": "2023-10-03T14:13+05:30"
            }
        },

        media_body=MediaFileUpload(file, resumable=True)
    )
    response = request.execute()

    with open('temp.json', 'w') as f:
        json.dump(response, f, indent=4)

    time.sleep(10)
    print(f"https://www.youtube.com/shorts/{response['id']}")


def fit_text(string: str, frame_width, font):
    translation_font = ImageFont.FreeTypeFont(
        font, size=75, encoding="unic")

    split_line = [x.strip() for x in string.split()]
    lines = ""
    w = 0
    line_num = 0
    line = ""
    for word in split_line:
        # Make a test
        w = translation_font.getlength(" ".join([line, word]))

        if word:
            # If it exceeds the frame width, add a new line
            if w > (frame_width - (2 * 6)):  # Leave 6px margin on each side
                lines += line.strip() + "\f"
                line = ""

        line += word + " "

    lines += line.strip()  # Append leftover words
    return lines


def create_lines(longline, start, end, fontsize=75, fontfile='assets/fonts/OpenSansCondensedBold.ttf', firstPart=False, lastPart=False):

    fit = fit_text(longline, 700, fontfile)

    texts = []
    now = 0
    # breaking line on basis of '\f'
    for wordIndex in range(len(fit)):
        if fit[wordIndex] == '\f' or wordIndex == len(fit)-1:
            texts.append(fit[now:wordIndex+1].strip('\f'))
            now = wordIndex

    # adding multiple lines to video
    string = ''
    count = 0
    for line in texts:

        lines = str(line.replace("'", "'\\\\\\''") + '...') if (count == (len(texts)-1) and firstPart) else str(line.replace(
            "'", "'\\\\\\''") + '.') if (count == (len(texts)-1) and lastPart) else str(line.replace("'", "'\\\\\\''"))

        string += ''',drawtext=fontfile={}:fontsize={}:text='{}':fontcolor=white:bordercolor=black:borderw=5:x=(w-text_w)/2:y=(h-text_h)/2-100+{}:'enable=between(t,{},{})' '''.format(
            fontfile, fontsize, lines, count*100, start, end)
        count += 1

    # print(string)
    return string


def video_choose(path):
    dir = os.path.dirname(path)
    video = os.path.join(dir, random.choice(os.listdir(path)))
    return video


def createVideo(content, count):
    input_video = video_choose('assets/videos/ready/')
    date = datetime.now().strftime("%d-%m-%Y")
    output_video = f'upload/{date}/{content[1]}.mp4'
    font_file = 'assets/fonts/BebasKai.ttf'
    font_size = 95
    font_color = 'black'
    bg_color = 'white'

    if not os.path.exists(f"upload/{date}"):
        os.makedirs(f"upload/{date}")

    part1 = create_lines(content[1], 0.5, 7, firstPart=True)
    part2 = create_lines(content[2], 7.5, 10, lastPart=True)

    command = """ffmpeg -i {} -vf "scale=1080:1920" -vf "drawtext=fontfile={}:fontsize={}:text={}:fontcolor={}:box=1:boxcolor={}@1.0:boxborderw=20:x=(w-text_w)/2:y=(h-text_h)/4-100{}{}" -c:v libx264 -c:a aac -t 10 "{}" -y """.format(
        input_video, font_file, font_size, content[0], font_color, bg_color, str(part1), str(part2), output_video)
    os.system(command)


def main(file=None):
    dir = "assets/data"
    if [] == os.listdir(dir):
        getData()  # get data from chattGPT

    filename = file if file is not None else f"{dir}/table{len(os.listdir(dir))}.txt"

    with open(filename, 'r') as f:
        data = f.readlines()

    count = 1
    for line in tqdm(data[1:]):
        new = re.split(r" \d+ ", line.replace('.', '').strip('\n'))
        createVideo(new, count)
        count += 1


# if __name__ == "__main__":
#     main()
