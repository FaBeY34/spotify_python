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
    total_duration_minutes = int((total_duration_ms / 1000) / 60)
    total_duration_seconds = int((total_duration_ms / 1000) % 60)   
    return "Run Time: " + str(total_duration_minutes) + ":" + str(total_duration_seconds)

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

def get_results(item_name, artist_name, type):
    results = sp.search(q=f'{type}:"{item_name}" artist:"{artist_name}"', type=type)
    items = results[type + "s"]["items"]
    if items == []:
        print("No Results Found")
        return
    i=1
    for item in items:
        print(f"{i}.Album Name: {item['name']}\nFirst Artist Name: {item['artists'][0]['name']}\nSpotify URI: {item['uri']}\n------------------------")
        i+=1
    
    print(f"retrieved {i - 1} {type}s related to given {type} name and artist name, also their spotify uri's to check them on spotify\n------------------------")
    print(f"so which {type} do you want to see details of?")

    item_number = int(input(f"Enter the number of {type}: "))
    os.system('cls')
    
    print(f"{items[item_number - 1]['name']}")
    print(f"{items[item_number - 1]['artists'][0]['name']}")
    print("***********************")

    selected_item = items[item_number - 1] #selected item
    item_id = items[item_number - 1]["id"] #for album
    item_uri = items[item_number - 1]["uri"] #for track and album

    if type == "album":
        all_results = sp.album_tracks(item_id)
        all_tracks = all_results["items"]
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
        print("\nTotal Tracks: ", all_results["total"])
        print(total_duration_time(all_tracks))
        print(release_date(selected_item) + "\n***********************")

    elif type == "track":
        track_details = sp.track(item_uri)
        track_album = track_details["album"]
        print("Artists: ", end="")
        for artist in selected_item["artists"]:
            print(artist["name"], end=", ")
        print("\n" + total_duration_time([selected_item]))
        print("Album Name: " + track_album["name"])
        print(release_date(track_album) + "\n***********************")

    print("Spotify URI: " + item_uri)


while True:
    print("*********************** Spotify API Program ***********************")
    print("Do not enter full album or track name for better selection\n------------------------")
    print("1- Album Name, Track List and Album Details")
    print("2- Track Name and Track Details")
    selection = input("3- Exit\n")
    
    if selection == "1":
        os.system('cls')
        album_name = input("Enter Album Name (with few characters): ")
        artist_name = input("Enter Artist Name (case sensitive): ")
        print("")
        get_results(album_name, artist_name, "album")

    elif selection == "2":
        os.system('cls')
        track_name = input("Enter Track Name (with few characters): ")
        artist_name = input("Enter Artist Name (case sensitive): ")
        print("")
        get_results(track_name, artist_name, "track")
        # print(lyrics([track])+ "\n***********************")#!!

    elif selection == "3":
        break

    input("Press Enter to enter again...")
    os.system('cls')