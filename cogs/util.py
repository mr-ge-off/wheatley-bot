async def debug_print(iterable):
    [print(x) for x in iterable]

async def tokenize(content):
    if content.startswith('!'):
        tokens = content.strip('!').split(' ')
        return (tokens[0], tokens[1:])
    return (None, None)