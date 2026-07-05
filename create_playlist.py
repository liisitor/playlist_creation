"""

Spotify Playlist Generator

Creates a private Spotify playlist from a plain text file of songs.

Input format:

    Artist - Song Title

Usage:

    python create_playlist.py <song_file.txt>

The script uses the filename as the playlist name, searches Spotify for each track, 
adds matched songs to the new playlist, and prints any songs that could not be found.

"""

import re
import sys
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def clean_line(line):
    line = line.strip()
    line = re.sub(r"^\d+[\).\s-]+", "", line)
    return line


def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def parse_song(line):
    if " - " not in line:
        return None, line

    artist, title = line.split(" - ", 1)
    return artist.strip(), title.strip()


def search_track(sp, artist, title):
    queries = [
        f'track:"{title}" artist:"{artist}"',
        f"{artist} {title}",
    ]

    artist_norm = normalize(artist)
    title_norm = normalize(title)

    for query in queries:
        result = sp.search(q=query, type="track", limit=10)
        items = result["tracks"]["items"]

        for item in items:
            item_title_norm = normalize(item["name"])
            item_artist_norms = [normalize(a["name"]) for a in item["artists"]]

            if title_norm == item_title_norm and artist_norm in item_artist_norms:
                return item

    return None


def read_songs(track_file):
    with track_file.open("r", encoding="utf-8") as f:
        lines = [clean_line(line) for line in f]

    songs = [
        line
        for line in lines
        if line and not line.startswith("#")
    ]

    if songs and songs[0].startswith("{\\rtf"):
        raise RuntimeError(
            "This file looks like RTF, not plain text. "
            "Save it as plain UTF-8 .txt first."
        )

    return songs


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python create_playlist.py <song_file.txt>")
        sys.exit(1)

    track_file = Path(sys.argv[1])

    if not track_file.exists():
        print(f"File not found: {track_file}")
        sys.exit(1)

    playlist_name = track_file.stem

    scope = "playlist-modify-private playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://127.0.0.1:8888/callback",
        open_browser=False,
        show_dialog=True,
        cache_path=".spotify_cache"
    ))

    me = sp.current_user()
    print("Logged in as:", me["id"], me.get("display_name"))
    print("Creating playlist:", playlist_name)

    playlist = sp.current_user_playlist_create(
        name=playlist_name,
        public=False,
        description=f"Created automatically from {track_file.name}"
    )

    songs = read_songs(track_file)

    track_uris = []
    not_found = []

    for song in songs:
        artist, title = parse_song(song)

        if not artist:
            print("Skipped invalid line:", song)
            not_found.append(song)
            continue

        track = search_track(sp, artist, title)

        if track:
            uri = track["uri"]

            if uri not in track_uris:
                track_uris.append(uri)

            found_artist = track["artists"][0]["name"]
            found_title = track["name"]

            print(f"Found: {artist} - {title} → {found_artist} - {found_title}")
        else:
            print(f"Not found: {artist} - {title}")
            not_found.append(song)

    if track_uris:
        for i in range(0, len(track_uris), 100):
            sp.playlist_add_items(playlist["id"], track_uris[i:i + 100])

    print("\nDone!")
    print("Playlist:", playlist["external_urls"]["spotify"])

    if not_found:
        print("\nCould not find:")
        for song in not_found:
            print("-", song)


if __name__ == "__main__":
    main()