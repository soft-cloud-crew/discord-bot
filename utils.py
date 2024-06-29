import random
import time
import discord
from discord.ext import commands


def time_text( unix_time ):
    template = "{0:12}\n<t:{1}:{2}> \\<t:{1}:{2}>\n\n"

    text  = template.format( "Relativo:",     unix_time, "R" )
    text += template.format( "Hora corta:",   unix_time, "t" )
    text += template.format( "Dia corto:",    unix_time, "d" )
    text += template.format( "Dia largo:",    unix_time, "D" )
    text += template.format( "Tiempo corto:", unix_time, "f" )
    text += template.format( "Tiempo largo:", unix_time, "F" )

    return text



class TimeMenu(discord.ui.View):


    async def add_time( self, interaction, add_time ):
        idiomas = self.bot.get_cog( 'Translator' )
        org_embed = interaction.message.embeds[0]
        time = int( org_embed.footer.text ) + add_time

        title = idiomas.get_translatable( idiomas.lang, ["utils"], "tiempo_titulo" )
        description = time_text( time )

        embed = discord.Embed( title=title, description=description )
        embed.set_footer( text=time )

        await interaction.response.edit_message( embed=embed )


    @discord.ui.button( label="-1m", style=discord.ButtonStyle.red )
    async def subtract_minute( self, interaction, button ):
        await self.add_time( interaction, -60 )


    @discord.ui.button( label="+1m", style=discord.ButtonStyle.green )
    async def add_minute( self, interaction, button ):
        await self.add_time( interaction, 60 )


    @discord.ui.button( label="-10m", style=discord.ButtonStyle.red )
    async def subtract_ten_minute( self, interaction, button ):
        await self.add_time( interaction, -60*10 )


    @discord.ui.button( label="+10m", style=discord.ButtonStyle.green )
    async def add_ten_minute( self, interaction, button ):
        await self.add_time( interaction, 60*10 )


    @discord.ui.button( label="-1h", style=discord.ButtonStyle.red )
    async def subtract_hour( self, interaction, button ):
        await self.add_time( interaction, -3600 )


    @discord.ui.button( label="+1h", style=discord.ButtonStyle.green )
    async def add_hour( self, interaction, button ):
        await self.add_time( interaction, 3600 )


    @discord.ui.button( label="-1d", style=discord.ButtonStyle.red )
    async def subtract_day( self, interaction, button ):
        await self.add_time( interaction, -3600*24 )


    @discord.ui.button( label="+1d", style=discord.ButtonStyle.green )
    async def add_day( self, interaction, button ):
        await self.add_time( interaction, 3600*24 )


    @discord.ui.button( label="-7d", style=discord.ButtonStyle.red )
    async def subtract_week( self, interaction, button ):
        await self.add_time( interaction, -3600*24*7 )


    @discord.ui.button( label="+7d", style=discord.ButtonStyle.green )
    async def add_week( self, interaction, button ):
        await self.add_time( interaction, 3600*24*7 )


    @discord.ui.button( label="-28d", style=discord.ButtonStyle.red )
    async def subtract_month( self, interaction, button ):
        await self.add_time( interaction, -3600*24*28 )


    @discord.ui.button( label="+28d", style=discord.ButtonStyle.green )
    async def add_month( self, interaction, button ):
        await self.add_time( interaction, 3600*24*28 )


    @discord.ui.button( label="-365d", style=discord.ButtonStyle.red )
    async def subtract_year( self, interaction, button ):
        await self.add_time( interaction, -3600*24*365 )


    @discord.ui.button( label="+365d", style=discord.ButtonStyle.green )
    async def add_year( self, interaction, button ):
        await self.add_time( interaction, 3600*24*365 )



class Utils( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.cuestionarios = { }


    @commands.hybrid_group( fallback='crear' )
    @commands.has_permissions( manage_messages=True )
    async def cuestionario( self, ctx, titulo ):
        idiomas = self.bot.get_cog( 'Translator' )
        
        while True:
            codigo = random.choice( '+-' ) + random.choice( '1234567890abcdef' )
            if codigo not in self.cuestionarios: break

        self.cuestionarios[codigo] = { 'title':titulo, 'date':int( time.time( ) ), 'ans':{ } }

        text = idiomas.get_translatable( idiomas.lang, ["utils"], "cuestionario_creado" )
        await ctx.send( embed=discord.Embed( title=titulo, description=text.format(codigo) ) )


    @cuestionario.command( )
    async def responder( self, ctx, codigo, respuesta ):
        idiomas = self.bot.get_cog( 'Translator' )
        
        if codigo not in self.cuestionarios:
            text = idiomas.get_translatable( idiomas.lang, ["utils"], "cuestionario_no_existe" )
            await ctx.send( text, ephemeral=True )
            return

        ans = { 'answer':respuesta, 'date':int( time.time( ) ) }
        self.cuestionarios[codigo]['ans'][ctx.author.id] = ans

        text = idiomas.get_translatable( idiomas.lang, ["utils"], "cuestionario_respuesta" )
        await ctx.send( text, ephemeral=True )


    @cuestionario.command( )
    @commands.has_permissions( manage_messages=True )
    async def cerrar( self, ctx, codigo ):
        idiomas = self.bot.get_cog( 'Translator' )
        
        if codigo not in self.cuestionarios:
            text = idiomas.get_translatable( idiomas.lang, ["utils"], "cuestionario_no_existe" )
            await ctx.send( text, ephemeral=True )
            return

        cuestionario = self.cuestionarios.pop( codigo )

        title = cuestionario['title']
        answers = map(lambda x: (x, cuestionario['ans'][x]), cuestionario['ans'])
        answers = map(lambda x: f'<@!{ x[0] }> <t:{ x[1]["date"] }:T> - { x[1]["answer"] }', answers)
        text = idiomas.get_translatable( idiomas.lang, ["utils"], "cuestionario_respuestas" )
        description = text.format( cuestionario["date"], '\n'.join(answers) )

        embed = discord.Embed( title=title, description=description )

        await ctx.send( embed=embed )


    @responder.autocomplete( 'codigo' )
    async def responder_autocomplete( self, interaction, curr ):
        return [discord.app_commands.Choice(name=self.cuestionarios[x]['title'],value=x) for x in self.cuestionarios][:25]


    @commands.hybrid_group( fallback='actual' )
    async def tiempo( self, ctx ):
        idiomas = self.bot.get_cog( 'Translator' )
        current_time = int( time.time( ) )

        title = idiomas.get_translatable( idiomas.lang, ["utils"], "tiempo_titulo_actual" )
        description = time_text( current_time )

        embed = discord.Embed( title=title, description=description )
        embed.set_footer( text=current_time )

        await ctx.send( embed=embed, view=TimeMenu() )



async def setup( bot ):

    await bot.add_cog( Utils( bot ) )
    print('Utilidades mixtas agregadas.')
