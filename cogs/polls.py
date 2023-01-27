'''Polling system for the community server.'''

from disnake.ext import commands
from disnake import Embed, File
from disnake.utils import get
from database import db
from enum import Enum
import os
from dataclasses import dataclass, field
import json
import matplotlib.pyplot as plt


STYLES = [
    ["✅", "❌"],
    ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"],
    ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"],
    ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🐣"],
    ["🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🍑", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥒", "🌶"],
    ["💻", "📱", "⌨", "🖥", "🖨", "🖱", "🖲", "💽", "💾", "💿", "📀", "📼", "📷", "📹", "📺", "📻", "🎙", "🎚", "🎛", "⏱"],
]



class Style(Enum):
    """The style of the poll."""
    YES_NO = 0
    NUMBERS = 1
    LETTERS = 2
    ANIMALS = 3
    FOODS = 4
    TECH = 5


@dataclass(slots=True)
class Poll:
    """A poll"""
    title: str
    question: str
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.options, str):
            self.options = json.loads(self.options)


class PollCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="poll_open", description="Creates a poll for the polls channel.")
    async def poll_open(self, inter, title: str, question: str, style: Style, options: str):
        """Creates a reaction poll for the polls channel."""
        options = [option.strip() for option in options.split(",")]
        emojis = STYLES[style][:len(options)]
        poll_channel = get(self.bot.guilds[0].channels, name="polls")

        if len(options) > 20:
            return await inter.response.send_message("You can only have up to 20 options.", ephemeral=True)

        if len(options) > (emoji_len := len(emojis)):
            return await inter.response.send_message(f"You can only have up to {emoji_len} options with this style",
                                                     ephemeral=True)

        embed = Embed(title=title, description=question, color=0x00ff00)
        for emoji, option in zip(emojis, options):
            embed.add_field(name="\u200b", value=f"{emoji} - {option}", inline=False)
        message = await poll_channel.send(embed=embed)
        for emoji in emojis[:len(options)]:
            await message.add_reaction(emoji)

        poll = Poll(title, question, {emoji: {"option": option, "voters": []} for emoji, option in zip(emojis, options)})
        db.add_poll(message.id, poll)
        await inter.response.send_message("Poll created!", ephemeral=True)

    @commands.slash_command(name="poll_close", description="Closes a poll.")
    async def poll_close(self, inter, message_id: str):
        """Closes a poll."""
        message_id = int(message_id)
        poll_channel = get(self.bot.guilds[0].channels, name="polls")
        poll_data = db.get_poll(message_id)

        if not poll_data:
            return await inter.response.send_message("This poll doesn't exist.", ephemeral=True)

        message = await poll_channel.fetch_message(message_id)
        if not message:
            return await inter.response.send_message("This poll doesn't exist.", ephemeral=True)

        await self.poll_results(inter, message_id)

        db.remove_poll(message_id)

        await inter.response.send_message("Poll closed!", ephemeral=True)

    @commands.slash_command(name="poll_results", description="Shows the results of a poll.")
    async def poll_results(self, inter, message_id: int):
        poll_channel = inter.channel  # get(self.bot.guilds[0].channels, name="polls")
        poll_data = db.get_poll(message_id)

        if not poll_data:
            return await inter.response.send_message("This poll doesn't exist.", ephemeral=True)

        poll = Poll(**json.loads(poll_data[0]))

        message = await poll_channel.fetch_message(message_id)
        if not message:
            return await inter.response.send_message("This poll doesn't exist.", ephemeral=True)

        embed = message.embeds[0]
        await message.edit(embed=embed)

        options = {option["option"]: len(option["voters"]) for option in poll.options.values() if option["voters"]}
        options = sorted(options.items(), key=lambda x: x[1], reverse=True)

        fig, ax = plt.subplots()
        ax.pie([option[1] for option in options], labels=[option[0] for option in options], autopct="%1.1f%%")
        ax.axis("equal")
        # label the pie chart
        plt.title(poll.question, fontsize=14, fontweight="bold")
        plt.savefig("poll.png")
        plt.close()

        await poll_channel.send(file=File("poll.png"))
        os.remove("poll.png")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handles the reaction add event."""
        async def remove_reaction():
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)

        if payload.channel_id != 1021767477807567028:
            return

        if payload.user_id == self.bot.user.id:
            return

        poll_data = db.get_poll(payload.message_id)

        if not poll_data:
            return await remove_reaction()

        poll = Poll(**json.loads(poll_data[0]))

        if payload.emoji.name not in poll.options:
            return await remove_reaction()

        # check to see if the user has already voted in this poll
        for option in poll.options.values():
            if payload.member.id in option["voters"]:
                return await remove_reaction()

        poll.options[payload.emoji.name]["voters"] += [payload.member.id]
        db.update_poll(payload.message_id, poll)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handles the reaction remove event."""
        if payload.channel_id != 1021767477807567028:
            return

        poll_data = db.get_poll(payload.message_id)

        if not poll_data:
            return

        poll = Poll(**json.loads(poll_data[0]))

        if payload.emoji.name not in poll.options:
            return

        member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)

        if member.id in poll.options[payload.emoji.name]["voters"]:
            poll.options[payload.emoji.name]["voters"].remove(member.id)
        db.update_poll(payload.message_id, poll)


def setup(bot):
    bot.add_cog(PollCog(bot))
    print('Polls is loaded')
