from mcstatus import JavaServer
from discord.ext import commands

class Minecraft( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.server = JavaServer( "scc-server.duckdns.org", 25565 )

    @commands.hybrid_group( fallback="ping" )
    async def mine( self, ctx ):
        await ctx.send( f"el servidor ha respondido en {await self.server.async_ping()} ms." )

    @mine.command( )
    async def list( self, ctx ):
        query = await self.server.async_query()
        lista = query.players.names
        flista = '\n'.join( lista )
        await ctx.send( f"{len(lista)} usuarios conectados:\n{ flista }" )

async def setup( bot ):
    await bot.add_cog( Minecraft( bot ) )
    print("Funcionalidad para servidor de minecraft")
