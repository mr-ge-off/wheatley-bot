from asyncio import get_event_loop, run_coroutine_threadsafe
from os import listdir, path, remove

from effects.effects_dict import effects_dict

from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.ext.commands.context import Context

import youtube_dl


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Voice(bot))


def _cleanup(filename):
    print(f"Removing {filename}...")
    remove(filename)
    print("Done!")


async def check_is_playing_invert(ctx: Context):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send("I'm already `!play`ing something! Try a `!stop` first.")
        return False
    return True


async def check_is_playing(ctx: Context):
    if ctx.voice_client and ctx.voice_client.is_playing():
        return True
    await ctx.send('I have to be playing something to do that :T')
    return False


async def check_is_in_voice(ctx: Context, warn = True):
    if not ctx.voice_client:
        if warn:
            await ctx.send('I need to be in a voice channel to do that!')
        return False
    return True


class Voice(commands.Cog):
    ENRICHMENT_CENTER_ID = 734468488105558026

    YDL_OPTS = {
        'format': 'bestaudio/best',
        'default_search': 'auto',
        'restrictfilenames': True,
        'outtmpl': path.join('queue', '%(title)s.%(ext)s'),
        'noplaylist': True,
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

    def _extract_info(self, ydl_data, source, stream, url):
        return {
            'channel': ydl_data['channel'],
            'name': ydl_data['title'],
            'ordinal': len(self.queue) + 1,
            'source': source,
            'stream': stream,
            'url': url,
        }

    async def _download(self, link, stream=True):

        # allow for search terms using ydl's search
        ydl_inp = link[0] if len(link) == 1 else ' '.join(link)

        with youtube_dl.YoutubeDL(Voice.YDL_OPTS) as ydl:
            loop = get_event_loop()
            audio_data = await loop.run_in_executor(None, lambda: ydl.extract_info(ydl_inp, download=not stream))
            audio_location = audio_data['url'] if stream else ydl.prepare_filename(audio_data)

            return self._extract_info(audio_data, audio_location, stream, None)

    def _queue_after_callback(self, exception, ctx: Context, stream=False, skip=False):
        if exception:
            print('Exception occurred: ', exception)

        # clean up file if necessary
        if not stream:
            _cleanup(self.queue[0]['source'])

        # decrement queue
        self.queue.pop(0)
        for item in self.queue[:]:
            item['ordinal'] = item['ordinal'] - 1

        # if we're on the last item, exit the voice channel
        if len(self.queue) == 0:
            coro = ctx.voice_client.disconnect()
            future = run_coroutine_threadsafe(coro, self.bot.loop)
            future.result()

        # else, create the next audio source and pass it to the player
        elif len(self.queue) > 0:
            if skip:
                ctx.voice_client.source = PCMVolumeTransformer(
                    FFmpegPCMAudio(self.queue[0]['source'], **Voice.FFMPEG_OPTS),
                    volume=0.5
                )
            else:
                ctx.voice_client.play(
                    PCMVolumeTransformer(FFmpegPCMAudio(self.queue[0]['source'], **Voice.FFMPEG_OPTS), volume=0.5),
                    after=lambda e: self._queue_after_callback(e, ctx, self.queue[0]['stream'])
                )

    ###########################################################################
    # COMMANDS                                                                #
    ###########################################################################
    @commands.command()
    async def join(self, ctx: Context):
        """-> Joins a voice channel.

         I'll try to join the channel you're in, or the Enrichment Center otherwise."""

        voice = ctx.author.voice
        if voice:
            if ctx.voice_client is None:
                await voice.channel.connect()
            elif ctx.voice_client.channel != voice.channel:
                await ctx.voice_client.move_to(voice.channel)
        else:
            await self.bot.get_channel(self.ENRICHMENT_CENTER_ID).connect()

    @commands.command()
    async def leave(self, ctx: Context):
        """-> Leaves the voice channel I'm in."""

        if not await check_is_in_voice(ctx):
            return

        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()  # TODO: playlists, enqueuing
    async def play(self, ctx: Context, *link, stream: bool = True):
        """-> Plays the linked YouTube video."""

        if not await check_is_playing_invert(ctx):
            return

        data_dict = await self._download(link, stream)

        ctx.voice_client.play(
            PCMVolumeTransformer(FFmpegPCMAudio(data_dict['source'], **Voice.FFMPEG_OPTS), volume=0.5),
            after=lambda e: self._queue_after_callback(e, ctx, stream)
        )

    @commands.command()
    async def effect(self, ctx: Context, effect_name):
        """-> Plays a sound effect from a list of effects."""

        if not await check_is_playing_invert(ctx):
            return

        def after_func(context: Context, e):
            if e:
                print('Exception occurred: ', e)
            print('Finished playing effect')
            coro = context.voice_client.disconnect()
            future = run_coroutine_threadsafe(coro, self.bot.loop)

            future.result()

        if ctx.voice_client is None:
            await self.join(ctx)

        if not effect_name:
            await ctx.send('You need to tell me what `!effect` to play.')
            return

        all_effects = {
            effect.split('.')[0]: path.join('effects', effect) for effect in listdir('./effects')
        }

        print('\n'.join([key + ': ' + value for key, value in all_effects.items()]))

        if effect_name in all_effects:
            ctx.voice_client.play(
                PCMVolumeTransformer(FFmpegPCMAudio(all_effects[effect_name]), volume=0.5),
                after=lambda e: after_func(ctx, e)
            )

        else:
            await ctx.channel.send(f"{effect_name} is not a valid sound effect.")

    @commands.command()
    async def stop(self, ctx: Context):
        """-> Stops the currently playing song."""

        if ctx.voice_client:
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx: Context):
        """-> Pauses the currently playing song."""

        if ctx.voice_client:
            ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx: Context):
        """-> Resumes playing the current song."""

        if ctx.voice_client:
            ctx.voice_client.resume()

    ###########################################################################
    # VOLUME COMMANDS                                                         #
    ###########################################################################
    @commands.group()
    async def volume(self, ctx: Context):
        """-> Commands for manipulating volume.

        If no valid subcommand is given, acts as an alias
        for !volume current."""

        if ctx.subcommand_passed and ctx.invoked_subcommand is None:
            await ctx.send("Hey, that's not a `!volume` command!")
        elif not ctx.subcommand_passed:
            await self.current(ctx)

    @volume.command()
    async def current(self, ctx: Context):
        """-> Tells the current volume."""

        if not await check_is_playing(ctx):
            return
        await ctx.send(f'The volume is currently at {ctx.voice_client.source.volume * 100}%.')

    @volume.command()  # TODO: me
    async def up(self, ctx: Context):
        """-> Sets the volume up 10%, or whatever you tell me.

        The volume change must be given as a percent,
        and cannot exceed 100%."""

        if not await check_is_playing(ctx):
            return
        pass

    @volume.command()  # TODO: me
    async def down(self, ctx: Context):
        """-> Sets the volume down 10%, or whatever you tell me.

        The volume change must be given as a percent,
        and cannot exceed 100%."""

        if not await check_is_playing(ctx):
            return
        pass

    @volume.command()
    async def max(self, ctx: Context):
        """-> Maxes out the volume."""

        if not await check_is_playing(ctx):
            return
        ctx.voice_client.source.volume = 1.0

    @volume.command()
    async def mute(self, ctx: Context):
        """-> Mutes the volume."""

        if not await check_is_playing(ctx):
            return

        ctx.voice_client.source.volume = 0.0

    ###########################################################################
    # QUEUE COMMANDS                                                          #
    ###########################################################################
    @commands.group()  # TODO: adding
    async def queue(self, ctx: Context):
        """-> Commands for manipulating the music queue.

        If no valid subcommand is given, acts as an alias
        for !queue add [args...]"""

        if ctx.invoked_subcommand is None:
            await ctx.send("Hey, that's not a `!queue` command!")

    @queue.command()
    async def add(self, ctx: Context, *item, stream: bool = True):
        """-> Adds an item to the music queue.

        I'll try and stream it first, though streaming
        runs the risk of being unstable. If you pass me
        stream=False, I'll actually download the song."""

        self.queue.append(await self._download(item, stream))
        await ctx.send(f"Added `{self.queue[-1]['name']}` to the queue.")

    @queue.command()
    async def remove(self, ctx: Context, item: int = 1):
        """-> Removes an item from the music queue."""

        removed = self.queue.pop(item - 1)
        for item in self.queue[item - 1:]:
            item['ordinal'] = item['ordinal'] - 1
        await ctx.send(f"Removed `{removed['name']}` from the queue.")

    @queue.command()
    async def clear(self, ctx: Context):
        """-> Empties the queue in its entirety."""

        self.queue.clear()
        await ctx.send('Cleared out the queue! No music for you.')

    @queue.command()
    async def empty(self, ctx: Context):
        """-> Alias for !clear."""

        await self.clear(ctx)

    @queue.command()
    async def start(self, ctx: Context):
        """-> Start playing the queue."""

        if not await check_is_in_voice(ctx, warn=False):
            await self.join(ctx)

        if len(self.queue) > 0:
            ctx.voice_client.play(
                PCMVolumeTransformer(FFmpegPCMAudio(self.queue[0]['source'], **Voice.FFMPEG_OPTS), volume=0.5),
                after=lambda e: self._queue_after_callback(e, ctx, self.queue[0]['stream'])
            )
        else:
            ctx.voice_client.play(
                PCMVolumeTransformer(FFmpegPCMAudio('./tts/no_queue_wheatley.wav'), volume=0.5),
                after=lambda e: (run_coroutine_threadsafe(ctx.voice_client.disconnect(), self.bot.loop).result()
                                 and (e and print(e)))
            )

    @queue.command()
    async def skip(self, ctx: Context):
        """-> Skip to the next song in the queue."""

        if not await check_is_playing(ctx):
            return

        stream = self.queue[0]['stream']
        self._queue_after_callback(None, ctx, stream, True)

    ###########################################################################
    # LIST COMMANDS                                                           #
    ###########################################################################
    @commands.group(aliases=['show'])
    async def list(self, ctx: Context):
        """-> Lists something. Options are 'queue' and 'effects'."""
        if ctx.invoked_subcommand is None:
            await ctx.send('Send me something valid to list!')

    @list.command(name='effects')
    async def eff_list(self, ctx: Context):
        """-> Shows all the sound effects I know."""

        transform = f'\n'.join([key + ' ' + effects_dict[key] for key in sorted(effects_dict.keys())])
        await ctx.send(f'```Name                -> Description\n{transform}```')

    @list.command(name='queue')
    async def queue_list(self, ctx: Context):
        """-> Show what's in the queue."""

        if len(self.queue) == 0:
            await ctx.send('Nothing is currently queued.')
            return

        transforms = '\n'.join([f"[{item['ordinal']}]: {item['name']} -- {item['channel']}" for item in self.queue])
        await ctx.send(f'Currently Queued:\n```{transforms}```')
