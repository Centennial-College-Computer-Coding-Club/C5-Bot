"""Cog to add polling functionality to the bot."""

from __future__ import annotations
from disnake.ext import commands
from disnake import ButtonStyle, ApplicationCommandInteraction, Embed, MessageInteraction, Color
from disnake.ui import View, ActionRow, Button, Item
from dataclasses import dataclass
from cogs.interaction_controller import Interactions, Interactive
from database import db
import json


@dataclass
class PollOption:
    name: str
    button: Button = None

    def __post_init__(self):
        self.button = Button(
            label=self.name,
            style=ButtonStyle.primary,
            custom_id=self.name
        )


class PollView(View):
    def __init__(self, poll: Poll):
        super().__init__(timeout=None)
        self.poll = poll

        for option in self.poll.options:
            self.add_item(option.button)

    async def interaction_check(self, interaction: MessageInteraction):
        if interaction.user.id in self.poll.voted:
            await interaction.response.send_message("You have already voted.", ephemeral=True)
            return False
        await interaction.response.send_message("Thank you for voting!", ephemeral=True)
        return True


class Poll(Interactive):
    def __init__(self, title: str, description: str, options: list[PollOption], message_id: int = None,
                 voted: list[int] = None):
        if voted is None:
            voted = []
        self.title = title
        self.description = description
        self.options = options
        self.message_id = message_id
        self.voted = voted

    async def on_button_click(self, interaction: MessageInteraction):
        if interaction.user.id in self.voted:
            return
        self.voted.append(interaction.user.id)
        raw_poll = db.get_poll(interaction.message.id)
        poll: dict = json.loads(raw_poll[0])
        poll["voted"].append(interaction.user.id)
        poll["options"][interaction.data["custom_id"]] += 1
        db.update_poll(interaction.message.id, poll)

    @staticmethod
    def from_data(data) -> Poll:
        message_id = data[0]
        data_dict = json.loads(data[1])
        title = data_dict["title"]
        description = data_dict["description"]
        options = [PollOption(option) for option in data_dict["options"]]
        return Poll(title, description, options, message_id)


class PollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interactions = Interactions()
        self.load_polls()

    def load_polls(self):
        polls = db.get_polls()
        for data in polls:
            self.interactions.add(Poll.from_data(data))

    @commands.slash_command(name="poll", description="Create a poll.")
    async def poll(self, inter: ApplicationCommandInteraction, title: str, description: str, options: str):
        """Create a poll in the current channel"""
        embed = Embed(title=title, description=description, color=Color.blurple())
        poll = Poll(title, description, [PollOption(name=option) for option in options.split(",")])
        view = PollView(poll)
        await inter.response.send_message("Poll created!", ephemeral=True)
        message = await inter.channel.send(embed=embed, view=view)
        poll.message_id = message.id
        db.add_poll(message.id, poll)
        self.interactions.add(poll)


def setup(bot):
    bot.add_cog(PollCog(bot))
    print("Poll cog loaded")
