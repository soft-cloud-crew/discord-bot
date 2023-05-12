from discord.ext import commands
import discord
import sqlite3

class Sql( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.con = sqlite3.connect( 'db/scc.db' )
        self.cur = self.con.cursor( )
        self.defaults = {}


    def cog_unload( self ):
        self.con.close( )


    def add_default( self, att, table, default):
        if table not in self.defaults       : self.defaults[table] = {}
        self.defaults[table][att] = default


    def put_default( self, att, table, uuid, insert=False ):
        default = self.defaults[table][att]
        if insert:
            self.cur.execute( 'INSERT INTO ? values(?)', ( table, uuid ) )
        self.cur.execute( 'UPDATE ? set ? = ? WHERE uuid IS ?;', ( table, att, default , uuid ) )
        self.con.commit( )


    def getAtt( self, att: str, table: str , uuid: int ):
        query = 'SELECT ? FROM ? WHERE uuid IS ?;'

        res = self.cur.execute( query, ( att, table, uuid ) ).fetchone( )

        if res == None:
            self.put_default( att, table, uuid, True )
            res = self.cur.execute( query, ( att, table, uuid ) ).fetchone( )

        elif res[0] == None:
            self.put_default( att, table, uuid )
            res = self.cur.execute( query, ( att, table, uuid ) ).fetchone( )

        return res[0]


    def modifyAtt( self, att: str, table: str, uuid: int, value ):
        res = self.cur.execute( 'SELECT * FROM ? WHERE uuid IS ?', ( table, uuid ) ).fetchone( )

        if res == None:
            self.put_default( att, table, uuid, True)

        self.cur.execute( 'UPDATE ? SET ? = ? WHERE uuid IS ?;', ( table, att, value, uuid ) )
        self.con.commit( )



async def setup( bot ):
    await bot.add_cog( Sql( bot ) )
    print( 'Funcionalidad de Base de Datos agregada' )
