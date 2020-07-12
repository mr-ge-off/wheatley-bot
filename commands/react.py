from emoji import emojize

# TODO: add positional param for message to react to?
async def _react(message, tokens):
    messages = await message.channel.history(limit=2).flatten()
    past_message = messages[1]
    if len(tokens) == 1:
        chars = list(dict.fromkeys(tokens[0].lower()))
        for char in chars:
            emoj = emojize(f':regional_indicator_{char}:', use_aliases=True)
            await past_message.add_reaction(emoj)
    else:
        for token in tokens:
            emoj = emojize(f':{token.lower()}:', use_aliases=True)
            if emoj.startswith(':'): continue
            await past_message.add_reaction(emoj)


react_doc = (
    'react', {
        'desc': 'Add text or emoji as reactions',
        'callback': _react,
    }
)