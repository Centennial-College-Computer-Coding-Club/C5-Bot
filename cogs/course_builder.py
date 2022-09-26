import json
from disnake.ext import commands
from disnake.utils import get
from disnake import PermissionOverwrite, ApplicationCommandInteraction
import re


categories = [1023227498009477262, 1023355121117180066, 1023355206513213440]
pattern = r"([A-Z]-(?=[A-Z]))|([A-Z](?=[0-9])|[0-9](?=[A-Z]))"


class ProgramBuilder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="create_program_channels", description="Create program channels")
    async def create_program_channels(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()
        with open("unique_courses.json", "r") as f:
            programs = json.load(f)

        for program in programs:
            if not get(inter.guild.channels, name=program.lower()):
                role = await self.bot.guilds[0].create_role(name=program)
                for category in categories:
                    cat = get(inter.guild.categories, id=category)
                    if len(cat.channels) == 50:
                        continue
                    else:
                        break
                else:
                    await inter.followup.send("All categories are full!")
                    return
                await self.bot.guilds[0].create_text_channel(
                    name=program,
                    topic=f"{programs[program]}",
                    category=cat,
                    overwrites={
                        self.bot.guilds[0].default_role: PermissionOverwrite(view_channel=False),
                        role: PermissionOverwrite(view_channel=True),
                        self.bot.guilds[0].get_role(1019047886077562913): PermissionOverwrite(view_channel=True),
                        self.bot.guilds[0].me: PermissionOverwrite(view_channel=True),
                    }
                )
        await inter.followup.send("Done")

    @commands.slash_command(name="add_courses", description="Add a course to your roles")
    async def add_courses(self, inter: ApplicationCommandInteraction, course: str):
        courses = [re.sub(pattern, lambda x: x.group(1)[:-1] if x.group(1) else x.group(2) + "-",
                          course.upper().strip()) for course in course.upper().split(",")]
        added_courses = []
        not_added_courses = []
        for course in courses:
            role = get(inter.guild.roles, name=course)
            if role:
                if role in inter.author.roles:
                    not_added_courses.append(course)
                    continue
                await inter.author.add_roles(role)
                added_courses.append(course)
                channel = get(inter.guild.channels, name=course.lower())
                category = get(inter.guild.categories, id=1016871747200495650)
                if channel.category != category:
                    await channel.edit(category=category)
            else:
                continue
        if added_courses:
            await inter.send(f"You have been added to {', '.join(added_courses)}", ephemeral=True)
            if not_added_courses:
                await inter.followup.send(f"The following courses were not added: {', '.join(not_added_courses)}",
                                          ephemeral=True)
        else:
            await inter.send("No courses were added", ephemeral=True)

    @commands.slash_command(name="remove_courses", description="Remove a course from your roles")
    async def remove_courses(self, inter: ApplicationCommandInteraction, course: str):
        courses = [re.sub(pattern, lambda x: x.group(1)[:-1] if x.group(1) else x.group(2) + "-",
                          course.upper().strip()) for course in course.upper().split(",")]
        removed_courses = []
        not_removed_courses = []
        for course in courses:
            role = get(inter.guild.roles, name=course)
            if role:
                if role not in inter.author.roles:
                    not_removed_courses.append(course)
                    continue
                await inter.author.remove_roles(role)
                removed_courses.append(course)
                role = get(inter.guild.roles, name=course)
                if not role.members:
                    channel = get(inter.guild.channels, name=course.lower())
                    for category in categories:
                        cat = get(inter.guild.categories, id=category)
                        if len(cat.channels) == 50:
                            continue
                        else:
                            break
                    else:
                        await inter.followup.send("All categories are full!")
                        return
                    await channel.edit(category=cat)
            else:
                not_removed_courses.append(course)
                continue
        if removed_courses:
            await inter.send(f"You have been removed from {', '.join(removed_courses)}", ephemeral=True)
            if not_removed_courses:
                await inter.followup.send(f"The following courses were not removed: {', '.join(not_removed_courses)}",
                                          ephemeral=True)
        else:
            await inter.send("No courses were removed", ephemeral=True)


def setup(bot):
    bot.add_cog(ProgramBuilder(bot))
    print("ProgramBuilder cog loaded")