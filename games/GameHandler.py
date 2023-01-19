from discord import ChannelType, Thread, TextChannel
from discord.ext.commands import Context
from games.Game import Game
from games.FlagGuesser.FlagGuesser import FlagGuesser
from datetime import datetime
from typing import Optional


class GameHandler():
	def __init__(self) -> None:
		self.games_by_channel = dict[int,dict[int, Game]]()
	
	async def _create_thread(self, channel: TextChannel, name: str) -> Thread:
		thread = await channel.create_thread(
			name=name,
			type=ChannelType.public_thread
		)
		return thread

	def _exist(self, channel_id: int) -> bool:
		"""
		Check if there is an ongoing game in the channel
		"""
		if channel_id in self.games_by_channel and len(self.games_by_channel[channel_id]) > 0:
			for thread_id, game in self.games_by_channel[channel_id].items():
				if game.has_started and not game.has_ended:
					return True
		return False
	
	def _clear(self, channel_id: int)  -> None:
		to_remove = []
		if channel_id in self.games_by_channel and len(self.games_by_channel[channel_id]) > 0:
			for thread_id, game in self.games_by_channel[channel_id].items():
				if not game.has_started or game.has_ended: # game hasn't been removed correctly from our gameHandler
					to_remove.append([channel_id, thread_id])
		for channel_id, thread_id in to_remove:
			self._remove(channel_id, thread_id)

	def _add(self, channel_id: int, thread_id: int, game: Game) -> None:
		if not channel_id in self.games_by_channel:
			self.games_by_channel[channel_id] = {}

		if thread_id in self.games_by_channel[channel_id]:
			raise Exception("There is already a game in this thread.")
		else:
			self.games_by_channel[channel_id][thread_id] = game
	
	def _remove(self, channel_id: int, thread_id: int) -> None:
		if not channel_id in self.games_by_channel:
			raise Exception("There is no game in this channel, or it has ended already.")
		
		elif not thread_id in self.games_by_channel[channel_id]:
			raise Exception("There is no game in this thread, or it has ended already.")
		else:
			del self.games_by_channel[channel_id][thread_id]

	def clear(self, ctx):
		self._clear(ctx.channel.id)

	async def new_game(self, ctx: Context, game_name: str, *args) -> None:
		if type(ctx.channel) != TextChannel:
			await ctx.send("Games can only be created in Text Channel !")
			return
		
		channel_id = ctx.channel.id
		self._clear(channel_id) # remove any artefact such as finished game still in the dict
		if self._exist(channel_id):
			await ctx.send("There is already an ongoing game in this channel !")
			return

		game_name = game_name.lower()
		if game_name == "flag" or game_name == "flagGuesser":
			title = f"{FlagGuesser.name} - {datetime.now()}"
			max_arguments = 2
			if len(args) > max_arguments:
				args = args[0:max_arguments]
			try:
				game = FlagGuesser(title, *args)
				thread = await self._create_thread(ctx.channel, title)
				game.set_thread(thread)

				self._add(channel_id, thread.id, game)
				await game.start()
			except Exception as e:
				await ctx.send(f"{e}")

		else:
			await ctx.send(f"No game with the name {game_name} found.")

	async def play(self, ctx: Context, *args) -> None:
		if type(ctx.channel) == Thread:
			thread: Thread = ctx.channel
			channel_id = thread.parent_id

			game = self.get(channel_id, thread.id)
			if game:
				await game.play(ctx, *args)
			else:
				await ctx.send("There is no game here :eyes:.")

	async def end_game(self, ctx: Context):
		if type(ctx.channel) == Thread:
			thread: Thread = ctx.channel
			channel_id = thread.parent_id

			game = self.get(channel_id, thread.id)
			if game and not game.has_ended:
				await game.end_game()


	def get(self, channel_id: int, thread_id: int) -> Optional[Game]:
		if not channel_id in self.games_by_channel:
			return None
		elif not thread_id in self.games_by_channel[channel_id]:
			return None
		else:
			return self.games_by_channel[channel_id][thread_id]
		
	def get_all(self) -> dict[int, dict[int, Game]]:
		return self.games_by_channel