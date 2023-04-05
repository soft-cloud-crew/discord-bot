#!/usr/bin/python

import os
import asyncio

import discord as dis
from discord.ext import commands

import typing as ty
from dotenv import load_dotenv


load_dotenv()
test = True

intents = dis.Intents.default()
intents.members = True ; intents.message_content = True

client = commands.Bot( command_prefix = commands.when_mentioned_or( 's$' ), help_command = None, intents = intents)

@client.event
async def on_ready():
    activity = dis.Activity( name = 'Mindustry', type = dis.ActivityType.playing )
    await client.change_presence( status = dis.Status.idle, activity = activity )

    print( 'logged in as {0.user}'.format( client ) )
    await client.load_extension( 'help' )
    await client.load_extension( 'musica' )
    await client.load_extension( 'economia' )
    await client.tree.sync( )


client.run( os.getenv( 'TOKENTEST' if test else 'TOKEN' ) )
