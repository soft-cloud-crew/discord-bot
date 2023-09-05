from mcstatus import JavaServer
from discord.ext import commands

class Minecraft( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.server = JavaServer( "scc-server.duckdns.org" )

    @command.hybrid_group( fallback="ping" )
    async def mine( self, ctx ):
        await ctx.send( f"el servidor ha respondido en {self.server.ping()} ms." )

    @mine.hybrid_command( )
    async def list( self, ctx ):
        query = self.server.query()
        lista = query.players.names
        await ctx.send( f"{len(lista)} usuarios conectados:\n{'\n'.join(lista)}" )

async def setup( bot ):
    bot.add_cog( Minecraft( bot ) )
    print("Funcionaliiad para servidor de minecraft")
