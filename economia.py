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
        self.con = sqlite3.connect( "db/economia.db" )
        self.cur = self.con.cursor( )

    def cog_unload( self ):
        self.con.close( )

    def getMoney( self, uuid: int ):
        res = self.cur.execute( "SELECT dinero FROM economia WHERE uuid IS ?;", ( uuid, ) ).fetchone( )
        if res == None:
            self.cur.execute( "INSERT INTO economia VALUES(?,?)", ( uuid, 0 ) )
            self.con.commit( )
            res = self.cur.execute( "SELECT dinero FROM economia WHERE uuid IS ?;", ( uuid, ) ).fetchone( )
        return res[0] 

    def modifyMoney( self, uuid: int, amount: int ):
        dinero = self.getMoney( uuid ) + amount
        self.cur.execute( "UPDATE economia SET dinero = ? WHERE uuid IS ?;", ( dinero, uuid ) )
        self.con.commit( )


    @commands.hybrid_group( fallback = "get", help = "Ve tu dinero actual o el de otra persona." )
    async def eco( self, ctx, miembro: dis.Member = None ):
        if miembro == None: miembro = ctx.author
        dinero = self.getMoney(miembro.id)
        await ctx.send( f'El miembro { miembro.display_name } tiene { dinero }$' )

    @eco.command( help = "Transfiere una cantidad de dinero a otra persona" )
    async def give( self, ctx, miembro: dis.Member, amount: int ):
        amount = abs( amount )
        self.modifyMoney( miembro.id, amount )
        self.modifyMoney( ctx.author.id, -amount )
        await ctx.send( f'El miembro { ctx.author.display_name } le ha regalado { amount }$ a { miembro.display_name }' )

    @eco.command( help = "Imprime dinero, nada mejor para la economia." )
    @has_admin( )
    async def imprimir( self, ctx ):
        await ctx.send( "no deberias hacer esto" )


async def setup( bot ):
    await bot.add_cog( Economia( bot ) )
    print( "Funcionalidad de Economia agregada" )

