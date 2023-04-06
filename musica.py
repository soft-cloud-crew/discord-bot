import asyncio
import os

import discord
from discord.ext import commands

import yt_dlp
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl = {
    'format':'bestaudio/best',
    'outtmpl':'Musica/youtube/%(title)s [%(id)s].%(ext)s',
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
}
ytdl = yt_dlp.YoutubeDL(ytdl)

ffmpeg_options = {'options': '-vn'}


class YTDLSource( discord.PCMVolumeTransformer ):
    def __init__( self, source, data , volume=0.5 ):
        super().__init__( source, volume=volume )

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url( cls, url, loop=None ):
        loop = loop or asyncio.get_event_loop( )
        data = await loop.run_in_executor( None, lambda: ytdl.extract_info( url, download=True ) )
        
        if 'entries' in data:
            data = data['entries'][0]

        filename = ytdl.prepare_filename( data )
        return cls( discord.FFmpegPCMAudio( filename, **ffmpeg_options ), data )


class Musica(commands.Cog):
    def __init__( self, bot ):
        self.bot = bot


    @commands.hybrid_group( falback = 'local', help = 'Reproduce un archivo local \n por el momento no soporta fila' )
    async def play( self, ctx, query ):

        source = discord.PCMVolumeTransformer( discord.FFmpegPCMAudio(f'Musica/{ query }' ) )
        ctx.voice_client.play( source, after = lambda e: print(f'{e}') if e else None )

        await ctx.send( f'Reproduciendo: { query }' )


    @play.command( help = 'reproduce un video de yt \n por el momento no soporta fila' )
    async def yt( self, ctx, query ):

        async with ctx.typing():
            player = await YTDLSource.from_url( query, self.bot.loop )
            ctx.voice_client.play( player, after = lambda e: print(f'{e}') if e else None )

        await ctx.send( f'Reproduciendo: { player.title }' )


    @play.autocomplete( 'query' )
    async def play_autocomplete( self, interaction, curr ):
        return [discord.app_commands.Choice(name=x,value=x) for x in os.listdir('./Musica')][:25]


    @yt.before_invoke
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
