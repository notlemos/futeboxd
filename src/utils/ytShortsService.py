import yt_dlp
import string 
import random

class YoutubeShortsService():
    def __init__(self):
        pass
    
    def searchYoutubeShorts(self, query):
        query = f"shorts {query}"
        
        options = {
            'format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'dump_single_json': True,
            'no_cache_dir': True
        }
        
        URLS = []
        
        with yt_dlp.YoutubeDL(options) as ydl:
            YoutubeShortsResults = ydl.extract_info(f"ytsearch50:{query}", download=False)
            
        for entry in YoutubeShortsResults['entries']:
            if entry.get("duration") and entry["duration"] <= 120:
                URLS.append(entry["url"])
        if URLS:
            return random.choice(URLS) 
        return None
    def downloadYoutubeShorts(self, url):
        randomString = list(string.ascii_lowercase)
        
        output_path = '/tmp/short%s.%%(ext)s' % "".join(random.choices(randomString, k=4))
        
        options = {
            'format': 'bestvideo[ext=mp4][height<=720][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][height<=720][vcodec^=avc1]',
            'merge_output_format': 'mp4',
            'outtmpl': output_path,
            'quiet': True,
            'noplaylist': True,
            'no_cache_dir': True
        }
        
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
                infoDictonary = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(infoDictonary).rsplit('.', 1)[0] + '.mp4'
                return filename
            except Exception as error:
                return error 
        
        