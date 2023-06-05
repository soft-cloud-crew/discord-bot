import random
import time
import discord
from discord.ext import commands


class Utils( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.cuestionarios = { }


    @commands.hybrid_group( fallback='crear' )
    async def cuestionario( self, ctx, titulo ):
        
        while True:
            codigo = random.choice( '+-' ) + random.choice( '1234567890abcdef' )
            if codigo not in self.cuestionarios: break

        self.cuestionarios[codigo] = { 'title':titulo, 'date':int( time.time( ) ), 'ans':{ } }

        await ctx.send( embed=discord.Embed( title=titulo, description=f'Se ha creado un cuestionario con codigo: { codigo }' ) )


    @cuestionario.command( )
    async def responder( self, ctx, codigo, respuesta ):
        
        if codigo not in self.cuestionarios:
            await ctx.send( 'El cuestionario no existe.', ephemeral=True )
            return

        ans = { 'answer':respuesta, 'date':int( time.time( ) ) }
        self.cuestionarios[codigo]['ans'][ctx.author.id] = ans

        await ctx.send( 'Tu respuesta ha sido agregada', ephemeral=True )


    @cuestionario.command( )
    async def cerrar( self, ctx, codigo ):
        
        if codigo not in self.cuestionarios:
            await ctx.send( 'El cuestionario no existe.', ephemeral=True )
            return

        cuestionario = self.cuestionarios.pop( codigo )

        title = cuestionario['title']
        answers = map(lambda x: (x, cuestionario['ans'][x]), cuestionario['ans'])
        answers = map(lambda x: f'<@!{ x[0] }> <t:{ x[1]["date"] }:T> - { x[1]["answer"] }', answers)
        description = f'Cuestionario creado el: <t:{ cuestionario["date"] }:T>\n\n' + '\n'.join(answers)

        embed = discord.Embed( title=title, description=description )

        await ctx.send( embed=embed )



async def setup( bot ):

    await bot.add_cog( Utils( bot ) )
    print('Utilidades mixtas agregadas.')
