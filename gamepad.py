import socket
from discord.ext import commands
import discord



class GameMenu( discord.ui.View ):


    def send_event( self, event: int ):
        c = socket.socket( )
        c.connect( ( '127.0.0.1', 1334 ) )
        c.send( bytes( (event,) ) )
        c.close( )


    @discord.ui.button( label="^" )
    async def buttonUp( self, interaction, button ):
        self.send_event( 1 )


    @discord.ui.button( label="V" )
    async def buttonDown( self, interaction, button ):
        self.send_event( 2 )


    @discord.ui.button( label="<" )
    async def buttonLeft( self, interaction, button ):
        self.send_event( 3 )


    @discord.ui.button( label=">" )
    async def buttonRight( self, interaction, button ):
        self.send_event( 4 )


    @discord.ui.button( label="A" )
    async def buttonA( self, interaction, button ):
        self.send_event( 5 )


    @discord.ui.button( label="B" )
    async def buttonB( self, interaction, button ):
        self.send_event( 6 )


    @discord.ui.button( label="Y" )
    async def buttonY( self, interaction, button ):
        self.send_event( 7 )


    @discord.ui.button( label="X" )
    async def buttonX( self, interaction, button ):
        self.send_event( 8 )


    @discord.ui.button( label="L" )
    async def buttonL( self, interaction, button ):
        self.send_event( 9 )


    @discord.ui.button( label="R" )
    async def buttonR( self, interaction, button ):
        self.send_event( 10 )


    @discord.ui.button( label="-" )
    async def buttonSelect( self, interaction, button ):
        self.send_event( 11 )


    @discord.ui.button( label="+" )
    async def buttonStart( self, interaction, button ):
        self.send_event( 12 )

class Gamepad( commands.Cog ):


    def __init__( self, bot ):
        self.bot = bot


    @commands.hybrid_command( )
    async def gamepad( self, ctx ):
        await ctx.send( "a", view=GameMenu( ) )



async def setup( bot ):

    await bot.add_cog( Gamepad( bot ) )
