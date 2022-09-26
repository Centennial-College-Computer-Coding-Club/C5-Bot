from discord import RawReactionActionEvent
from utilsx.discord import Cog

from config.reaction_roles import reaction_roles


class ReactionRoles(Cog):
    """
    This instance handles all reaction role events.
    """
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def process_reaction(self, payload: RawReactionActionEvent, r_type=None) -> None:
        if payload.message_id in reaction_roles.keys():
            for obj in reaction_roles[payload.message_id]:
                if obj[0] == payload.emoji.name:
                    guild = self.bot.get_guild(payload.guild_id)
                    user = await guild.fetch_member(payload.user_id)
                    role = guild.get_role(obj[1])
                    if role is None:
                        self.bot.ph.warn(f"An invalid role ID ({obj[0]}, {obj[1]}) was provided in `reaction_roles` for"
                                         f" message with ID: {payload.message_id}")
                        self.bot.ph.warn("Not performing any action as result.")
                    elif r_type == "add":
                        await user.add_roles(role)
                    elif r_type == "remove":
                        await user.remove_roles(role)
                    else:
                        self.bot.ph.warn("Invalid reaction type was provided in `process_reaction`.")
                        self.bot.ph.warn("Not performing any action as result.")
                    break

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.process_reaction(payload, "add")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        await self.process_reaction(payload, "remove")


def setup(bot):
    bot.add_cog(ReactionRoles(bot))