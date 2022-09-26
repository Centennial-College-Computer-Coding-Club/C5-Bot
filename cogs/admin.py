"""Admin commands for the bot."""

from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from enum import Enum


class Cogs(str, Enum):
    """Enum of cogs."""
    ADMIN = "cogs.admin"
    BOT_STATUS = "cogs.bot_status"


class Admin(commands.Cog):
    """Admin commands for the bot."""
    def __init__(self, bot):
        self.bot = bot

    async def cog_slash_command_check(self, inter: ApplicationCommandInteraction) -> bool:
        """Only allow bot devs to use these commands."""
        if 1017508104881066084 in [role.id for role in inter.author.roles]:
            return True
        await inter.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return False

    @commands.slash_command(name="ping", description="Check the latency of the bot.")
    async def ping(self, inter: ApplicationCommandInteraction):
        """Pings the bot returning response delay."""
        await inter.response.send_message(f"{self.bot.user.name} responded in {round(self.bot.latency * 1000)}ms", ephemeral=True)

    @commands.slash_command(name="load", description="Loads a cog.")
    async def load(self, inter: ApplicationCommandInteraction, cog: Cogs):
        """Loads a cog."""
        try:
            self.bot.load_extension(cog)
            await inter.response.send_message(f"Loaded {cog}", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error loading {cog}: {e}", ephemeral=True)

    @commands.slash_command(name="unload", description="Unloads a cog.")
    async def unload(self, inter: ApplicationCommandInteraction, cog: Cogs):
        """Unloads a cog."""
        if cog != "cogs.admin":
            try:
                self.bot.unload_extension(cog)
                await inter.response.send_message(f"Unloaded {cog}", ephemeral=True)
            except Exception as e:
                await inter.response.send_message(f"Error unloading {cog}: {e}", ephemeral=True)

    @commands.slash_command(name="reload", description="Reloads a cog.")
    async def reload(self, inter: ApplicationCommandInteraction, cog: Cogs):
        """Reloads a cog."""
        if cog != "cogs.admin":
            try:
                self.bot.reload_extension(cog)
                await inter.response.send_message(f"Reloaded {cog}", ephemeral=True)
            except Exception as e:
                await inter.response.send_message(f"Error reloading {cog}: {e}", ephemeral=True)

    @commands.slash_command(name="shutdown", description="Shuts down the bot.")
    async def shutdown(self, inter: ApplicationCommandInteraction):
        """Shuts down the bot."""
        await inter.response.send_message("Shutting down...", ephemeral=True)
        await self.bot.close()


def setup(bot):
    bot.add_cog(Admin(bot))
    print("Admin cog loaded")
