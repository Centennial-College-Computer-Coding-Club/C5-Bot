"""Greet new users when they join the server."""

from disnake.ext import commands
from disnake import Member, Embed, Color


class Greeting(commands.Cog):
    """Greets new users"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """Sends a welcome message to the new user."""

        # Check which invite was used
        invite_used = None
        for invite in await member.guild.invites():
            if invite.uses > self.bot.invite_uses[invite.code]:
                invite_used = invite

        # Update the invite_uses dictionary
        self.bot.invite_uses[invite_used.code] = invite_used.uses

        # Log the invite used and the member who used it to channel 1020312901665423411
        embed = Embed(
            title="New Member",
            description=f"{member.mention} joined using invite {invite_used.code}",
            color=Color.green()
        )
        await self.bot.get_channel(1020312901665423411).send(embed=embed)

        # Greet the new user
        embed = Embed(
            title=f"Welcome to {member.guild.name}, {member.name}! :wave:",
            description=f"This server is a community hub for software engineering related courses at Centennial "
                        f"College. Please read the rules in {member.guild.rules_channel.mention} and enjoy your stay!"
                        f"\n\nPlease use the bot command `/program` to select your enrolled school program and add all "
                        f"of your courses using `/add_courses` to gain access to the rest of the server.",
            color=Color.green()
        )
        channel = member.guild.system_channel
        await channel.send(content=member.mention, embed=embed)


def setup(bot):
    bot.add_cog(Greeting(bot))
    print("Greeting cog loaded")
