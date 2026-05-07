import discord 
from discord.ext import commands
import logging
from utils.ytShortsService import YoutubeShortsService
import os

logger = logging.getLogger(__name__)
youtubeShortsService = YoutubeShortsService()


class GetRandomYoutubeShorts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        
    @commands.command(name="shorts")
    async def getRandomShort(self, ctx, *, tag: str):
        await ctx.message.add_reaction("<:loading:1372046197573025792>")
        
        videoUrl = youtubeShortsService.searchYoutubeShorts(tag)

        if videoUrl == None:
            await ctx.reply("Falha ao baixar.")
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("❌")
            return 
        
        videoPath = youtubeShortsService.downloadYoutubeShorts(videoUrl)
        
        try: 
            userAnswer = await ctx.reply(file=discord.File(videoPath), mention_author=True)
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("<:check:1372079293403889704>")
            await userAnswer.add_reaction("<:youtubeplay:1372638557650292797>")
            
            await self.bot.wait_for(
                "reaction_add",
                timeout=60.0,
                check=lambda r, u: (
                    u != ctx.bot.user and
                    r.message.id == userAnswer.id and
                    hasattr(r.emoji, 'id') and 
                    r.emoji.id == 1372638557650292797
                )
            )
            
            await ctx.reply(f"<{videoUrl}>", mention_author=False)
            os.remove(videoPath)
            return
        except Exception as e:
            await ctx.send(e)
            return e 
    

async def setup(bot):
    await bot.add_cog(GetRandomYoutubeShorts(bot))