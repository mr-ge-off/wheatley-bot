from os import listdir
from discord.ext import commands
import discord


# Extension method to hot-load this cog
def setup(bot):
    bot.add_cog(Admin(bot))


class Admin(commands.Cog):
    admin_id = 497958142919966731

    def __init__(self, bot):
        self.bot = bot
        self.lockId = None

    async def cog_check(self, ctx):

        # check that the right prefix is used and the user is an admin
        if ctx.prefix == '$' and isinstance(ctx.author, discord.Member):
            return Admin.admin_id in [role.id for role in ctx.author.roles]

        return False

    # check the lock status
    async def bot_check(self, ctx):
        if ((self.lockId and
            ctx.author.id == self.lockId) or 
            (Admin.admin_id in [role.id for role in ctx.author.roles] and
            ctx.command.name == 'unlock') or
                not self.lockId):
            return True

        await ctx.send(f"I'm currently locked to {self.bot.get_user(self.lockId).mention}")
        return False

    @commands.command()
    async def lock(self, ctx, user: discord.User=None):
        """Locks me to only receive commands from one user."""

        locker = user if user else ctx.author
        await ctx.send(f"I've been locked to {locker.mention}.")
        self.lockId = locker.id

    @commands.command()
    async def unlock(self, ctx):
        """Allows me to receive commands from anyone."""

        await ctx.send("I'm now unlocked.")
        self.lockId = None

    @commands.command()
    async def reloadcog(self, ctx, cogname):
        """Hotloads a cog (for dev only)"""
        
        if cogname in [cog.lower() for cog in self.bot.cogs]:
            self.bot.reload_extension(f'cogs.{cogname}')
            print(f'reloaded cogs.{cogname}')
        else:
            await ctx.send(f'`{cogname}` is not a valid cog.')
