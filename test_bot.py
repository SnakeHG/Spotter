import discord
from discord.ext import commands
from discord.utils import oauth_url
from discord import Permissions
import logging
import os
from text_proc import TextEvaluator
from safe_browsing import SafeBrowsingChecker, extract_urls
from dotenv import load_dotenv

load_dotenv()

#TOKENS FROM ENV FILE
TOKEN = os.getenv("discord_token")
GOOGLE_API_KEY = os.getenv("google_token")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Safe Browsing checker
url_checker = SafeBrowsingChecker(GOOGLE_API_KEY)

@bot.command()
async def invite(ctx):
    perms = Permissions(send_messages=True, read_messages=True)
    invite_url = oauth_url(
        bot.user.id,
        permissions=perms,
        scopes=("bot", "applications.commands")
    )
    await ctx.send(f"Invite me using this link:\n{invite_url}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    
    username = message.author.display_name 
    content = message.content

    urls = extract_urls(content)
    if urls:
        for url in urls:
            is_safe, threat_types = url_checker.check_url(url)
            
            if is_safe == False:  # Malicious URL detected
                await message.delete()
                threat_list = ", ".join(threat_types)
                warning = await message.channel.send(
                    f"⚠️ {username}, your message contained a malicious link and was removed.\n"
                    f"Threat types: {threat_list}"
                )
                print(f"Blocked malicious URL from {username}: {url} ({threat_list})")
                return
            elif is_safe is None:  # API error
                print(f"Warning: Could not check URL {url} (API error)")

    if content == "ban me": # Sample illegal message (replace with function to detect if message should be illegal)
        await message.delete() # deletes the message
        return

    print(f'{username}: {content}')


bot.run(TOKEN)

# eval = TextEvaluator()
# print(eval.evaluate("Hello world!"))
