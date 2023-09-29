# selenium modules
import random
import csv
import subprocess
from PIL import ImageFont
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import psutil
import time
import os
import re


def browser():
    if ("chrome.exe" in (i.name() for i in psutil.process_iter())):
        os.system("taskkill /im chrome.exe /f")

    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("--log-level=3")
    options.add_argument(
        "user-data-dir=C:\\Users\\Ishu1\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
    options.add_argument("profile-directory=Default")
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

    return webdriver.Chrome(options=options, service=Service('C:\\Users\\Ishu1\\OneDrive - Tech Outbox\\zzz\\chromedriver.exe'))


def getTable():
    driver = browser()
    driver.get("https://chat.openai.com/c/dff8190f-125a-46f9-b62a-f42b6e537c40")
    time.sleep(5)

    tables = driver.find_elements(By.CSS_SELECTOR, 'table')

    if not os.path.exists('tables'):
        os.mkdir('tables')

    for table in range(len(tables)):
        with open('tables/table{}.txt'.format(table+1), 'w') as f:
            f.write(tables[table].text)
        print('Got {} table!'.format(table+1))

    driver.quit()


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


def create_lines(longline, start, end, fontsize=75, fontfile='OpenSansCondensedBold.ttf', firstPart=False, lastPart=False):

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
    input_video = video_choose('videos\\ready\\')
    output_video = f'upload/output{count}.mp4'
    font_file = 'BebasKai.ttf'
    text_file = 'OpenSansCondensedBold.ttf'
    font_size = 95
    font_color = 'black'

    part1 = create_lines(content[1], 0.5, 7, firstPart=True)
    part2 = create_lines(content[2], 7.5, 10, lastPart=True)

    command = """ffmpeg -i {} -vf "scale=1080:1920" -vf "drawtext=fontfile={}:fontsize={}:text={}:fontcolor={}:box=1:boxcolor=white@1.0:boxborderw=20:x=(w-text_w)/2:y=(h-text_h)/4-100{}{}" -c:v libx264 -c:a aac -t 10 {} -y """.format(
        input_video, font_file, font_size, content[0], font_color, str(part1), str(part2), output_video)
    # time.sleep(5)
    os.system(command)


def getText(file=None):
    with open('data/table2.txt', 'r') as f:
        data = f.readlines() 

    filename = "table1.csv"
    rows = []
    count = 1
    for line in tqdm(data[1:]):
        new = re.split(r" \d+ ", line.replace('.', '').strip('\n'))
        createVideo(new, count)
        count += 1
        # break

    # print(rows)
    #     # writing to csv file
    # with open(filename, 'w') as csvfile:
    #     # creating a csv writer object
    #     csvwriter = csv.writer(csvfile)

    #     # writing the fields
    #     csvwriter.writerow(["Topic", "part1", "part2"])

    #     # writing the data rows
    #     csvwriter.writerows(rows)


def split_txt_into_multi_lines(input_str: str, line_length: int):
    words = input_str.split(" ")
    line_count = 0
    split_input = ""
    for word in words:
        line_count += 1
        line_count += len(word)
        if line_count > line_length:
            split_input += "\n"
            line_count = len(word) + 1
            split_input += word
            split_input += " "
        else:
            split_input += word
            split_input += " "

    return split_input


getText()
