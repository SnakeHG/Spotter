import discord
from discord.ext import commands
import logging
import os
from text_proc import TextEvaluator
from safe_browsing import SafeBrowsingChecker, extract_urls
from dotenv import load_dotenv
import asyncio

load_dotenv()

#TOKENS FROM ENV FILE
TOKEN = os.getenv("discord_token")
GOOGLE_API_KEY = os.getenv("google_token")
HF_TOKEN = os.getenv("HF_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# Initialize Safe Browsing checker
url_checker = SafeBrowsingChecker(GOOGLE_API_KEY)

# Initialize text evaluator (uses HF_TOKEN from environment by default)
text_evaluator = TextEvaluator()

# Filtering thresholds (tunable)
TOXIC_THRESHOLD = 0.8
PHISH_THRESHOLD = 0.7

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = message.author.display_name 
    content = message.content
    # First: evaluate the text content for toxicity / phishing using text_proc
    try:
        loop = asyncio.get_running_loop()
        toxic_score_struct, phish_score = await loop.run_in_executor(None, text_evaluator.evaluate, content)
    except Exception as e:
        # If evaluation fails, log and continue with URL checks
        print(f"Text evaluation error: {e}")
        toxic_score_struct, phish_score = 0.0, 0.0

    # Act on evaluation results
    if phish_score >= PHISH_THRESHOLD:
        await message.delete()
        await message.channel.send(
            f"⚠️ {username}, your message was removed: suspected phishing (score={phish_score:.2f})."
        )
        print(f"Removed suspected phishing message from {username}: score={phish_score:.2f}")
        return

    for score_struct in toxic_score_struct:
        label = score_struct.label
        score = score_struct.score

        if score >= TOXIC_THRESHOLD:
            await message.delete()
            await message.channel.send(
                f"⚠️ {username}, your message violated community standards (reason={label}, toxicity={score:.2f}) and was removed."
            )
        print(f"Removed toxic message from {username}: score={score:.2f}, reason={label}")
        return

    # Then check extracted URLs (existing behavior)
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


client.run(TOKEN)

# eval = TextEvaluator()
# print(eval.evaluate("Hello world!"))
