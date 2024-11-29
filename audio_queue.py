class AudioQueue:
    def __init__(self):
        # Dictionary to hold queues for each guild
        self.queues = {}

    def get_queue(self, guild_id):
        """
        Returns a list of all songs in the queue for the specified guild.
        """
        return self.queues.get(guild_id, [])

    def add_to_queue(self, guild_id, song_data):
        """
        Adds a song to the queue for the specified guild.
        """
        if guild_id not in self.queues:
            self.queues[guild_id] = []  # Initialize queue if it doesn't exist
        self.queues[guild_id].append(song_data)

    def get_next_in_queue(self, guild_id):
        """
        Removes and returns the next song from the queue for the specified guild.
        Returns None if the queue is empty or does not exist.
        """
        if guild_id in self.queues and self.queues[guild_id]:
            return self.queues[guild_id].pop(0)  # Remove and return the first song
        return None
    
    def clear_queue(self, guild_id):
        """
        Clears music queue for specified guild.
        """
        self.queues[guild_id] = []
