from discord import commands
import discord



class Torneo( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot


    @commands.hybrid_group( fallback="crear", help="Crea un torneo" )
    async def torneo( self, ctx, titulo: str, args: str = None ):
        sql = self.bot.get_cog( 'Sql' )

        pass



async def setup( bot ):
    await bot.add_cog( Torneo( bot ) )
    print( "Funcionalidad de Torneos agregada" )
