"""Tracks who used what invites."""

from disnake.ext import commands


class InviteTracking(commands.Cog):
    """Tracks invites"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        """Adds a new invite to the invite_uses dictionary."""
        self.bot.invite_uses[invite.code] = 0

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        """Removes an invite from the invite_uses dictionary."""
        self.bot.invite_uses.pop(invite.code)


def setup(bot):
    bot.add_cog(InviteTracking(bot))
    print("Invite Tracking cog loaded")