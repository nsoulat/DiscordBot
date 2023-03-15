import discord
from discord.ext import commands
import datetime
import os
from dotenv import load_dotenv
from games.GameHandler import GameHandler

# import environment variables so they can be caught by os.getenv()
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
GENERAL_CHANNEL_ID = os.getenv("GENERAL_ID")
DEBUG = not (os.getenv("ENV_PROD", "True").lower() in ("true", "1")) # DEBUG is True only if ENV_PROD is not "True" or 1

delimiter = '$' # the bot only react when messages begin with this

# bot permissions
# intents = discord.Intents(274877975552) # see https://discord.com/developers/applications/ to compute the value
intents = discord.Intents(messages=True, message_content=True, guilds=True)

help_command = commands.DefaultHelpCommand(show_parameter_descriptions=False)

bot = commands.Bot(command_prefix=delimiter, intents=intents, help_command=help_command)
gameHandler = GameHandler(bot)

@bot.event
async def on_ready():
	print(f"{datetime.datetime.now()}. Logged as {bot.user}")
	if DEBUG:
		print(f"\n\n/!\ The bot is running in DEBUG MODE\n\n")
	elif GENERAL_CHANNEL_ID:
		try:
			channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
			await channel.send("Hello I'm live <:cute_hehe:947149768814104596>") # use of custom emoji: https://github.com/Rapptz/discord.py/issues/390
		except Exception as e:
			print(f"Error when sending message to channel general: {e}")


@bot.command()
async def hack(ctx, target): # target will be the first word after $hack. Rest of the content is omitted
	"""It may or may not hack the person you target 👀.

	Args:
		target (str): target to hack.
	"""
	await ctx.send(f"I'm hacking {target}! 🐱‍💻")

@bot.command()
async def game(ctx, game = None, *args):
	"""Creates a game.

	Args:
		game (str): Name of the game. Available games are 'flag'.
		*args (Any, optional): Other arguments for the initialization of the game. (see https://github.com/nsoulat/DiscordBot#games ).
	"""
	if game:
		await gameHandler.new_game(ctx, game, *args)

@bot.command(hidden=True)
async def play(ctx, *args):
	"""Command used in games.

	Args:
		*args (Any): Some arguments. see https://github.com/nsoulat/DiscordBot#games.
	"""
	await gameHandler.play(ctx, *args)

@bot.command(hidden=True)
async def end(ctx):
	"""Command used in games.
	
	End the game.
	"""
	await gameHandler.end_game(ctx)

@bot.command()
async def ongoing_games(ctx):
	"""Show ongoing games.

	Lists all the ongoing games (only in Channels and not in DMs) the Bot is holding.
	"""
	count = 0
	text = ""
	for channel_id, value in gameHandler.get_all_games_in_channels().items():
		for thread_id, game in value.items():
			if game.has_started and not game.has_ended:
				count += 1
				text += f"\n{game.title}: {game.thread.jump_url}"
	if count == 0:
		await ctx.send("No ongoing game was found !")
	else:
		await ctx.send(f"{count} game{' was' if count == 1 else 's were'} found:"+text)

@bot.command()
async def delete(ctx):
	"""Delete the thread of a game.
	"""
	await gameHandler.delete(ctx)

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def delete_all(ctx):
	"""Delete all the threads of a channel that has been created by the bot.
	"""
	await gameHandler.delete_all(ctx)

@bot.command(name="thread?")
async def is_thread(ctx):
	"""Check if this is a Thread, Text Channel or DM.
	"""
	type_channel = type(ctx.channel)
	if type_channel == discord.TextChannel:
		await ctx.send("No, this is a Text Channel.")
	elif type_channel == discord.Thread:
		await ctx.send("Yes, this is a Thread !")
	elif type_channel == discord.DMChannel:
		await ctx.send("No, this is a DM channel.")
	else:
		await ctx.send(f"Hum, this is a {type_channel}.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def offline(ctx):
	"""Disconnects the bot from discord.
	"""
	if GENERAL_CHANNEL_ID and not DEBUG:
		try:
			channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
			await channel.send("Bye everyone. I am going to sleep ! <:cute_hehe:947149768814104596>")
		except Exception as e:
			print(f"Error when sending message to channel general: {e}")

	await gameHandler.end_all(include_dm=True)

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