"""All moderation commands for the bot."""

from disnake import ApplicationCommandInteraction, Member, VoiceChannel, Role, Message
from disnake.ext import commands
import json


def duration_converter(duration: str) -> int:
    if duration[-1] == "s":
        duration = int(duration[:-1])
    elif duration[-1] == "m":
        duration = int(duration[:-1]) * 60
    elif duration[-1] == "h":
        duration = int(duration[:-1]) * 3600
    elif duration[-1] == "d":
        duration = int(duration[:-1]) * 86400
    else:
        duration = int(duration)
    return duration


class Moderation(commands.Cog):
    """Moderation commands"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_slash_command_check(self, inter: ApplicationCommandInteraction) -> bool:
        """Only allow bot devs to use these commands."""
        if 1019047886077562913 in [role.id for role in inter.author.roles]:
            return True
        await inter.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return False

    @staticmethod
    async def log(inter: ApplicationCommandInteraction, action: str, member: Member = None, duration: str = None,
                  reason: str = None):
        """Logs moderation actions to the moderation log channel."""
        channel = inter.guild.get_channel(1020312901665423411)
        if reason is None:
            reason = "No reason provided."
        if duration is None and member is None:
            await channel.send(f"{inter.author.mention} {action} for {reason}")
        elif duration is None:
            await channel.send(f"{inter.author.mention} {action} {member.mention} for {reason}")
        else:
            await channel.send(f"{inter.author.mention} {action} {member.mention} for {duration} for {reason}")

    @commands.slash_command(name="kick", description="Kicks a user.")
    async def kick(self, inter: ApplicationCommandInteraction, member: Member, *, reason: str = None):
        """Kicks a user."""
        try:
            await member.kick(reason=reason)
            await self.log(inter, "kicked", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been kicked.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error kicking {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="ban", description="Bans a user.")
    async def ban(self, inter: ApplicationCommandInteraction, member: Member, *, reason: str = None):
        """Bans a user."""
        try:
            await member.ban(reason=reason)
            await self.log(inter, "banned", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been banned.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error banning {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="unban", description="Unbans a user.")
    async def unban(self, inter: ApplicationCommandInteraction, member: Member, *, reason: str = None):
        """Unbans a user."""
        try:
            await member.unban(reason=reason)
            await self.log(inter, "unbanned", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been unbanned.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error unbanning {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="timeout", description="Times out a user.")
    async def timeout(self, inter: ApplicationCommandInteraction, member: Member, duration: str, *, reason: str = None):
        """Times out a user."""
        try:
            await member.timeout(duration=duration_converter(duration), reason=reason)
            await self.log(inter, "timed out", member, duration=duration, reason=reason)
            await inter.response.send_message(f"{member.name} has been timed out.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error timing out {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="untimeout", description="Untimes out a user.")
    async def untimeout(self, inter: ApplicationCommandInteraction, member: Member, *, reason: str = None):
        """Untimes out a user."""
        try:
            await member.untimeout(reason=reason)
            await self.log(inter, "untimed out", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been untimed out.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error untiming out {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="mute", description="Mutes a user.")
    async def mute(self, inter: ApplicationCommandInteraction, member: Member, duration: str, *, reason: str = None):
        """Mutes a user."""
        try:
            await member.mute(duration=duration_converter(duration), reason=reason)
            await self.log(inter, "muted", member, duration=duration, reason=reason)
            await inter.response.send_message(f"{member.name} has been muted.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error muting {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="unmute", description="Unmutes a user.")
    async def unmute(self, inter: ApplicationCommandInteraction, member: Member, *, reason: str = None):
        """Unmutes a user."""
        try:
            await member.unmute(reason=reason)
            await self.log(inter, "unmuted", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been unmuted.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error unmuting {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="deafen", description="Deafens a user.")
    async def deafen(self, inter: ApplicationCommandInteraction, member: Member, duration: str, *, reason: str = None):
        """Deafens a user."""
        try:
            await member.deafen(duration=duration_converter(duration), reason=reason)
            await self.log(inter, "deafened", member, duration=duration, reason=reason)
            await inter.response.send_message(f"{member.name} has been deafened.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error deafening {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="undeafen", description="Undeafens a user.")
    async def undeafen(self, inter: ApplicationCommandInteraction, member: Member, *, reason: str = None):
        """Undeafens a user."""
        try:
            await member.undeafen(reason=reason)
            await self.log(inter, "undeafened", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been undeafened.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error undeafening {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="move", description="Moves a user to a voice channel.")
    async def move(self, inter: ApplicationCommandInteraction, member: Member, channel: VoiceChannel, *, reason: str = None):
        """Moves a user to a voice channel."""
        try:
            await member.move_to(channel, reason=reason)
            await self.log(inter, "moved", member, reason=reason)
            await inter.response.send_message(f"{member.name} has been moved to {channel.name}.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error moving {member.name}: {e}", ephemeral=True)

    @commands.slash_command(name="nick", description="Changes a user's nickname.")
    async def nick(self, inter: ApplicationCommandInteraction, member: Member, *, nickname: str = None):
        """Changes a user's nickname."""
        try:
            await member.edit(nick=nickname)
            await self.log(inter, "changed nickname of", member, reason=nickname)
            await inter.response.send_message(f"{member.name}'s nickname has been changed to {nickname}.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error changing {member.name}'s nickname: {e}", ephemeral=True)

    @commands.slash_command(name="purge", description="Purges messages.")
    async def purge(self, inter: ApplicationCommandInteraction, amount: int, member: Member = None):
        """Purges messages."""
        try:
            if member:
                await inter.channel.purge(limit=amount, check=lambda m: m.author == member)
                await self.log(inter, "purged messages from", member, reason=amount)
            else:
                await inter.channel.purge(limit=amount)
                await self.log(inter, "purged messages", reason=amount)
            await inter.response.send_message(f"{amount} messages have been purged.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error purging messages: {e}", ephemeral=True)

    @commands.slash_command(name="role", description="Gives or removes a role from a user.")
    async def role(self, inter: ApplicationCommandInteraction, member: Member, role: Role, add: bool = True):
        """Gives or removes a role from a user."""
        try:
            if add:
                await member.add_roles(role)
                await self.log(inter, "added role", member, reason=role.name)
                await inter.response.send_message(f"{role.name} has been added to {member.name}.", ephemeral=True)
            else:
                await member.remove_roles(role)
                await self.log(inter, "removed role", member, reason=role.name)
                await inter.response.send_message(f"{role.name} has been removed from {member.name}.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error adding/removing role: {e}", ephemeral=True)

    @commands.slash_command(name="roles", description="Lists all roles.")
    async def roles(self, inter: ApplicationCommandInteraction):
        """Lists all roles."""
        try:
            roles = [role.name for role in inter.guild.roles]
            await inter.response.send_message(f"Roles: {', '.join(roles)}", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error listing roles: {e}", ephemeral=True)

    @commands.slash_command(name="slowmode", description="Sets the slowmode of a channel.")
    async def slowmode(self, inter: ApplicationCommandInteraction, seconds: int):
        """Sets the slowmode of a channel."""
        try:
            await inter.channel.edit(slowmode_delay=seconds)
            await self.log(inter, "set slowmode to", reason=str(seconds))
            await inter.response.send_message(f"Slowmode has been set to {seconds} seconds.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error setting slowmode: {e}", ephemeral=True)

    @commands.slash_command(name="whitelist", description="Adds a domain link or invite code to the whitelist.")
    async def whitelist(self, inter: ApplicationCommandInteraction, *, domain: str):
        """Adds a domain link or invite code to the whitelist."""
        try:
            if domain.startswith("http"):
                domain = domain.split("/")[2]
            if domain.startswith("www."):
                domain = domain[4:]
            if domain.startswith("discord.gg"):
                domain = domain.split("/")[1]
            if domain in self.bot.whitelist:
                await inter.response.send_message(f"{domain} is already whitelisted.", ephemeral=True)
            else:
                self.bot.whitelist.append(domain)
                with open("whitelist.json", "w") as f:
                    json.dump({"whitelist": self.bot.whitelist}, f)
                await self.log(inter, "whitelisted", reason=domain)
                await inter.response.send_message(f"{domain} has been whitelisted.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Error whitelisting {domain}: {e}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Checks if a message is a command."""
        if message.author.bot:
            return
        elif "discord.gg" in message.content:
            if message.content.split("/")[-1] not in self.bot.whitelist:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, you are not allowed to post invite links here.",
                                           delete_after=5)
                await self.log(message,
                               f"sent an invite link that was blocked in {message.channel.mention}",
                               reason=message.content)
        # elif "http" in message.content:
        #     if message.content.split("/")[2] not in self.bot.whitelist:
        #         await message.delete()
        #         await message.channel.send(f"{message.author.mention}, you are not allowed to post links here.",
        #                                    delete_after=5)
        if message.content.startswith(self.bot.command_prefix):
            await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Moderation(bot))
    print("Moderation cog loaded")
