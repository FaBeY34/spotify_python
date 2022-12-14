import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# API anahtarınızı buraya girin
client_id = "b85b312b81054962b3e48f2bf5505224"
client_secret = "79782237097e4bbbbb949718061aa1db"

# Spotify API'ye bağlanmak için gerekli ayarlar
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# artist_name = "Adele"
# album_name = "25"

# results = sp.search(q='artist:' + artist_name, type='album')
# albums = results['albums']['items']

#get input from user
while True:
    album_name = input("Enter Album Name (case sensitive) : ")
    artist_name = input("Enter Artist Name (case sensitive) : ")
    print("")
    # girilen albümün ID'sini bulmak için sorgu
    results = sp.search(q=f'album:"{album_name}" artist:"{artist_name}"', type="album")
    albums = results["albums"]["items"]
    # Eğer birden fazla sonuç döndürülürse, ilk sonucu kullanma
    for album in albums:
        if album['name'] == album_name:
            for artist in album["artists"]:
                if artist["name"] == artist_name:
                    album_id = album["id"]
                    results = sp.album_tracks(album_id=album_id)
                    tracks = results["items"]
    
                    total_track_number = 0
                    for track in tracks:
                        total_track_number = total_track_number + 1
                        print(track["name"])
                        # Şarkının söyleyen sanatçılarının isimlerini çekme
                        artists = track["artists"]
                        artist_names = []
                        for artist in artists:
                            if artist["name"] != artist_name:
                                artist_names.append(artist["name"])
                        artist_names_str = ", ".join(artist_names)
                        if len(artist_names) > 0:
                            print("Other Artists: " + artist_names_str)

                    print("\nTotal Tracks: ", total_track_number)
    
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
                    spotify_uri = album["uri"]
                    print("Spotify URI: " + spotify_uri)
    
                    # Albüm çıkış tarihini yazdırma
                    release_date = str(album["release_date"])
                    date_elements = release_date.split("-")
                    if len(date_elements) == 1:
                        print("Release Date: " + date_elements[0])
                    else:
                        date_object = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d %B %Y")
                        print("Release Date: " + str(date_object) + "\n***********************")
                
    input("\nPress Enter to enter again...\nto exit, close the window or press CTRL + C")
    os.system('cls')
    # if len(albums) > 0:
    #     album = albums[0]
    #     album_id = album["id"]

    #     for i in range(len(albums)):
    #         if albums[i]["name"] == album_name:
    #             album = albums[i]
    #             album_id = album["id"]
    #             break

        # Albüm içerisindeki şarkıları çekmek için sorgu
        # results = sp.album_tracks(album_id=album_id)
        # tracks = results["items"]
        # Çekilen şarkı listesini ekrana yazdırma
        # total_track_number = 0
        # for track in tracks:
        #     total_track_number = total_track_number + 1
        #     print(track["name"])
        #     # Şarkının söyleyen sanatçılarının isimlerini çekme
        #     artists = track["artists"]
        #     artist_names = []
        #     for artist in artists:
        #         if artist["name"] != artist_name:
        #             artist_names.append(artist["name"])
        #     artist_names_str = ", ".join(artist_names)
        #     if len(artist_names) > 0:
        #         print("Other Artists: " + artist_names_str)

        # # Albüm içindeki şarkı sayısı
        # print("\nTotal Tracks: ", total_track_number)
        # Albüm toplam süresini hesaplama

        # Spotify kodunu yazdırma
        
        # spotify_uri = album["uri"]
        # print("Spotify URI: " + spotify_uri)

        # # Albüm çıkış tarihini yazdırma
        # release_date = str(album["release_date"])
        # date_elements = release_date.split("-")
        # if len(date_elements) == 1:
        #     print("Release Date: " + date_elements[0])
        # else:
        #     date_object = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d %B %Y")
        #     print("Release Date: " + str(date_object))
