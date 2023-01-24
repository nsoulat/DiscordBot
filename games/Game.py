from abc import ABC, abstractmethod
from discord import Thread

class Game(ABC):
	def __init__(self):
		self.has_started: bool = False
		self.has_ended: bool = False

	def set_thread(self, thread: Thread):
		self.thread: Thread = thread
	
	@property
	@abstractmethod
	def name(self) -> str:
		pass

	@abstractmethod
	async def start(self):
		pass

	@abstractmethod
	async def play(self, ctx, *args):
		pass

	@abstractmethod
	async def end(self):
		pass