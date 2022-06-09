from emoji import emojize
from discord.ext import commands

DIGIT_MAP = {
    '1': ':one:',
    '2': ':two:',
    '3': ':three:',
    '4': ':four:',
    '5': ':five:',
    '6': ':six:',
    '7': ':seven:',
    '8': ':eight:',
    '9': ':nine:',
    '0': ':zero:',
}


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Text(bot))


def _get_codepoint(single_letter: str):
    unicode_indicator_seed = 0x0001F1E6

    if len(single_letter) > 1:
        single_letter = single_letter[0]

    if single_letter in DIGIT_MAP.keys():
        return emojize(DIGIT_MAP[single_letter], language='alias')
    else:
        return chr(unicode_indicator_seed + (ord(single_letter) - 97))


class Text(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def react(self, ctx, *words):
        """Adds reactions to the last post.

        Will add as many letters of a single word as I can,
        or will attempt to add each named emoji if more than
        one word is passed."""

        messages = await ctx.message.channel.history(limit=2).flatten()
        past_message = messages[1]
        if len(words) == 1:
            chars = list(dict.fromkeys(words[0].lower()))
            for char in chars:
                emoj = _get_codepoint(char)
                await past_message.add_reaction(emoj)
        else:
            for token in words:
                emoj = emojize(f':{token.lower()}:', language='alias')
                if emoj.startswith(':'):
                    continue
                await past_message.add_reaction(emoj)

    @commands.command()
    async def gik(self, ctx):
        """Gak!"""

        await ctx.send('gak!')

    @commands.command()
    async def gak(self, ctx):
        """Gik!"""

        await ctx.send('gik!')
