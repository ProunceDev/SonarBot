from constants import *
from interactions import *
from interactions.api.voice.audio import AudioVolume
import asyncio
from Extensions.youtube import youtube_handle
from audio_queue import AudioQueue


class Commands(Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
		self.queue = AudioQueue()
		self.active_players = {}

	@slash_command(
		name="play",
		description="Play a song or playlist from YouTube.",
		options=[
			SlashCommandOption(
				name="link",
				description="The song or playlist to play.",
				type=OptionType.STRING,
				required=True,
			),
		],
	)
	async def play(self, ctx: ComponentContext, link: str):
		await ctx.defer(ephemeral=False)

		if not ctx.author.voice:
			return await ctx.send(
				embed=self.create_embed("Error", "You need to be in a voice channel to use this command.", color=0xFF0000),
				ephemeral=True,
			)

		if not ctx.voice_state:
			await ctx.author.voice.channel.connect(deafened=True)

		link_info = youtube_handle.get_link_info(link)
		if not link_info:
			return await ctx.send(
				embed=self.create_embed("Error", "Could not retrieve song information. Please try again.", color=0xFF0000),
				ephemeral=True,
			)

		for song_data in link_info:
			song_data['requested_by'] = ctx.user.mention
			self.queue.add_to_queue(ctx.guild_id, song_data)

		if not self.has_active_player(ctx.guild_id):
			self.create_player(ctx, ctx.guild_id)

		if ctx.voice_state.paused:
			ctx.voice_state.resume()

		await ctx.send(
			embed=self.create_embed(
				"Added to Queue",
				f"Added {len(link_info)} song(s) to the queue.",
				color=0x00FF00,
			)
			, ephemeral=True
		)

	@slash_command(
		name="join",
		description="Join your current voice channel.",
	)
	async def join(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		if not ctx.author.voice:
			return await ctx.send(
				embed=self.create_embed("Error", "You need to be in a voice channel to use this command.", color=0xFF0000),
				ephemeral=True,
			)

		await ctx.author.voice.channel.connect(deafened=True)
		await ctx.send(embed=self.create_embed("Joined", "Successfully joined your voice channel.", color=0x00FF00), ephemeral=True)

	@slash_command(
		name="pause",
		description="Pause music playback.",
	)
	async def pause(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		if not ctx.voice_state or not ctx.voice_state.playing:
			return await ctx.send(
				embed=self.create_embed("Error", "I am not playing anything right now.", color=0xFF0000),
				ephemeral=True,
			)

		if ctx.voice_state.paused:
			return await ctx.send(
				embed=self.create_embed("Error", "Music is already paused.", color=0xFF0000),
				ephemeral=True,
			)

		await ctx.send(embed=self.create_embed("Paused", "Music playback has been paused.", color=0xFFFF00))
		ctx.voice_state.pause()

	@slash_command(
		name="resume",
		description="Resume music playback.",
	)
	async def resume(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		if not ctx.voice_state or not ctx.voice_state.paused:
			return await ctx.send(
				embed=self.create_embed("Error", "Music is not paused.", color=0xFF0000),
				ephemeral=True,
			)

		await ctx.send(embed=self.create_embed("Resumed", "Music playback has been resumed.", color=0x00FF00))
		ctx.voice_state.resume()

	@slash_command(
		name="stop",
		description="Stop music playback.",
	)
	async def stop(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		if not ctx.voice_state or not ctx.voice_state.playing:
			return await ctx.send(
				embed=self.create_embed("Error", "I am not playing anything right now.", color=0xFF0000),
				ephemeral=True,
			)

		self.queue.clear_queue(ctx.guild_id)
		await ctx.send(embed=self.create_embed("Stopped", "Music playback has been stopped.", color=0xFF0000))
		await ctx.voice_state.stop()

	@slash_command(
		name="skip",
		description="Skip the current song.",
	)
	async def skip(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		if not ctx.voice_state or not ctx.voice_state.playing:
			return await ctx.send(
				embed=self.create_embed("Error", "I am not playing anything to skip.", color=0xFF0000),
				ephemeral=True,
			)

		await ctx.send(embed=self.create_embed("Skipped", "Skipped the current song.", color=0xFFFF00))
		await ctx.voice_state.stop()

	@slash_command(
		name="leave",
		description="Leave the current voice channel.",
	)
	async def leave(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		if not ctx.voice_state:
			return await ctx.send(
				embed=self.create_embed("Error", "I am not in a voice channel.", color=0xFF0000),
				ephemeral=True,
			)

		await ctx.voice_state.disconnect()
		await ctx.send(embed=self.create_embed("Left", "Successfully left the voice channel.", color=0xFF0000))
		
	def convert_seconds(self, seconds):
		minutes = seconds // 60
		remaining_seconds = seconds % 60
		return f"{minutes}:{remaining_seconds:02}"

	@slash_command(
		name="queue",
		description="List all songs in the queue.",
	)
	async def queue(self, ctx: ComponentContext):
		await ctx.defer(ephemeral=False)

		guild_queue = self.queue.get_queue(ctx.guild_id)
		if not guild_queue:
			return await ctx.send(
				embed=self.create_embed("Queue", "The queue is currently empty.", color=0xFFFF00)
			)

		queue_list = "\n".join(
			[f"{idx + 1}. [{song['title']}]({song['url']}) ( Length: {self.convert_seconds(song['length'])} )" for idx, song in enumerate(guild_queue)]
		)
		await ctx.send(
			embed=self.create_embed(
				"Current Queue",
				f"**Songs in the queue:**\n{queue_list}",
				color=0x1DB954,
			)
		)

	def has_active_player(self, guild_id) -> bool:
		return self.active_players.get(guild_id, False)

	async def audio_player(self, ctx, guild_id) -> None:
		next_in_queue = self.queue.get_next_in_queue(guild_id)
		while next_in_queue is not None:
			audio_stream_url = youtube_handle.get_audio_stream_url(next_in_queue['url'])
			if not audio_stream_url:
				next_in_queue = self.queue.get_next_in_queue(guild_id)
				continue

			async def play_audio():
				audio = AudioVolume(audio_stream_url)
				audio.volume = 4.0  # Adjust volume if needed
				await ctx.voice_state.play(audio)

			# Send "Now Playing" embed
			await ctx.channel.send(
				embed=self.create_embed(
					"Now Playing",
					f"[{next_in_queue['title']}]({next_in_queue['url']})\n ( Length: {self.convert_seconds(next_in_queue['length'])} ) Requested by {next_in_queue['requested_by']}",
					color=0x1DB954,
				)
			)

			await play_audio()

			next_in_queue = self.queue.get_next_in_queue(guild_id)

		self.active_players[guild_id] = False

	def create_player(self, ctx, guild_id) -> None:
		self.active_players[guild_id] = True
		asyncio.create_task(self.audio_player(ctx, guild_id))

	@staticmethod
	def create_embed(title, description, color=0xFFFFFF):
		return Embed(title=title, description=description, color=color)
