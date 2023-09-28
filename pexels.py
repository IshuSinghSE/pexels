import pexelsPy
import requests
from tqdm import tqdm

PEXELS_API = 'RK5CuP1Np8dzawFCOAiDn5NJgJAXj14IvxoyjuE3ve76otW1es4W4rWj'
api = pexelsPy.API(PEXELS_API)

pageNumbers = 1
resultsPage = 80

api.search_videos('nature/?orientation=portrait', page=pageNumbers, results_per_page=resultsPage)
videos = api.get_videos()


for data in tqdm(videos):
    url_video = 'https://www.pexels.com/video/' + str(data.id) + '/download'
    r = requests.get(url_video)
    with open('videos/'+data.url.split('/')[-2]+'.mp4', 'wb') as outfile:
        outfile.write(r.content)
