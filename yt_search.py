from youtubesearchpython import VideosSearch
from youtubesearchpython import Video
from youtubesearchpython import ResultMode

def lookup(search):
    global res
    search = VideosSearch(search, 1)
    res = search.result()
    link = res['result'][0]['link']
    return link

def search_title(url):
    search = Video.getInfo(url, mode= ResultMode.json)
    return search['title']

#print(search_title('https://www.youtube.com/watch?v=H5v3kku4y6Q'))
