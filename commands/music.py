from urllib.parse import urlparse
import discord
import youtube_dl


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

async def _join(message, tokens, _voice_client=None):
    voice = message.author.voice
    if voice:
        if _voice_client is None:
            _voice_client = await voice.channel.connect()
        elif _voice_client.channel != voice.channel:
            await _voice_client.move_to(voice.channel)
    return _voice_client


async def _search(keywords):
    return 'https://www.youtube.com/watch?v=qF4RCOcz9ow'


async def _music(message, tokens):
    # await message.channel.send('This fall... Experience more than ever before.')
    client = await _join(message, tokens)
    
    if client is None:
        await message.channel.send('You have to be in a voice channel to play !music.')
        return

    url = tokens[0] if urlparse(tokens[0]).netloc != '' else await search(tokens)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        audio_url = ydl.extract_info(url, download=False)['formats'][0]['url']
        client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print('done', e))

music_doc = (
    'music', {
        'desc': 'Commands and subcommands for playing music',
        'callback': _music,
    }
)

