import discord
from discord.ext import commands
import os

class Translator( commands.Cog ):
    def __init__( self, bot ):
        self.bot = bot
        self.lang = 'es'
        self.langs = { }
        self.__importar_langs__( )


    def add_to_langs( self, path: list[str], value: str ):
        lang = path[  0 ]
        key  = path[ -1 ]
        path = path[1:-1]

        if lang not in self.langs: self.langs[lang] = { }

        temp = self.langs[lang]

        for x in path:
            if x not in temp:
                temp[x] = { }
            temp = temp[x]
        temp[key] = value


    def traducible( self, lang, path, key ):
        temp = self.langs[lang]

        for x in path:
            temp = temp[x]
        return temp[key]


    def traducir( self, path, key, id_usuario = None ):
        if not id_usuario: lang = self.lang
        else: lang = self.lang

        return self.traducible( lang, path, key )


    def __importar_lang__( self, file ):
        with open( os.path.join( *file ), "r", encoding="utf-8" ) as langfile:
            value = None
            key = None
            for linea in langfile:
                if linea[0] == "#" and value != None:
                    c = slice(1,-1)
                    self.add_to_langs( [file[-1]]+file[c]+[key], value[:-1] )
                if linea[0] == "#": value = ""; key = linea[1:-1]
                else: value += linea
            self.add_to_langs( [file[-1]]+file[c]+[key], value[:-1] )


    def __importar_langs__( self ):
        files = dict( [(x[0], x[2]) for x in os.walk("langs") if len(x[2]) ] )
        for langfile in [ x.split("/") + [y] for x in files for y in files[x]]:
            self.__importar_lang__( langfile )


    @commands.hybrid_command()
    @commands.has_permissions( manage_messages=True )
    async def idioma( self, ctx, idioma ):
        if idioma in self.langs:
            self.lang = idioma
            await ctx.send( self.traducir( ["traducibles"], "cambio_exito" ) )
        else:
            await ctx.send( self.traducir( ["traducibles"], "cambio_fallo" ) )



async def setup( bot ):
    await bot.add_cog( Translator( bot ) )
