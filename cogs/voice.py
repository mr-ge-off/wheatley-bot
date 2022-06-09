import asyncio
from os import listdir, path, remove

from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.ext.commands.context import Context
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


async def _is_playing_check(ctx: Context):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send("I'm already `!play`ing something! Try a `!stop` first.")
        return False
    return True


class Voice(commands.Cog):
    ENRICHMENT_CENTER_ID = 734468488105558026

    YDL_OPTS = {
        'format': 'bestaudio/best',
        'default_search': 'auto',
        'restrictfilenames': True,
        'outtmpl': path.join('queue', '%(title)s.%(ext)s')
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'mp3',
        #     'preferredquality': '192'
        # }]
    }

    FFMPEG_OPTS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.queue = []

    def _extract_info(self, ydl_data, source):
        return {
            'source': source,
            'name': ydl_data['title'],
            'channel': ydl_data['channel'],
            'ordinal': len(self.queue) + 1,
        }

    async def _download(self, link, stream=True):

        # allow for search terms using ydl's search
        ydl_inp = link[0] if len(link) == 1 else ' '.join(link)

        with youtube_dl.YoutubeDL(Voice.YDL_OPTS) as ydl:
            loop = asyncio.get_event_loop()
            audio_data = await loop.run_in_executor(None, lambda: ydl.extract_info(ydl_inp, download=not stream))

            return self._extract_info(audio_data, audio_data['url'] if stream else ydl.prepare_filename(audio_data))

    ###########################################################################
    # COMMANDS                                                                #
    ###########################################################################
    @commands.command()
    async def join(self, ctx):
        """-> Joins a voice channel.

         I'll try to join the channel you're in, or the Enrichment Center otherwise."""

        voice = ctx.author.voice
        if voice:
            if ctx.voice_client is None:
                await voice.channel.connect()
            elif ctx.voice_client.channel != voice.channel:
                await ctx.voice_client.move_to(voice.channel)
        else:
            ctx.voice_client = await self.bot.get_channel(self.ENRICHMENT_CENTER_ID).connect()

    @commands.command()
    async def leave(self, ctx):
        """-> Leaves the voice channel I'm in."""

        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    @commands.check(_is_playing_check)
    async def play(self, ctx, *link, stream: bool = True):
        """-> Plays the linked YouTube video."""

        if ctx.voice_client is None:
            await ctx.send('I have to have joined a channel to play `!music`.')
            return

        data_dict = await self._download(link, stream)

        # TODO: playlists
        ctx.voice_client.play(
            PCMVolumeTransformer(FFmpegPCMAudio(data_dict['source'], **Voice.FFMPEG_OPTS), volume=0.5),
            after=lambda e: (len(self.queue) > 0 and self.queue.pop(0)) and (stream or _cleanup(data_dict['source'], e))
        )

    @commands.command()
    @commands.check(_is_playing_check)
    async def effect(self, ctx, effect_name):
        """-> Plays a sound effect from a list of effects."""

        if ctx.voice_client is None:
            await ctx.send('I have to have joined a channel to play `!music`.')
            return

        if not effect_name:
            await ctx.send('You need to tell me what `!effect` to play.')
            return

        all_effects = { 
            effect.split('.')[0]: path.join('effects', effect) for effect in listdir('./effects')
        }

        if effect_name in all_effects:
            ctx.voice_client.play(
                PCMVolumeTransformer(FFmpegPCMAudio(all_effects[effect_name]), volume=0.5),
                after=lambda e: print('Finished playing.', e)
            )

        else:
            await ctx.channel.send(f"{effect_name} is not a valid sound effect.")

    @commands.command()
    async def stop(self, ctx):
        """-> Stops the currently playing song."""

        if ctx.voice_client:
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        """-> Pauses the currently playing song."""

        if ctx.voice_client:
            ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """-> Resumes playing the current song."""

        if ctx.voice_client:
            ctx.voice_client.resume()

    ###########################################################################
    # QUEUE COMMANDS                                                          #
    ###########################################################################
    @commands.group()
    async def queue(self, ctx):
        """-> Commands for manipulating the music queue"""

        if ctx.invoked_subcommand is None:
            await ctx.send("Hey, that's not a `!queue` command!")

    @queue.command()
    async def add(self, ctx, *item, stream=True):
        """-> Adds an item to the music queue."""

        self.queue.append(await self._download(item, stream))
        await ctx.send(f"Added `{self.queue[-1]['name']}` to the queue.")

    @queue.command()
    async def remove(self, ctx, item: int = None):
        """-> Removes an item from the music queue."""

        removed = self.queue.pop(item - 1) if item else self.queue.pop(0)
        for item in self.queue:
            item['ordinal'] = item['ordinal'] - 1
        await ctx.send(f"Removed `{removed['name']}` from the queue.")

    @queue.command()
    async def show(self, ctx):
        """-> Show what's in the queue."""

        if len(self.queue) == 0:
            await ctx.send('Nothing is currently queued.')
            return

        transforms = '\n'.join([f"[{item['ordinal']}]: {item['name']} -- {item['channel']}" for item in self.queue])
        await ctx.send(f'Currently Queued:\n```{transforms}```')

    @queue.command()
    async def list(self, ctx):
        """-> Alias for !show."""

        await self.show(ctx)

    @queue.command()
    @commands.check(_is_playing_check)
    async def start(self, ctx):
        """-> Start playing the queue."""
        pass

    @queue.command()
    async def skip(self, ctx):
        """-> Skip to the next song in the queue."""
        pass

