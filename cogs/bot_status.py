"""Shows console messages for the bot's status."""

from disnake.ext import commands
import json


class BotStatus(commands.Cog):
    """Displays the status of the bot when connecting, connected and disconnected"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print('Logging in...')

    @commands.Cog.listener()
    async def on_ready(self):
        # Log all the invites in the server
        with open('whitelist.json', 'r') as f:
            self.bot.whitelist = json.load(f)["whitelist"]
        invites = {}
        for guild in self.bot.guilds:
            for invite in await guild.invites():
                invites[invite.code] = invite.uses
        self.bot.invite_uses = invites

        # Print the bot's status
        print('------------------------')
        print('Logged in as: ' + self.bot.user.name)
        print('')
        print(f'Ready')

    @commands.Cog.listener()
    async def on_disconnect(self):
        print(f'Disconnected')
        print('Attempting reconnection......')

    @commands.Cog.listener()
    async def on_resumed(self):
        print('Connection has been restored')
        print(f'Ready')


def setup(bot):
    bot.add_cog(BotStatus(bot))
    print("Bot Status loaded")
