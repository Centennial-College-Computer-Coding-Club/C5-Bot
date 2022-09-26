from abc import ABC, abstractmethod
from utils.singleton import Singleton
from disnake.ext import commands
import disnake


class Interactive(ABC):
    @abstractmethod
    def __init__(self, message_id: int = None):
        self.message_id = message_id

    @abstractmethod
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        pass

    @staticmethod
    @abstractmethod
    def from_data(data):
        pass


class Interactions(Singleton):
    def __init__(self):
        self.interactions = {}

    def add(self, interaction: Interactive):
        self.interactions[interaction.message_id] = interaction

    def remove(self, message_id):
        self.interactions.pop(message_id)

    def get(self, message_id):
        return self.interactions.get(message_id)

    def get_all(self):
        return self.interactions.values()


class InteractionController(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.interactions = Interactions()

    async def load_all_interactions(self):
        for interaction in self.interactions.get_all():
            channel = self.bot.get_channel(interaction.message_id)
            view = channel.fetch_message(interaction.message_id)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        instance = self.interactions.get(interaction.message.id)
        if instance is None:
            return
        await instance.on_button_click(interaction)


def setup(bot: commands.Bot):
    bot.add_cog(InteractionController(bot))
    print("Interaction Controller loaded")