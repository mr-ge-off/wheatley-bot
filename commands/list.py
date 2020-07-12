from .react import react_doc
from .poll import poll_doc
from .music import music_doc
from .help import help_doc

async def _list(message, tokens):
    await message.channel.send(
        "Here's everything I know how to do:\n" +
        '```' +
        '\n'.join([f'!{item}: {value["desc"]}' for item, value in all_commands.items()]) +
        '```'
    )

_list_doc = (
    'list', {
        'desc': ' Lists all commands',
        'callback': _list,
    },
)

_docs = [
    _list_doc,
    react_doc,
    poll_doc,
    music_doc,
    help_doc,
]

all_commands = { tup1: tup2 for tup1,tup2 in _docs }

