from games.Game import Game
from games.FlagGuesser.FlagGuesser import FlagGuesser
from infra.FlagRepository import FlagRepository

from discord import ChannelType, Thread, TextChannel, DMChannel
from discord.ext.commands import Context, Bot

from datetime import datetime
from typing import Optional


class GameHandler():
	def __init__(self, bot: Bot) -> None:
		self.games_by_channel = dict[int,dict[int, Game]]()
		self.games_by_dm = dict[int, Game]()
		self.bot = bot

		self.flagRepo = FlagRepository()
	
	
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
	

	def _add_in_channel(self, channel_id: int, thread_id: int, game: Game) -> None:
		if not channel_id in self.games_by_channel:
			self.games_by_channel[channel_id] = {}

		if thread_id in self.games_by_channel[channel_id]:
			raise Exception("There is already a game in this thread.")
		else:
			self.games_by_channel[channel_id][thread_id] = game


	def _add_in_dm(self, channel_id: int, game: Game) -> None:
		if channel_id in self.games_by_dm: # only one game at a time in DMs
			old_game = self.games_by_dm[channel_id]
			if old_game and old_game.has_started and not old_game.has_ended:
				raise Exception("There is already an ongoing game here!")
			else:
				del self.games_by_dm[channel_id]
		
		self.games_by_dm[channel_id] = game
	

	def _remove_game(self, game: Game):
		self._remove(game.thread.parent_id, game.thread.id)


	def _remove(self, channel_id: int, thread_id: int) -> None:
		if not channel_id in self.games_by_channel:
			raise Exception("There is no game in this channel, or it has ended already.")
		
		elif not thread_id in self.games_by_channel[channel_id]:
			raise Exception("There is no game in this thread, or it has ended already.")
		else:
			del self.games_by_channel[channel_id][thread_id]


	def _get_from_thread(self, channel_id: int, thread_id: int) -> Optional[Game]:
		if not channel_id in self.games_by_channel:
			return None
		elif not thread_id in self.games_by_channel[channel_id]:
			return None
		else:
			return self.games_by_channel[channel_id][thread_id]
	

	def _get_from_dm(self, channel_id) -> Optional[Game]:
		return self.games_by_dm.get(channel_id, None)
			

	def _get_finished_game_in_channels(self, include_artefacts: bool = True) -> list[Game]:
		"""
		Return all the games from channels that has ended
		if artefacts is True, then games that hasn't started are also returned
		"""
		out = []
		for channel_id in self.games_by_channel:
			for thread_id, game in self.games_by_channel[channel_id].items():
				if game.has_ended or (include_artefacts and not game.has_started):
					out.append(game)
		return out


	def _clear(self) -> None:
		"""
		Remove all finished games (from channels) from gameHandler
		"""
		for game in self._get_finished_game_in_channels():
			self._remove_game(game)


	async def _delete_thread(self, thread: Thread) -> None:
		if thread:
			if thread.owner == self.bot.user:
				try:
					await thread.delete()
				except Exception as e:
					print(e)
					await thread.send("This thread cannot be deleted ?")
			else:
				await thread.send("Sorry, I only delete threads that I created !")


	async def _delete(self, thread: Thread) -> None:
		game =  self._get_from_thread(thread.parent_id, thread.id)
		if game:
			if not game.has_ended:
				await game.end()
			self._remove_game(game)
		await self._delete_thread(thread)


	async def delete(self, ctx: Context) -> None:
		"""
		Delete the thread of a game
		"""
		if type(ctx.channel) == Thread:
			await self._delete(ctx.channel)
			self._clear()
		else:
			await ctx.send("This command can be used only in the thread of a game.")


	async def delete_all(self, ctx: Context) -> None:
		"""
		Delete all the threads of a channel that are associated to a game.
		"""
		if type(ctx.channel) == TextChannel:
			count = 0
			for thread in ctx.channel.threads:
				if thread.owner == self.bot.user:
					count += 1
					await self._delete(thread)
			failed = [thread for thread in ctx.channel.threads if thread.owner == self.bot.user]
			count_failed = len(failed)
			self._clear()
			if count_failed == 0:
				await ctx.send(f"All game-threads have been removed ! ({count} thread{'s' if count > 0 else ''} deleted)")
			else:
				await ctx.send(f"{count - count_failed}/{count} thread{'s' if count - count_failed > 0 else ''} deleted. Here are the non-deleted threads:")
				for thread in failed:
					await ctx.send(thread.jump_url)
		else:
			ctx.send("This command can be used only in text channel.")


	async def new_game(self, ctx: Context, game_name: str, *args) -> None:
		"""
		Create a new game, either from a Text Channel or a DM
		"""		
		type_channel = type(ctx.channel)
		if not type_channel in {ChannelType, DMChannel}:
			await ctx.send("Games can only be created in Text Channel or in DM !")
			return

		game_name = game_name.lower()
		if game_name == "flag" or game_name == "flagGuesser":
			title = f"{FlagGuesser.name} - {datetime.now()}"
			max_arguments = 2
			if len(args) > max_arguments:
				args = args[0:max_arguments]
			try:
				game = FlagGuesser(title, self.flagRepo, *args)
				if type_channel == TextChannel:
					thread = await self._create_thread(ctx.channel, title)
					game.set_thread(thread)
					self._add_in_channel(ctx.channel.id, thread.id, game)
				elif type_channel == DMChannel:
					game.set_thread(ctx.channel)
					self._add_in_dm(ctx.channel.id, game)
				else:
					raise Exception(f"This error should not occur. The channel type is {type_channel}")
				
				await game.start()
			except Exception as e:
				await ctx.send(f"{e}")

		else:
			await ctx.send(f"No game with the name {game_name} found.")


	def get_game(self, channel: Thread | DMChannel) -> Optional[Game]:
		if type(channel) == Thread:
			return self._get_from_thread(channel.parent_id, channel.id)
		elif type(channel) == DMChannel:
			return self._get_from_dm(channel.id)
			

	async def play(self, ctx: Context, *args) -> None:
		game = self.get_game(ctx.channel)

		if game and not game.has_ended:
			await game.play(ctx, *args)
		else:
			await ctx.send("There is no game here :eyes:.")


	async def end_game(self, ctx: Context):
		game = self.get_game(ctx.channel)

		if game and not game.has_ended:
			await game.end()


	async def end_all(self, include_dm: bool = False):
		"""
		End all games that are in Threads
		include_dm (default: False): end also games in DMs
		"""
		for channel_id in self.games_by_channel:
			for thread_id, game in self.games_by_channel[channel_id].items():
				if game.has_started and not game.has_ended:
					await game.end()

		if include_dm:
			for channel_id, game in self.games_by_dm.items():
				if game.has_started and not game.has_ended:
					await game.end()


	def get_all_games_in_channels(self) -> dict[int, dict[int, Game]]:
		return self.games_by_channel