from importlib import import_module
from os import environ, listdir, path, remove
from urllib.parse import urlparse
from discord.ext import commands
import discord
import youtube_dl


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Voice(bot))


def _cleanup(filename, exception):
    if exception:
        print(f"Encountered exception: {exception}")

    print(f"Removing {filename}...")
    remove(filename)
    print("Done!")


class Voice(commands.Cog):
    ENRICHMENT_CENTER_ID = 734468488105558026

    YDL_OPTS = {
        'format': 'bestaudio/best',
        'default_search': 'auto',
        'outtmpl': './queue/%(title).%(ext)'
    }

    FFMPEG_OPTS = {
        'options': '-vn',
    }

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.client = None
        self.queue = []

        # try:
        #     self.token = import_module('secrets').youtube_key
        # except NameError:
        #     self.token = environ['YOUTUBE_TOKEN']
        #
        # # pafy.set_api_key(self.token)

    ###########################################################################
    # COMMANDS                                                                #
    ###########################################################################
    @commands.command()
    async def join(self, ctx):
        """Joins the voice channel you're in, or the Enrichment Center otherwise."""

        voice = ctx.author.voice
        if voice:
            if self.client is None:
                self.client = await voice.channel.connect()
            elif self.client.channel != voice.channel:
                await self.client.move_to(voice.channel)
        else:
            self.client = await self.bot.get_channel(self.ENRICHMENT_CENTER_ID).connect()

    @commands.command()
    async def leave(self, ctx):
        """Leaves the voice channel I'm in."""

        if self.client:
            await self.client.disconnect()
            self.client = None

    @commands.command()
    async def music(self, ctx, *link):
        """Plays the linked YouTube video."""

        # allow for search terms using ydl's search
        ydl_inp = link[0] if len(link) == 1 else ' '.join(link)

        if self.client is None:
            await ctx.channel.send('I have to have joined a channel to play `!music`.')
            return

        with youtube_dl.YoutubeDL(Voice.YDL_OPTS) as ydl:
            audio_data = ydl.extract_info(ydl_inp, download=True)
            audio_url = ydl.prepare_filename(audio_data)

            # TODO: playlists
            self.client.play(
                discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_url, **Voice.FFMPEG_OPTS), volume=0.5),
                after=lambda e: _cleanup(audio_url, e)
            )

    @commands.command()
    async def effect(self, ctx, effect_name):
        """Plays a sound effect from a list of effects."""

        if self.client is None:
            await ctx.channel.send('I have to have joined a channel to play `!music`.')
            return

        if not effect_name:
            await ctx.channel.send('You need to tell me what `!effect` to play.')
            return

        all_effects = { 
            effect.split('.')[0]: path.join('effects', effect) for effect in listdir('./effects')
        }

        if effect_name in all_effects:
            self.client.play(
                discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(all_effects[effect_name], **Voice.FFMPEG_OPTS), volume=0.5),
                after=lambda e: print('Finished playing.', e)
            )

        else:
            await ctx.channel.send(f"{effect_name} is not a valid sound effect.")

    ###########################################################################
    # PRIVATE helper methods                                                  #
    ###########################################################################

    # async def _play(self, link):
    #     # url = link if urlparse(link).netloc != '' else await search(args)
    #
    #     yt_data = None # pafy.new(link)
    #     audio = yt_data.getbestaudio()
    #     filepath = "./queue/song" + '.' + audio.extension
    #     audio.download(filepath=filepath)
    #     print(filepath)
    #
    #     self.client.play(
    #         discord.FFmpegPCMAudio(filepath),
    #         after=lambda e: _cleanup(filepath, e)
    #     )
