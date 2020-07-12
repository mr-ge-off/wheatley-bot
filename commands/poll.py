
async def _poll(message, tokens):
    await message.channel.send('Coming soon to theaters!')
    # TODO: implement this!

poll_doc = (
    'poll', {
        'desc': ' Commands and subcommands for making polls',
        'callback': _poll,
    }
)