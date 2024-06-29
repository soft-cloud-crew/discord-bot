import discord
from discord.ext import commands

class SccHelp( commands.HelpCommand ):
    async def send_command_help( self, command ):
        idiomas = self.context.bot.get_cog( 'Translator' )

        title = idiomas.get_translatable( idiomas.lang, ["help"], "comando_titulo" )
        title = title.format( command.name )
        description = idiomas.get_translatable( idiomas.lang, ["help"], "comando_descripcion" )
        description = description.format( command.qualified_name, command.usage, command.help )
        helpEmbed = discord.Embed( title=title, description=description, color=0xffdc98 )

        aliases = ', '.join( command.aliases )
        if not aliases:
            aliases = idiomas.get_translatable( idiomas.lang, ["help"], "comando_sin_alias" )
        helpEmbed.add_field( name = idiomas.get_translatable( idiomas.lang, ["help"], "alias" ), value = aliases )

        canal = self.get_destination( )
        await canal.send( embed = helpEmbed )


    async def send_group_help( self, group ):
        idiomas = self.context.bot.get_cog( 'Translator' )

        title = idiomas.get_translatable( idiomas.lang, ["help"], "categoria_titulo" )
        title = title.format( group.qualified_name )
        description = idiomas.get_translatable( idiomas.lang, ["help"], "categoria_descripcion" )
        description = description.format( group.qualified_name, group.usage, group.help )
        helpEmbed = discord.Embed( title=title, description=description, color=0xffdc98 )

        commandList = await self.filter_commands( group.commands, sort=True )
        commandList = map( lambda x: f"{ x.name }: { x.short_doc }", commandList )
        commandList = '\n'.join( commandList )
        helpEmbed.add_field( name = 'Comandos', value = commandList )

        aliases = ', '.join( group.aliases )
        if not aliases:
            aliases = idiomas.get_translatable( idiomas.lang, ["help"], "comando_sin_alias" )
        helpEmbed.add_field( name = 'Alias', value = aliases, inline = False )

        canal = self.get_destination( )
        await canal.send( embed = helpEmbed )


    async def send_bot_help( self, mapping ):

        idiomas = self.context.bot.get_cog( 'Translator' )
        title = idiomas.get_translatable( idiomas.lang, ["help"], "bot_titulo" )
        description = idiomas.get_translatable( idiomas.lang, ["help"], "bot_descripcion" )
        helpEmbed = discord.Embed( title=title, description=description, color=0xffdc98 )

        for cog in mapping.keys( ):
            commandsList = mapping[ cog ]
            if cog == None:
                cog = idiomas.get_translatable( idiomas.lang, ["help"], "categoria_nula" )
            else: cog = cog.qualified_name
            command = ', '.join( map( lambda x: x.qualified_name, commandsList ) )
            helpEmbed.add_field( name = cog, value = command )

        canal = self.get_destination( )
        await canal.send( embed = helpEmbed )

async def setup( bot ):
    bot.help_command = SccHelp( )
    print( 'Funcionalidad de Ayuda agregada' )
