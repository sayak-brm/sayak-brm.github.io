#!/usr/bin/python3

import json
from datetime import datetime

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

def get_yt(album_id):
    links = json.load(open("pre/spotify_albums/yt_links.json"))
    if album_id not in links.keys(): return ""
    else: return links[album_id]

def gen_album(album):
    date = datetime.strptime(album["release_date"], "%Y-%m-%d")
    spotify_uri = "spotify:album:" + album["id"]
    shortcode = '{{< spotify "' + spotify_uri + '" >}}\n{{< songwhip "' + spotify_uri + '" >}}\n'
    yt = get_yt(album["id"])
    if yt:
        shortcode = '{{< youtube ' + yt + ' >}}\n' + shortcode
    with open(f"content/music/{album['name']}.md", "w") as page:
        page.write("---\ntitle: ")
        page.write(album["name"])
        page.write("\ndate: ")
        page.write(date.strftime("%Y-%m-%dT%H:%M:%S+05:30"))
        page.write("\ndraft: false\ntoc: false\ntags: \n")
        page.write("  - music\n  - sayak b\n  - edm\n")
        page.write("---\n\n")
        page.write(shortcode)
    print("Generated music page for:", album["name"])


def main():
    artist_uri = json.load(open("pre/spotify_albums/artist_uri.json"))
    albums = get_albums(artist_uri)
    
    for album in albums:
        gen_album(album)

main()