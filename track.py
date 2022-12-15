import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
# Spotify API erişim anahtarlarınızı buraya girin
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# İstediğiniz şarkının adını ve sanatçısını buraya girin
track_name = "Without Me"
artist_name = "Halsey"

# Spotify API'yi kullanarak şarkıyı arayın
results = sp.search(q=f'track:"{track_name}" artist:"{artist_name}"', type="track")
items = results["tracks"]["items"]
track = items[0]

# Şarkı bilgilerini alın
song_name = track["name"]
album_name = track["album"]["name"]
release_date = track["album"]["release_date"]
duration = track["duration_ms"]
spotify_uri = track["uri"]

# Varsa, şarkı sözlerini alın
lyrics = None
if "lyrics" in track:
    lyrics = track["lyrics"]

# Şarkı bilgilerini ekrana yazdırın
print("Şarkı:", song_name)
print("Albüm:", album_name)
print("Çıkış Tarihi:", release_date)
print("Çalma Süresi (ms):", duration)
print("Spotify URI:", spotify_uri)
print("Sözler:", lyrics)
