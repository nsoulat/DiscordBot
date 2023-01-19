from abc import ABC, abstractmethod
from discord import Thread

class Game(ABC):

	has_started = False
	has_ended = False
	
	@property
	@abstractmethod
	def name(self) -> str:
		pass

	@property
	@abstractmethod
	def thread(self) -> Thread:
		pass

	@abstractmethod
	async def start(self):
		pass

	@abstractmethod
	async def end_game(self):
		pass