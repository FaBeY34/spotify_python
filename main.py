import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def total_duration_time(tracks):
    total_duration_ms = 0
    for track in tracks:
        total_duration_ms += track["duration_ms"]
    total_duration_minutes = int((total_duration_ms / 1000 / 60) % 60)
    total_duration_hours = int((total_duration_ms / 1000 / 60) / 60)
    total_duration_seconds = int((total_duration_ms / 1000) % 60)   
    if total_duration_hours == 0:
        return "Run Time: " + str(total_duration_minutes) + " min " + str(total_duration_seconds) + " sec"
    return "Run Time: " + str(total_duration_hours) + " hr " + str(total_duration_minutes) + " min"

def release_date(item):
    release_date = str(item["release_date"])
    date_elements = release_date.split("-")
    if len(date_elements) == 1:
        return "Release Date: " + date_elements[0]
    date_object = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d %B %Y")
    return "Release Date: " + str(date_object)

def lyrics(item):
    if "lyrics" not in item:
        return "Lyrics: None\n"
    return "Lyrics:\n" + item["lyrics"]

while True:
    print("*********************** Spotify API Program ***********************")
    print("1- Album Name, Track List and Album Details")
    print("2- Track Name and Track Details")
    selection = input("3- Exit\n")
    
    if selection == "1":
        os.system('cls')
        album_name = input("Enter Album Name (case sensitive): ")
        artist_name = input("Enter Artist Name (case sensitive): ")
        print("")
        # Query to get album id
        results = sp.search(q=f'album:"{album_name}" artist:"{artist_name}"', type="album")
        print(results)
        albums = results["albums"]["items"]

        # Check if album exists
        for album in albums:
            # Check if album name and artist name match
            if album["name"] == album_name:
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
                        print(total_duration_time(tracks))
                        print("Spotify URI: " + album["uri"])
                        print(release_date(album) + "\n***********************")

    elif selection == "2":
        os.system('cls')
        track_name = input("Enter Track Name (case sensitive): ")
        artist_name = input("Enter Artist Name (case sensitive): ")
        print("")
        #!!
        results = sp.search(q=f'track:"{track_name}" artist:"{artist_name}"', type="track")
        tracks = results["tracks"]["items"]

        for track in tracks:
            if track["name"] == track_name:
                track_uri = track["uri"]
                track_details = sp.track(track_uri)
                track_album = track_details["album"]

                print(total_duration_time([track]))
                print("Track Album: " + track_album["name"])
                print("Track URI: " + track_uri)
                print(release_date(track_album))
                print(lyrics([track])+ "\n***********************")#!!
                break

    elif selection == "3":
        break
    input("Press Enter to enter again...")
    os.system('cls')