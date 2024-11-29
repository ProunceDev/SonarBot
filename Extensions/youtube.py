import yt_dlp
from interactions import *
from pytube import Playlist, YouTube

class Youtube(Extension):
    pass # Just for handling by interactions.py cogs.

class YouTubeHandler():
    def get_playlist_info(self, link):
        """Returns a list of video titles and URLs from a YouTube playlist using pytube."""
        playlist_info = []
        try:
            playlist = Playlist(link)
            for video in playlist.videos:
                try:
                    playlist_info.append({'title': video.title, 'url': video.watch_url, 'length': video.length})
                except:
                    pass

        except Exception as e:
            pass
            
        return playlist_info

    def get_video_title(self, video_url):
        try:
            yt = YouTube(video_url)
            return [{'title': yt.title, 'url': yt.watch_url, 'length': yt.length}]
        except Exception as e:
            return None

    def get_audio_stream_url(self, video_url):
        """Extracts the direct audio stream URL using yt_dlp."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info['url'] if 'url' in info else None

    def get_link_info(self, link):

        playlist_info = self.get_playlist_info(link)

        if not playlist_info:
            playlist_info = self.get_video_title(link)

        return playlist_info

youtube_handle = YouTubeHandler()
