from discord.ext import commands
import discord


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Poll(bot))


class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot