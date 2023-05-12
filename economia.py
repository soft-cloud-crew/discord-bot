from discord.ext import commands
import discord as dis
import sqlite3
import typing as ty


def has_admin():
    def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)


class Economia( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot

    @commands.hybrid_group( fallback = "get", help = "Ve tu dinero actual o el de otra persona." )
    async def eco( self, ctx, miembro: dis.Member = None ):
        if miembro == None: miembro = ctx.author
        sql = self.bot.get_cog( 'sql' )

        dinero = sql.getAtt( 'dinero', 'economia', miembro.id )
        await ctx.send( f'El miembro { miembro.display_name } tiene { dinero }$' )

    @eco.command( help = "Transfiere una cantidad de dinero a otra persona" )
    async def give( self, ctx, miembro: dis.Member, amount: int ):
        amount = abs( amount )
        sql = self.bot.get_cog( 'sql' )

        money_author = sql.getAtt( 'dinero', 'economia', ctx.author.id )
        money_member = sql.getAtt( 'dinero', 'economia', ctx.author.id )
        sql.modifyAtt( 'dinero', 'economia' miembro.id,    money_member + amount )
        sql.modifyAtt( 'dinero', 'economia' ctx.author.id, money_author - amount )

        await ctx.send( f'El miembro { ctx.author.display_name } le ha regalado { amount }$ a { miembro.display_name }' )

    @eco.command( help = "Imprime dinero, nada mejor para la economia." )
    @has_admin( )
    async def imprimir( self, ctx ):
        await ctx.send( "no deberias hacer esto" )


async def setup( bot ):
    await bot.add_cog( Economia( bot ) )
    bot.get_cog( 'sql' ).add_default( 'dinero', 'economia', 0 )
    print( "Funcionalidad de Economia agregada" )

