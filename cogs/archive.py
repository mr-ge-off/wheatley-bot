import discord
from discord.ext import commands
from discord.ext.commands.context import Context


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Archive(bot))


class Archive(commands.Cog):
    ARCHIVE_ID = 986375182455304222

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def archive(self, ctx: Context, *keywords: str):

        print(ctx.message.reference)
        print((await ctx.channel.fetch_message(ctx.message.reference.message_id)).content)
        print(keywords)

