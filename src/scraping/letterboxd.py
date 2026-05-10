import asyncio

import aiohttp
from bs4 import BeautifulSoup
import cloudscraper
from ..utils.headers import headersScraping
from curl_cffi.requests import AsyncSession
from curl_cffi import request


headers = headersScraping()


class LetterboxdScrapingService():
    
    @staticmethod
    def getProfileService(url):
        scraper = cloudscraper.create_scraper()
    
        
        response = scraper.get(url, timeout=10, headers=headers)
        
        if response.status_code != 200:
            return None
        
        soupResponse = BeautifulSoup(response.text, 'html.parser')
        
        imageTag = soupResponse.find("meta", property="og:image")
        image = imageTag["content"] if imageTag else None 
        
        nameTag = soupResponse.find("span", class_="displayname tooltip")
        name = nameTag.get_text(strip=True) if nameTag else None 
        
        patronTag = soupResponse.find("span", class_="badge -patron")
        patron = patronTag.get_text(strip=True) if patronTag else None
        
        return image, name, patron

    @staticmethod
    def getUserFavoritesService(url):
        scraper = cloudscraper.create_scraper()
        
        response = scraper.get(url, timeout=10, headers=headers)
        
        if response.status_code != 200:
            return None
        
        soupResponse = BeautifulSoup(response.text, "html.parser")
        
        favoriteMovies = soupResponse.select("li.griditem .favourite-production-poster-container")
        allDataFavoriteMovies = []
        
        for movie in favoriteMovies:
            reactComponent = movie.select_one("div.react-component")
            imageComponent = movie.select_one("img")
            
            
            targetLink = reactComponent.get("data-item-link")
            movieName = imageComponent.get("alt")
            
            
            allDataFavoriteMovies.append({
                "movie": movieName,
                "target-link": "https://letterboxd.com" + targetLink
            })
        
        return allDataFavoriteMovies
    async def getIdMovie(url):
        async with AsyncSession(impersonate="chrome104") as session:
            response = await session.get(url, timeout=10, headers=headers)
            
            if response.status_code != 200:
                print(response.status_code)
                return None, None 
            
            soupContent = BeautifulSoup(response.text, "html.parser")
            
            linkTmdbContent = soupContent.select_one("p.text-link.text-footer a[data-track-action='TMDB']")
            
            movieId = linkTmdbContent["href"].strip("/").split("/")[-1]
            mediaType = linkTmdbContent["href"].strip("/").split("/")[-2]
            
            return movieId, mediaType



# async def main():
#     async with aiohttp.ClientSession() as session:
        
#         result = await LetterboxdScrapingService.getIdMovie(
#             url="https://letterboxd.com/film/the-apartment/"
#         )
        
#         print(result)
        
# asyncio.run(main())