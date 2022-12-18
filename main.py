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
        albums = results["albums"]["items"]
        
        i=1
        for album in albums:
            print(f"{i}.Album Name: {album['name']}\nFirst Artist Name: {album['artists'][0]['name']}\nSpotify URI: {album['uri']}\n------------------------")
            i+=1

        print(f"retrieved {i} albums related to given album name and artist name, also their spotify uri's to check them on spotify")
        print("So which album do you want to see details of?")
        album_number = int(input("Enter the number of album: "))
        os.system('cls')
        print(f"{i}.Album: " + albums[album_number - 1]["name"])
        print("***********************")
        
        album_id = albums[album_number-1]["id"]
        album_track_results = sp.album_tracks(album_id=album_id)
        all_tracks = album_track_results["items"]
        
        for track in all_tracks:
            print(track["name"])
            artists = track["artists"]
            artist_names = []
            for artist in artists:
                if artist["name"] != artist_name:
                    artist_names.append(artist["name"])
            artist_names_str = ", ".join(artist_names)
            if len(artist_names) > 0:
                print("Other Artists: " + artist_names_str)
        
        print("\nTotal Tracks: ", album["total_tracks"])
        print(total_duration_time(all_tracks))
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
                artists = track["artists"]
                print("All Artists: ", end="")
                artist_names = []
                for artist in artists:
                    if artist["name"] != artist_name:
                        artist_names.append(artist["name"])
                
                track_uri = track["uri"]
                track_details = sp.track(track_uri)
                track_album = track_details["album"]
                
                for artist in track["artists"]:
                    print(artist["name"], end=", ")
                print("\n" + total_duration_time([track]))
                print("Track Album: " + track_album["name"])
                print("Track URI: " + track_uri)
                print(release_date(track_album))
                print(lyrics([track])+ "\n***********************")#!!
                break

    elif selection == "3":
        break
    input("Press Enter to enter again...")
    os.system('cls')