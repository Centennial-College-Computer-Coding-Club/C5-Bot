"""disnake UI to select a school program and assign a role to the user"""

from disnake.ext import commands
from disnake.ext.commands import has_permissions
from disnake.ui import View, ActionRow, Item, Select
from disnake import ButtonStyle, ApplicationCommandInteraction, Role
from database import db
import disnake


class ProgramSelectorView(View):
    def __init__(self, inter: ApplicationCommandInteraction, programs: list):
        super().__init__(timeout=60)
        self.inter = inter
        self.programs = programs
        self.selected_program = None
        self.select = Select()
        for program in self.programs:
            self.select.add_option(label=program, value=program)
        self.add_item(self.select)

    async def interaction_check(self, interaction):
        await self.on_selection(interaction)
        return True

    async def on_timeout(self):
        await self.inter.edit_original_message(content="You took too long to select a program. Please try again.",
                                               view=None)

    async def on_error(self, error, item, interaction):
        print(error)
        await self.inter.edit_original_message(content="An error occurred. Please try again.", view=None)

    async def on_selection(self, interaction):
        self.selected_program = interaction.data["values"][0]
        await interaction.response.defer()
        self.stop()


class ProgramSelector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="program", description="Select your program code.")
    async def program(self, inter: ApplicationCommandInteraction):
        """Select your school program code."""
        programs = db.get_programs()
        program_names = [program[1] for program in programs]
        programs_list = [f"{program[0]}-{program[1]}" for program in programs]
        author_roles = [role.name for role in inter.author.roles]

        for name in program_names:
            if name in author_roles:
                await inter.send("You already have a program role.", ephemeral=True)
                return

        view = ProgramSelectorView(inter, programs_list)
        await inter.response.send_message("Please select your program:", view=view, ephemeral=True)
        await view.wait()
        if view.selected_program is None:
            return
        choice = view.selected_program[5:]
        if choice:
            role = disnake.utils.get(inter.guild.roles, name=choice)
            if role:
                await inter.author.add_roles(role)
                await inter.edit_original_message(content=f"You have been assigned the {role.mention} role.", view=None)

    @commands.slash_command(name="create_program", description="Add your program code.")
    async def create_program(self, inter: ApplicationCommandInteraction, program_code: int, program_name: str):
        if len(str(program_code)) != 4:
            await inter.send("Program code must be 4 digits.", ephemeral=True)
            return

        programs = db.get_programs()
        program_codes = [int(program[0]) for program in programs]

        if program_code in program_codes:
            await inter.send("Program code already exists.", ephemeral=True)
            return

        db.add_program(program_code, program_name)
        role = await inter.guild.create_role(
            name=program_name,
            mentionable=True,
            reason=f"Added by {inter.author.name}#{inter.author.discriminator}"
        )
        await inter.send(f"Program added. Role created: {role.mention}", ephemeral=True)

    @has_permissions(manage_roles=True)
    @commands.slash_command(name="remove_program", description="Remove your program code.")
    async def remove_program(self, inter: ApplicationCommandInteraction, program_code: int):
        programs = db.get_programs()
        program_codes = [int(program[0]) for program in programs]
        program_names = [program[1] for program in programs]
        if program_code not in program_codes:
            await inter.send("Program code does not exist.", ephemeral=True)
            return
        db.remove_program(program_code)
        role = disnake.utils.get(inter.guild.roles, name=program_names[program_codes.index(program_code)])
        await role.delete(reason=f"Removed by {inter.author.name}#{inter.author.discriminator}")
        await inter.send(f"Program removed. Role deleted: {role.mention}", ephemeral=True)


def setup(bot):
    bot.add_cog(ProgramSelector(bot))
    print("Program Selector cog loaded")
