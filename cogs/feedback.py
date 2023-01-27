'''Anonymous Feedback System'''

from disnake.ext import commands
from disnake import Embed
from disnake.utils import get


class Feedback(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="feedback", description="Send anonymous feedback/suggestions to the community leaders.")
    async def feedback(self, inter, *, feedback: str):
        """Send anonymous feedback/suggestions to the community leaders."""
        await inter.response.send_message("Thank you for your feedback! We will review it as soon as possible.", ephemeral=True)
        embed = Embed(title="New anonymous feedback received:", color=0x00ff00)
        embed.add_field(name="\u200b", value=feedback, inline=False)
        await self.bot.get_channel(1019046753099583508).send(embed=embed, content=f"{get(inter.guild.roles, id=1019047886077562913).mention}")


def setup(bot):
    bot.add_cog(Feedback(bot))
    print('Feedback is loaded')
