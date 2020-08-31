#!/usr/bin/python3

import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_albums(artist_uri):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.artist_albums(artist_uri)
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    return albums


def main():
    artist_uri = json.load(open("pre/spotify_albums/artist_uri.json"))
    albums = get_albums(artist_uri)
    
    for album in albums:
        print(album['name'])

main()