from distutils.util import strtobool

from disnake import RawReactionActionEvent
from disnake.ext.commands import Cog


class ReactionLogger(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.channel = None

    def channel_is_set(self):
        if not self.channel:
            self.bot.ph.warn("No valid emoji log channel has been found yet, ignoring log.")
            return False
        return True

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if not self.channel_is_set():
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        await self.embed(self.channel, title=reaction_logger["added"]["title"],
                         message=reaction_logger["added"]["content"].format(member=member, guild=guild,
                                                                            emoji=payload.emoji, channel=channel),
                         footer=Footer(reaction_logger["added"]["footer"].get("text"),
                                       reaction_logger["added"]["footer"].get("icon").format(guild=guild),
                                       reaction_logger["added"]["footer"].get("timestamp")),
                         color=(None if reaction_logger["added"]["color"].get("random", True) else
                                reaction_logger["added"]["color"].get("color", 0x00ff00)))

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if not self.channel_is_set():
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        await self.embed(self.channel, title=reaction_logger["removed"]["title"],
                         message=reaction_logger["removed"]["content"].format(member=member, guild=guild,
                                                                              emoji=payload.emoji, channel=channel),
                         footer=Footer(reaction_logger["removed"]["footer"].get("text"),
                                       reaction_logger["removed"]["footer"].get("icon").format(guild=guild),
                                       reaction_logger["removed"]["footer"].get("timestamp")),
                         color=(None if reaction_logger["removed"]["color"].get("random", True) else
                                reaction_logger["removed"]["color"].get("color", 0xff0000)))


def setup(bot):
    if strtobool(cfg["REACTION_LOGGING"].get("enabled", "true")):
        bot.add_cog(ReactionLogger(bot))