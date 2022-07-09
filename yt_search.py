from youtubesearchpython import VideosSearch

def lookup(search):
    search = VideosSearch(search, 1)
    res = search.result()
    link = res['result'][0]['link']
    return link