from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from ..scraping.letterboxd import LetterboxdScrapingService
from ..api.tmdb import fetchDataTmdb

scrapLetterboxdService = LetterboxdScrapingService()

class LetterboxdImagesPillowService():
    def __init__(self):
        pass 
    
    @staticmethod
    async def handleMoviePoster(session, letterboxdUrl):
        movieId, mediaType = await LetterboxdScrapingService.getIdMovie(letterboxdUrl)
        if not movieId or mediaType:
            return None 
        
        posterPath, _ = await fetchDataTmdb(session, movieId, mediaType)
        if not posterPath:
            return 
        
        posterUrl = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{posterPath}"
        
        async with session.get(posterUrl) as response:
            if response.status != 200:
                return None 
            imageData = await response.read()
            return Image.open(BytesIO(imageData)).convert('RGBA')
    @staticmethod
    async def handleMovieBackDrop(session, letterboxdUrl):
        movieId, mediaType = await LetterboxdScrapingService.getIdMovie(letterboxdUrl)
        if not movieId or mediaType:
            return None 
        
        
        _, backdropPath = await fetchDataTmdb(session, movieId, mediaType)
        if not backdropPath:
            return 
        
        backdropUrl = f"https://image.tmdb.org/t/p/w1280{backdropPath}"
        async with session.get(backdropUrl) as response:
            if response.status != 200:
                return None 

            backdropData = await response.read()
            
            return Image.open(BytesIO(backdropData)).convert('RGBA')
        