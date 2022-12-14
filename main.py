import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

load_dotenv()
# API authentication
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Spotify API connection
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# Get input from user
while True:
    album_name = input("Enter Album Name (case sensitive) : ")
    artist_name = input("Enter Artist Name (case sensitive) : ")
    print("")
    # Query to get album id
    results = sp.search(q=f'album:"{album_name}" artist:"{artist_name}"', type="album")
    albums = results["albums"]["items"]
    # Check if album exists
    for album in albums:
        # Check if album name and artist name match
        if album['name'] == album_name:
            for artist in album["artists"]:
                if artist["name"] == artist_name:
                    album_id = album["id"]
                    results = sp.album_tracks(album_id=album_id)
                    tracks = results["items"]
                    # Track list printing
                    total_track_number = 0
                    for track in tracks:
                        total_track_number = total_track_number + 1
                        print(track["name"])
                        artists = track["artists"]
                        artist_names = []
                        for artist in artists:
                            if artist["name"] != artist_name:
                                artist_names.append(artist["name"])
                        artist_names_str = ", ".join(artist_names)
                        if len(artist_names) > 0:
                            print("Other Artists: " + artist_names_str)

                    print("\nTotal Tracks: ", total_track_number)
                    # Album total duration calculation
                    total_duration_ms = 0
                    for track in tracks:
                        total_duration_ms += track["duration_ms"]
                    total_duration_minutes = int((total_duration_ms / 1000 / 60) % 60)
                    total_duration_hours = int((total_duration_ms / 1000 / 60) / 60)
                    total_duration_seconds = int((total_duration_ms / 1000) % 60)
    
                    if total_duration_hours == 0:
                        print("Run Time: " + str(total_duration_minutes) + " min " + str(total_duration_seconds) + " sec")
                    else:
                        print("Run Time: " + str(total_duration_hours) + " hr " + str(total_duration_minutes) + " min")
                    # Spotify URI printing
                    spotify_uri = album["uri"]
                    print("Spotify URI: " + spotify_uri)
                    # Print album release date
                    release_date = str(album["release_date"])
                    date_elements = release_date.split("-")
                    if len(date_elements) == 1:
                        print("Release Date: " + date_elements[0])
                    else:
                        date_object = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d %B %Y")
                        print("Release Date: " + str(date_object) + "\n***********************")
    # continue until user closes the window or presses CTRL + C
    input("\nPress Enter to enter again...\nto exit, close the window or press CTRL + C")
    os.system('cls')