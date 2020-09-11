from os import listdir
from discord.ext import commands
import discord


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.lockId = None


    async def bot_check(self, ctx):
        if self.lockId is not None:
            if ctx.author.id != self.lockId:
                await ctx.send(f"I'm currently locked by @{self.bot.get_user(self.lockId).name}")
                return False

        return True


    @commands.command()
    async def lock(self, ctx):
        """Locks me to only receive commands from one user."""

        await ctx.send(f"I've been locked by @{ctx.author.name}.")
        self.lockId = ctx.author.id


    @commands.command()
    async def unlock(self, ctx):
        """Allows me to receive commands from anyone."""

        await ctx.send("I'm now unlocked.")
        self.lockId = None