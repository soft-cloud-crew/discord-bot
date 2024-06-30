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
        self.looped = 0
        self.current = None
        self.verbose = False


    async def current_end( self, error = None ):
        idiomas = self.bot.get_cog( 'Translator' )
        print(error) if error else None

        if self.looped == 1 and self.current:
            self.queue.append( self.current )
        elif self.looped == 2 and self.current:
            self.queue.insert( 0, self.current )

        if len(self.queue): self.current = self.queue.pop(0)
        else:
            await self.chan.send( idiomas.traducir( ["musica"], "fila_terminado" ) )
            self.current = None

        #async with self.chan.typing:
        if self.current and self.current['source'] == 'yt':
            source = await YTDLSource.from_url( self.current['query'] )
            title = source.title
            self.current['title'] = title

        elif self.current and nueva_cancion['source'] == 'local':
            title = self.current['query']
            source = discord.PCMVolumeTransformer( discord.FFmpegPCMAudio(f'Musica/{ title }' ) )
            self.current['title'] = title.split('/')[-1]

        if self.current:
            after_func = lambda e: asyncio.run_coroutine_threadsafe( self.current_end( e ), self.bot.loop ).result( )
            self.voice.play( source, after = after_func )

            if self.verbose:
                reproduciendo = idiomas.traducir( ["musica"], "cancion_reproduciendo" )
                await self.chan.send( reproduciendo.format( self.current["title"] ) )


    @commands.hybrid_command( help='Resume la sesion' )
    async def resume( self, ctx ):
        if self.queue:
            await self.current_end()


    @commands.hybrid_command( aliases=['np'], help='Muestra la cancion que se esta reproduciendo' )
    async def playing( self, ctx ):
        idiomas = self.bot.get_cog( "Translator" )
        if self.current:
            reproduciendo = idiomas.traducir( ["musica"], "cancion_reproduciendo" )
            await self.chan.send( reproduciendo.format( self.current["title"] ) )
        else:
            await ctx.send( idiomas.traducir( ["musica"], "fila_vacia" ) )


    @commands.hybrid_command( hidden=True )
    async def set_verbose( self, ctx, value: bool = False ):
        self.verbose = value
        await ctx.send( f'set verbose value to: {value}', ephemeral=True )


    @commands.hybrid_group( fallback = 'local', help = 'Agrega un archivo local a la fila \n en caso de no estar reproduciendo nada comienza la fila' )
    async def play( self, ctx, query ):
        idiomas = self.bot.get_cog( "Translator" )
        self.queue.append( { 'source':'local', 'query':query } )
        text = idiomas.traducir( ["musica"], "fila_local_añadir" )
        await ctx.send( text.format(query) ,ephemeral=not self.verbose )
        self.chan = ctx.channel

        if not self.voice or not self.voice.is_playing():
            await self.current_end()


    @play.command( help = 'Agrega un video de youtube (por id) a la fila \n en caso de no estar reproduciendo nada comienza la fila' )
    async def yt( self, ctx, query ):
        idiomas = self.bot.get_cog( "Translator" )
        self.queue.append( { 'source':'yt', 'query':query } )
        text = idiomas.traducir( ["musica"], "fila_yt_añadir" )
        await ctx.send( text ,ephemeral=not self.verbose )
        self.chan = ctx.channel

        if not self.voice or not self.voice.is_playing():
            await self.current_end()


    @play.command( help = "Para la cancion que se este reproduciendo actualmunte." )
    async def skip( self, ctx ):
        idiomas = self.bot.get_cog( "Translator" )

        self.voice.stop()
        text = idiomas.traducir( ["musica"], "fila_saltar" )
        await ctx.send( text, ephemeral=not self.verbose )


    @play.command( help = 'Activa o desactiva la funcion de bucle \n las opciones son: desactivar bucle de toda la cola y bucle de la canción' )
    async def loop( self, ctx, loop: int ):
        idiomas = self.bot.get_cog( "Translator" )
        if loop not in ( 0, 1, 2 ):
            text = idiomas.traducir( ["musica"], "bucle_no_opcion" )
            await ctx.send( text )

        else:
            self.looped = loop
            txt = idiomas.traducir( ["musica"], "bucle_opcion_"+str(loop) )
            text = idiomas.traducir( ["musica"], "bucle_cambiado" )
            await ctx.send( text.format( txt ) )


    @play.autocomplete( 'query' )
    async def play_autocomplete( self, interaction, curr ):
        return [discord.app_commands.Choice(name=x[7:],value=x[7:]) for x in glob.glob(f'Musica/{ curr }*')][:25]

    @loop.autocomplete( 'loop' )
    async def loop_autocomplete( self, interaction, curr ):
        idiomas = self.bot.get_cog( "Translator" )
        opcion = lambda x: idiomas.traducir( ["musica"], "bucle_opcion_" + str( x ) )
        return [discord.app_commands.Choice(name=opcion(x),value=x) for x in range(3)]


    @yt.before_invoke
    @play.before_invoke
    async def conectado( self, ctx ):
        if ctx.voice_client is None and ctx.author.voice:
            self.voice = await ctx.author.voice.channel.connect()
        elif ctx.voice_client is None:
            idiomas = self.bot.get_cog( "Translator" )
            text = idiomas.traducir( ["musica"], "conectar_no_usuario" )
            await ctx.send( text )
            raise commands.CommandError('Author not connected to VC.')



async def setup( bot ):
    await bot.add_cog( Musica( bot ) )
    print( "Funcionalidad de Musica agregada" )
