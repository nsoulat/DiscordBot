from abc import ABC, abstractmethod

class Game(ABC):

	has_started = False
	has_ended = False
	
	@property
	@abstractmethod
	def name(self):
		pass

	@abstractmethod
	async def start(self):
		pass