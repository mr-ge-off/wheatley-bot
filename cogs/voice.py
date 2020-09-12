from importlib import import_module
from os import environ, listdir, path
from urllib.parse import urlparse
from discord.ext import commands
import discord
import pafy


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Voice(bot))


class Voice(commands.Cog):
    enrichment_center_id = 734468488105558026

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

        try:
            self.token = import_module('secrets').youtube_key
        except NameError:
            self.token = environ['YOUTUBE_TOKEN']

        pafy.set_api_key(self.token)


    ###########################################################################
    # COMMANDS                                                                #
    ###########################################################################
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

        await self._play(link)


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


    ###########################################################################
    # PRIVATE helper methods                                                  #
    ###########################################################################
    def _cleanup(filename, exception):
        if exception:
            print(f"Encountered exception: {exception}")

        print(f"Removing {filename}...")
        os.remove(filename)
        print("Done!")


    async def _play(self, link):
        url = link if urlparse(link).netloc != '' else await search(args)

        yt_data = pafy.new(url)
        audio = yt_data.getbestaudio()
        print(audio)
        filepath=path.join('.', 'music', audio.title)
        print(filepath)
        filename = audio.download()
        print(filename)

        self.client.play(
            discord.FFmpegPCMAudio(filename),
            after=lambda e: Voice._cleanup(filename, e)
        )
