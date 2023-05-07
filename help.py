import discord
from discord.ext import commands

class SccHelp( commands.HelpCommand ):
    async def send_command_help( self, command ):

        title = f'Ayuda del comando: { command.name }'
        description = f's${ command.qualified_name } { command.usage }\n{ command.help }'
        helpEmbed = discord.Embed( title=title, description=description, color=0xffdc98 )

        aliases = ', '.join( command.aliases )
        if not aliases: aliases = "Ninguno"
        helpEmbed.add_field( name = 'Alias', value = aliases )

        canal = self.get_destination( )
        await canal.send( embed = helpEmbed )


    async def send_group_help( self, group ):
        title = f'Ayuda del grupo: { group.qualified_name }'
        description = f's${ group.qualified_name } { group.usage }\n{ group.help }'
        helpEmbed = discord.Embed( title=title, description=description, color=0xffdc98 )

        commandList = await self.filter_commands( group.commands, sort=True )
        commandList = map( lambda x: f"{ x.name }: { x.short_doc }", commandList )
        commandList = '\n'.join( commandList )
        helpEmbed.add_field( name = 'Comandos', value = commandList )

        aliases = ', '.join( group.aliases )
        if not aliases: aliases = "Ninguno"
        helpEmbed.add_field( name = 'Alias', value = aliases, inline = False )

        canal = self.get_destination( )
        await canal.send( embed = helpEmbed )


    async def send_bot_help( self, mapping ):

        title = 'Comandos del bot del SCC'
        description = '''
            Bot personal del SCC con funcionalidad de economia entre otras cosas.
            (en desarrollo)
            '''
        helpEmbed = discord.Embed( title=title, description=description, color=0xffdc98 )

        for cog in mapping.keys( ):
            commandsList = mapping[ cog ]
            if cog == None: cog = 'Misceláneo'
            else: cog = cog.qualified_name
            command = ', '.join( map( lambda x: x.qualified_name, commandsList ) )
            helpEmbed.add_field( name = cog, value = command )

        canal = self.get_destination( )
        await canal.send( embed = helpEmbed )

async def setup( bot ):
    bot.help_command = SccHelp( )
    print( 'Funcionalidad de Ayuda agregada' )
