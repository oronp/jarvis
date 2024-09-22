import spotipy
from spotipy.oauth2 import SpotifyOAuth

from action_handling.spotify_api.spotify_api_config import SpotifyApiConfig
from utils.logger import JarvisLogger

logger = JarvisLogger('SpotifyAPI')
config = SpotifyApiConfig()


class SpotifyApiObject:
    def __init__(self, selected_device: int = None) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIFY_CLIENT_ID,
                                                            client_secret=config.SPOTIFY_CLIENT_SECRET,
                                                            redirect_uri=config.SPOTIFY_REDIRECT_URI,
                                                            scope=config.STR_SCOPE))

        self.devices: list[dict] = self.get_devices()
        device_index = selected_device or 0
        self.selected_device = self.devices[device_index]['id']

    def get_devices(self) -> list:
        """Function to get user's devices (you need a device active to control playback)"""
        devices_dict = self.sp.devices()
        logger.info(f"Available devices: {[_device['name'] for _device in devices_dict['devices']]}")
        return devices_dict['devices']

    def play_song(self, song_uri: str) -> None:
        """Function to play a song by URI on a specific device"""
        if self.selected_device:
            self.sp.start_playback(device_id=self.selected_device, uris=[song_uri])
        else:
            self.sp.start_playback(uris=[song_uri])

    def search_song(self, song_name: str) -> str:
        results = self.sp.search(q=song_name, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            song_uri = track['uri']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            logger.info(f"Found song: {song_name} by {artist_name}")
            return song_uri
        else:
            logger.info("No results found.")
            return None
