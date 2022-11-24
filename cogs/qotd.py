'''Question of the Day cog'''

from disnake.ext import commands
from database import db


class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="qotd", description="Get the question of the day")
    async def qotd(self, inter):
        data = db.get_random_qotd()
        if data:
            await inter.response.send_message(data[0])
        else:
            await inter.response.send_message("No questions found", ephemeral=True)

    @commands.slash_command(name="add_qotd", description="Add a question of the day")
    async def add_qotd(self, inter, *, question: str):
        db.add_qotd(question, 0)
        await inter.response.send_message("Question added", ephemeral=True)

    @commands.slash_command(name="reset_qotd", description="Reset all questions of the day")
    async def reset_qotd(self, inter):
        db.reset_qotd()
        await inter.response.send_message("Questions reset", ephemeral=True)


def setup(bot):
    bot.add_cog(QOTD(bot))
    print('QOTD is loaded')
