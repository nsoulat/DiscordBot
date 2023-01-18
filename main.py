import discord
from discord.ext import commands
import datetime
import os
from dotenv import load_dotenv

# import environment variables so they can be caught by os.getenv()
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
GENERAL_CHANNEL_ID = os.getenv("GENERAL_ID")
DEBUG = not (os.getenv("ENV_PROD", "True").lower() in ("true", "1")) # DEBUG is True only if ENV_PROD is not "True" or 1

delimiter = '$' # the bot only react when messages begin with this

# bot permissions
# intents = discord.Intents(274877975552) # see https://discord.com/developers/applications/ to compute the value
intents = discord.Intents(messages=True, message_content=True, guilds=True)

bot = commands.Bot(command_prefix=delimiter, intents=intents)


@bot.event
async def on_ready():
	print(f"{datetime.datetime.now()}. Logged as {bot.user}")
	if DEBUG:
		print(f"\n\n/!\ The bot is running in DEBUG MODE\n\n")
	elif GENERAL_CHANNEL_ID:
		try:
			channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
			await channel.send("Hello I'm live <:cute_hehe:947149768814104596>")
		except Exception as e:
			print(f"Error when sending message to channel general: {e}")


@bot.command()
async def hack(ctx, target): # target will be the first word after $hack. Rest of the content is omitted
	await ctx.send(f"I'm hacking {target}! 🐱‍💻")


@bot.command()
@commands.has_permissions(administrator=True)
async def offline(ctx):
	if GENERAL_CHANNEL_ID and not DEBUG:
		try:
			channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
			await channel.send("Bye everyone. I am going to sleep ! <:cute_hehe:947149768814104596>")
		except Exception as e:
			print(f"Error when sending message to channel general: {e}")

	# this will close the connection to discord but raises an error on Windows after closing the connection (https://github.com/Rapptz/discord.py/issues/5209)
	await bot.close()


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return # the bot do not react to its own message

	if message.content.lower() == "good bot":
		await message.channel.send(f"Me ? Thank you (๑>ᴗ<๑)")
	
	await bot.process_commands(message) # check other bot.command()


bot.run(BOT_TOKEN)