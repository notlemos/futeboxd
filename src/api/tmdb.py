from ..utils.headers import headersTmdb
from itertools import islice, chain

import asyncio
import aiohttp

async def fetchDataTmdb(session, endpoint, mediaType):
    
    headers = headersTmdb()
    
    request = f"https://api.themoviedb.org/3/{mediaType}/{endpoint}/images"
    
    async with session.get(request, headers=headers) as response:
        if response.status != 200:
            print(response.status)
            return None
    
        responseData = await response.json()
    
    moviePosters = responseData.get('posters', [])
    movieBackdrops = responseData.get('backdrops', [])
    
    backdrop = next(islice((b for b in movieBackdrops if b.get('iso_639_1') is None),0 , None), None)
    poster = next(
        chain(
            (p for p in moviePosters if p.get('iso_639_1') == 'en'),
            (p for p in moviePosters if p.get('iso_639_1') is None),
            
            ),
            None
    )    
    
    posterPath = poster['file_path'] if poster else None 
    backdropPath = backdrop['file_path'] if backdrop else None
    
    return posterPath, backdropPath

# async def main():
#     async with aiohttp.ClientSession() as session:
        
#         result = await fetchDataTmdb(
#             session,
#             endpoint="11216",
#             mediaType="movie"
#         )
        
#         print(result)
        
# asyncio.run(main())