
async def _music(message, tokens):
    await message.channel.send('This fall... Experience more than ever before.')
    # TODO: implement this!

music_doc = (
    'music', {
        'desc': 'Commands and subcommands for playing music',
        'callback': _music,
    }
)
