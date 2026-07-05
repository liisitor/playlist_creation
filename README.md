# Spotify Playlist Generator

A small Python script that creates a private Spotify playlist from a plain UTF-8 text file of songs.

## What it does

- Reads songs from a `.txt` file, one song per line.

- Uses the text file name as the Spotify playlist name.

- Creates a new private Spotify playlist.

- Searches Spotify for each song using artist and title.

- Adds matched tracks to the playlist.

- Skips duplicate Spotify track URIs.

- Prints matched songs and any songs that could not be found.

## Input format

Create a plain UTF-8 text file with one track per line:

```
Artist - Song Title
```

Example:

```
The National - Fake Empire    
Editors - Munich    
White Lies - Death
```

Numbered lines are also cleaned automatically, so this is accepted too:

```
1. The National - Fake Empire    
2. Editors - Munich    
3. White Lies - Death
```

Lines starting with `\\\#` are ignored.

## How to run

Install the dependencies:

```
pip install spotipy python-dotenv
```

Create a Spotify developer app:

[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

Add the following Redirect URI in your Spotify app settings:

```
http://127.0.0.1:8888/callback
```

Create a `.env` file in the project folder:

```
SPOTIPY\_CLIENT\_ID=your\_client\_id  
SPOTIPY\_CLIENT\_SECRET=your\_client\_secret   
SPOTIPY\_REDIRECT\_URI=http://127.0.0.1:8888/callback
```

Run the script:

```
python create\_playlist.py late\_night\_drive.txt
```

The first time the script runs, Spotipy opens a browser window where you log into Spotify and authorize the application. The access token is cached locally, so subsequent runs do not require logging in again unless the cache is deleted.

## Example output

```
Logged in as: user\_id Display Name    
    
Creating playlist: late\_night\_drive    
Found: The National - Fake Empire -\> The National - Fake Empire    
Found: Editors - Munich -\> Editors - Munich    
Not found: Unknown Artist - Unknown Song    
    
Done!    
Playlist: https://open.spotify.com/playlist/...    
    
Could not find:    
- Unknown Artist - Unknown Song
```

## What I learned

This project helped me practise AI-assisted coding in a realistic way by turning a small personal workflow into a repeatable script. I gained experience working with the Spotify Web API, OAuth authentication, file parsing, validating API results, and improving the script through testing and debugging.

