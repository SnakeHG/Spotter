import discord
from discord.ext import commands
import logging
import os
from text_proc import TextEvaluator

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = message.author.display_name 
    content = message.content

    print(f'{username}: {content}')


# client.run(TOKEN)

eval = TextEvaluator()
print(eval.evaluate("Hello world!"))
