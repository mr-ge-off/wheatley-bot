import io

import discord
from discord.ext import commands
from discord.ext.commands.context import Context


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Silly(bot))


class Silly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slap(self, ctx: Context, slappee: discord.User):
        """-> Slaps the selected user."""

        slapper_pic_bytes = await ctx.author.avatar_url_as(format='png', size=256).read()
        slappee_pic_bytes = await slappee.avatar_url_as(format='png', size=256).read()

        await ctx.send(f'{ctx.author.mention} slapped {slappee.mention}!')
        await ctx.send(files=[
            discord.File(io.BytesIO(slapper_pic_bytes), filename='slapper.png'),
            discord.File('./images/slap.jpg'),
            discord.File(io.BytesIO(slappee_pic_bytes), filename='slappee.png'),
        ])
