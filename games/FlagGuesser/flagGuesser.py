from unidecode import unidecode
from games.Game import Game
from discord import Thread, File
from discord.ext.commands import Context
import io
import aiohttp
import json
import random

FLAGPEDIA_URL = "https://flagcdn.com/192x144"

EASY, HARD, US = "easy", "hard", "us"
FRENCH, ENGLISH = "fr", "en"

class FlagGuesser(Game):
	name = "Guess the flag"
	allowed_difficulties = set([EASY])
	allowed_languages = set([FRENCH])
	thread = None
	attempt_count = 0
	winner = None

	def __init__(self, title: str, difficulty=EASY, language=FRENCH) -> None:
		if not difficulty in self.allowed_difficulties:
			raise Exception(f"This difficulty is not available. Here are the allowed difficulties: {', '.join(self.allowed_difficulties)}")
		if not language in self.allowed_languages:
			raise Exception(f"This language is not available. Here are the allowed languages: {', '.join(self.allowed_languages)}")
		self.title = title
		self.difficulty = difficulty
		self.language = language

	def set_thread(self, thread: Thread) -> None:
		self.thread = thread

	async def start(self):
		self.has_started = True
		await self.thread.send(f"""
Welcome to ***{self.name}*** !
The goal of this game is for you to find to which country the flag below belongs!
Type `$play "your country"` to try out !
If it is too difficult, type `$end` to get the answer.
For this game, you have to give the name of the country in **French** !
		""")
		country_code = self.get_random_country_code()
		self.answer, all_answers = self.get_answer_and_alt(country_code)
		self.all_answers = self.clean_answers(all_answers)
		self.emoji = self.get_emoji(country_code)
		self.cc = country_code
		await self.send_image(country_code)

	def get_random_country_code(self) -> str:
		with open("./games/FlagGuesser/asset/codes.json", 'r', encoding='utf-8') as file:
			data: dict[str, dict] = json.load(file)
		
		data_keys = list(data.keys())
		if self.difficulty == EASY:
			data_keys = [key for key in data_keys if not data[key]["subCountry"]]
		elif self.difficulty == US:
			data_keys = [key for key in data_keys if data[key]["subCountry"] and data[key]["subCountryOf"] == "us"]
		return random.choice(data_keys)

	def get_answer_and_alt(self, country_code: str) -> list[str]:
		with open(f"./games/FlagGuesser/asset/names_{self.language}.json", 'r', encoding='utf-8') as file:
			names: dict[str, dict] = json.load(file)
		
		main_name = names[country_code]["name"]
		return main_name, [main_name]+names[country_code]["alt"]

	def get_emoji(self, country_code: str):
		with open("./games/FlagGuesser/asset/codes.json", 'r', encoding='utf-8') as file:
			data: dict[str, dict] = json.load(file)
		if not country_code in data:
			raise Exception(f"There is no country with this code {country_code}.")
		if not "emoji" in data[country_code]:
			print(f"No emoji found for {self.answer} ({country_code})")
			return None
		return data[country_code]["emoji"]

	def clean_answers(self, answers: list[str]) -> set[str]:
		return set([clean(answer) for answer in answers])

	async def send_image(self, country_code: str):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{FLAGPEDIA_URL}/{country_code}.png") as resp:
				if resp.status != 200:
					return await self.thread.send('Error when downloading the file...')
				data = io.BytesIO(await resp.read())
				await self.thread.send(file=File(data, 'which_country_is_it.png'))

	async def play(self, ctx: Context, *args):
		test = " ".join(args)
		if len(test) == 0: # no args were given
			await ctx.reply("You have to add the name of a country or sub-country!\nEx: $play France")
			return

		self.attempt_count += 1
		if clean(test) in self.all_answers:
			self.winner = ctx.author
			await ctx.reply(f"Well done {ctx.author.mention}. You found it !", mention_author=False)
			await ctx.message.add_reaction("👍")
			await ctx.message.add_reaction("🎉")
			await self.end()
		else:
			await ctx.reply(f"No! :innocent:")
			await ctx.message.add_reaction("👎")

	async def send_sum_up(self):
		await self.thread.parent.send(self.get_sum_up())
	
	def get_sum_up(self) -> str:
		return f"{self.winner.mention if self.winner else 'No one'} has found {self.answer} {self.emoji if self.emoji else ''} ({self.attempt_count} attempt{'s' if self.attempt_count > 1 else ''}) !"
	
	async def end(self):
		self.has_ended = True
		await self.send_sum_up()


def clean(s: str) -> str:
	s = unidecode(s) 		# transform all accented letters to non-accented letters
	s = s.lower()			# we want the string to be lowercase
	s = s.replace("-", " ") # change hyphens to spaces
	s = str.rstrip(s) 		# remove trailing whitespace characters
	s = str.lstrip(s) 		# remove leading whitespace characters
	# remove all multiple spaces following each other
	s = "".join([s[i] for i in range(len(s)) if i==0 or s[i].isalpha() or (s[i]==" " and s[i-1]!=" ")])
	return s