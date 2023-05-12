import asyncio
import glob

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
        self.queue = []
        self.voice = None
        self.chan = None


    async def current_end( self, error = None ):
        print(error) if error else None
        if len(self.queue): nueva_cancion = self.queue.pop(0)
        else: return None

        #async with self.chan.typing:
        if nueva_cancion['source'] == 'yt':
            source = await YTDLSource.from_url( nueva_cancion['query'] )
            title = source.title
        elif nueva_cancion['source'] == 'local':
            title = nueva_cancion['query']
            source = discord.PCMVolumeTransformer( discord.FFmpegPCMAudio(f'Musica/{ title }' ) )
        after_func = lambda e: asyncio.run_coroutine_threadsafe( self.current_end( e ), self.bot.loop ).result( )
        self.voice.play( source, after = after_func )

        await self.chan.send( f'Reproduciendo: { title }' )


    @commands.hybrid_group( fallback = 'local', help = 'Agrega un archivo local a la fila \n en caso de no estar reproduciendo nada comienza la fila' )
    async def play( self, ctx, query ):
        self.queue.append( { 'source':'local', 'query':query } )
        await ctx.send( f'La cancion { query } ha sido añadida a la cola.' )
        self.chan = ctx.channel

        if not self.voice or not self.voice.is_playing():
            await self.current_end()


    @play.command( help = 'Agrega un video de youtube (por id) a la fila \n en caso de no estar reproduciendo nada comienza la fila' )
    async def yt( self, ctx, query ):
        self.queue.append( { 'source':'yt', 'query':query } )
        await ctx.send( 'La cancion ha sido añadida a la cola.' )
        self.chan = ctx.channel

        if not self.voice or not self.voice.is_playing():
            await self.current_end()


    @play.autocomplete( 'query' )
    async def play_autocomplete( self, interaction, curr ):
        return [discord.app_commands.Choice(name=x[7:],value=x[7:]) for x in glob.glob(f'Musica/{ curr }*')][:25]


    @yt.before_invoke
    @play.before_invoke
    async def conectado( self, ctx ):
        if ctx.voice_client is None and ctx.author.voice:
            self.voice = await ctx.author.voice.channel.connect()
        elif ctx.voice_client is None:
            await ctx.send( 'Usuario no conectado a un canal de voz.' )
            raise commands.CommandError('Author not connected to VC.')



async def setup( bot ):
    await bot.add_cog( Musica( bot ) )
    print( "Funcionalidad de Musica agregada" )
