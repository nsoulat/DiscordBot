from unidecode import unidecode
from games.Game import Game
from discord import Thread

class FlagGuesser(Game):
	name = "Guess the flag"

	def __init__(self, thread: Thread, title) -> None:
		self.thread = thread
		self.title = title

	async def start(self):
		self.has_started = True
		await self.thread.send(f"Welcome to {self.name} !")


def clean(s: str) -> str:
	s = unidecode(s) 		# transform all accented letters to non-accented letters
	s = s.lower()			# we want the string to be lowercase
	s = s.replace("-", " ") # change hyphens to spaces
	s = str.rstrip(s) 		# remove trailing whitespace characters
	s = str.lstrip(s) 		# remove leading whitespace characters
	# remove all multiple spaces following each other
	s = "".join([s[i] for i in range(len(s)) if i==0 or s[i].isalpha() or (s[i]==" " and s[i-1]!=" ")])
	return s