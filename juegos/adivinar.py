from discord.ext import commands

class Adivinar( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.integrantes = { }

    @commands.command( )
    async def unirse( self, bot )
