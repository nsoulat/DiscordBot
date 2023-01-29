from games.Game import Game
from domain.Constants import LANGUAGE, DIFFICULTY, CONTINENT
from infra.FlagRepository import FlagRepository

from discord import Thread, File, DMChannel
from discord.ext.commands import Context

from unidecode import unidecode
import io
import aiohttp
import random

FLAGPEDIA_URL = "https://flagcdn.com/192x144"


class FlagGuesser(Game):
	name = "Guess the flag"
	allowed_difficulties = set([DIFFICULTY.EASY, DIFFICULTY.HARD, DIFFICULTY.US, DIFFICULTY.EUROPE])
	allowed_languages = set([LANGUAGE.FRENCH, LANGUAGE.ENGLISH])

	def __init__(self, title: str, flagRepository: FlagRepository, difficulty=DIFFICULTY.EASY, language=LANGUAGE.FRENCH) -> None:
		super().__init__()
		if not difficulty in self.allowed_difficulties:
			raise Exception(f"This difficulty is not available. Here are the allowed difficulties: {', '.join(self.allowed_difficulties)}")
		if not language in self.allowed_languages:
			raise Exception(f"This language is not available. Here are the allowed languages: {', '.join(self.allowed_languages)}")
		self.title = title
		self.difficulty = difficulty
		self.language = language
		self.flagRepository = flagRepository
		self.thread: Thread | DMChannel = None
		self.attempt_count = 0
		self.winner = None

	async def start(self):
		self.has_started = True
		await self.thread.send(f"""
Welcome to ***{self.name}*** !
The goal of this game is for you to find to which country the flag below belongs!
Type `$play "your country"` to try out !
If it is too difficult, type `$end` to get the answer.
For this game, you have to give the name of the country in **{LANGUAGE.trad(self.language)}** !
		""")
		self.country = self._get_random_country()
		self._set_answers()
		await self.send_image(self.country.code)

	def _get_random_country(self):
		countries = []
		if self.difficulty == DIFFICULTY.US:
			countries = self.flagRepository.get_US_regions()
		else:
			include_subCountry = self.difficulty in { DIFFICULTY.HARD }
			continent = None
			if self.difficulty == DIFFICULTY.EUROPE:
				continent = CONTINENT.EUROPE
			countries = self.flagRepository.get_all_countries(include_subCountry, continent)
		return random.choice(countries)

	def _set_answers(self) -> None:
		"""
		'Clean' the names of the country to better check when players try some names
		"""
		self.all_answers = set([clean(answer) for answer in self.country.names[self.language].all_names])

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
		if type(self.thread) == Thread:
			await self.thread.parent.send(self.get_sum_up())
		elif type(self.thread) == DMChannel:
			await self.thread.send(self.get_sum_up())

	def get_sum_up(self) -> str:
		return f"{self.winner.mention if self.winner else 'No one'} has found {self.country.names[self.language].main} {self.country.emoji if self.country.emoji else ''} ({self.attempt_count} attempt{'s' if self.attempt_count > 1 else ''}) !"
	
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