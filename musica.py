import asyncio

import discord
from discord.ext import commands


class Musica(commands.Cog):
    def __init__( self, bot ):
        self.bot = bot


    @commands.hybrid_command( falback = 'local', help = 'Reproduce un archivo local' )
    async def play( self, ctx, query ):

        source = discord.PCMVolumeTransformer( discord.FFmpegPCMAudio(f'Musica/{ query }' ) )
        ctx.voice_client.play( source, after = lambda e: print(f'{e}') if e else None )

        await ctx.send( f'Reproduciendo: { query }' )

    @play.before_invoke
    async def conectado( self, ctx ):
        if ctx.voice_client is None and ctx.author.voice:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client is None:
            await ctx.send( 'Usuario no conectado a un canal de voz.' )
            raise commands.CommandError('Author not connected to VC.')



async def setup( bot ):
    await bot.add_cog( Musica( bot ) )
    print( "Funcionalidad de Musica agregada" )
