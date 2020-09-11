from os import listdir
from emoji import emojize
from discord.ext import commands
import discord


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
                emoj = emojize(f':regional_indicator_{char}:', use_aliases=True)
                await past_message.add_reaction(emoj)
        else:
            for token in words:
                emoj = emojize(f':{token.lower()}:', use_aliases=True)
                if emoj.startswith(':'): continue
                await past_message.add_reaction(emoj)