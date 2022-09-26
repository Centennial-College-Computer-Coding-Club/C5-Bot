"""Handles any errors that occur in the bot."""

from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from disnake.errors import InteractionResponded
import traceback


class ErrorHandling(commands.Cog):
    """Handles errors"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: ApplicationCommandInteraction, error: Exception):
        """Handle errors."""
        if error.__class__.__name__ == "CheckFailure":
            return
        else:
            try:
                await inter.response.send_message(f"Error: {error}", ephemeral=True)
            except InteractionResponded:
                await inter.followup.send(f"Error: {error}", ephemeral=True)
            traceback.print_exc()


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
    print("Error Handling cog loaded")
