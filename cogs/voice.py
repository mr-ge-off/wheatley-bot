from os import listdir, path
from urllib.parse import urlparse
from discord.ext import commands
import discord
import youtube_dl


class Voice(commands.Cog):
    enrichment_center_id = '734468488105558026'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def __init__(self, bot):
        self.bot = bot
        self.client = None
        self.queue = []


    @commands.command()
    async def join(self, ctx):
        """Joins the voice channel you're in."""

        voice = ctx.author.voice
        if voice:
            if self.client is None:
                self.client = await voice.channel.connect()
            elif self.client.channel != voice.channel:
                await self.client.move_to(voice.channel)
        else:
            await ctx.send('You have to be in a voice channel to make me !join one!')


    @commands.command()
    async def leave(self, ctx):
        """Leaves the voice channel I'm in."""

        if self.client:
            await self.client.disconnect()
            self.client = None


    @commands.command()
    async def music(self, ctx, link):
        """Plays the linked YouTube video."""

        if self.client is None:
            await ctx.channel.send('I have to have joined a channel to play !music.')
            return

        url = link if urlparse(link).netloc != '' else await search(args)
        with youtube_dl.YoutubeDL(Voice.ydl_opts) as ydl:
            audio_url = ydl.extract_info(url, download=False)['formats'][0]['url']
            self.client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print('done', e))


    @commands.command()
    async def effect(self, ctx, effect_name):
        """Plays a sound effect from a list of effects."""

        if self.client is None:
            await ctx.channel.send('I have to have joined a channel to play !music.')
            return

        if not effect_name:
            await ctx.channel.send('You need to tell me what !effect to play.')
            return

        all_effects = { 
            effect.split('.')[0]: path.join('effects', effect) for effect in listdir('./effects')
        }

        if effect_name in all_effects:
            self.client.play(
                discord.FFmpegPCMAudio(all_effects[effect_name]),
                after=lambda e: print('Finished playing.', e)
            )

        else:
            await ctx.channel.send(f"{effect_name} is not a valid sound effect.")