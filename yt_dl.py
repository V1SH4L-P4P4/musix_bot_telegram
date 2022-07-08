#musicbot_main is parent
import youtube_dl

def src_find(url):
    global url_aud
    YDLoptions = {'format':"bestaudio"}
    with youtube_dl.YoutubeDL(YDLoptions) as ydl:
        info = ydl.extract_info(url, download=False)
        url_aud = info['formats'][0]['url']
        return url_aud

