#!/usr/bin/env python

r"""
  __  __           _      _   _               
 |  \/  |_   _ ___(_) ___| \ | | _____      __
 | |\/| | | | / __| |/ __|  \| |/ _ \ \ /\ / /
 | |  | | |_| \__ \ | (__| |\  | (_) \ V  V / 
 |_|  |_|\__,_|___/_|\___|_| \_|\___/ \_/\_/  
                                              
"""

import argparse
import configparser
import re
import requests
import youtube_dl
import spotipy
import six

from os import system, rename, listdir, curdir, name
from os.path import basename, realpath
from collections import OrderedDict
from bs4 import BeautifulSoup

try:
    from . import repair
    from . import log
except:
    import repair
    import log

if six.PY2:
    from urllib2 import urlopen
    from urllib2 import quote
    input = raw_input
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen

YOUTUBECLASS = 'spf-prefetch'

def setup():
    """
    Gathers all configs
    """

    global CONFIG, BING_KEY, GENIUS_KEY, config_path, LOG_FILENAME, LOG_LINE_SEPERATOR 

    LOG_FILENAME = 'musicrepair_log.txt'
    LOG_LINE_SEPERATOR = '........................\n'

    CONFIG = configparser.ConfigParser()
    config_path = realpath(__file__).replace(basename(__file__),'')
    config_path = config_path + 'config.ini'
    CONFIG.read(config_path)

    GENIUS_KEY = CONFIG['keys']['genius_key']
    BING_KEY = CONFIG['keys']['bing_key']

    if GENIUS_KEY == '<insert genius key here>':
        log.log_error('Warning, you are missing the Genius key. Add it using --config')

    if BING_KEY == '<insert bing key here>':
        log.log_error('Warning, you are missing the Bing key. Add it using --config')

def add_config():
    """
    Prompts user for API keys, adds them in an .ini file stored in the same
    location as that of the script
    """

    genius_key = input('Enter Genius key : ')
    bing_key = input('Enter Bing key : ')

    CONFIG['keys']['bing_key'] = bing_key
    CONFIG['keys']['genius_key'] = genius_key

    with open(config_path, 'w') as configfile:
        CONFIG.write(configfile)


def get_tracks_from_album(album_name):
    '''
    Gets tracks from an album using Spotify's API
    '''

    spotify = spotipy.Spotify()

    album = spotify.search(q='album:' + album_name, limit=1)
    album_id = album['tracks']['items'][0]['album']['id']
    results = spotify.album_tracks(album_id=str(album_id))
    songs = []
    for items in results['items']:
        songs.append(items['name'])

    return songs


def get_url(song_input, auto):
    '''
    Provides user with a list of songs to choose from
    returns the url of chosen song.
    '''
    youtube_list = OrderedDict()
    num = 0  # List of songs index

    html = requests.get("https://www.youtube.com/results",
                        params={'search_query': song_input})
    soup = BeautifulSoup(html.text, 'html.parser')

    # In all Youtube Search Results

    for i in soup.findAll('a', {'rel': YOUTUBECLASS}):
        song_url = 'https://www.youtube.com' + (i.get('href'))
        song_title = (i.get('title'))
        # Adds title and song url to dictionary
        youtube_list.update({song_title: song_url})

        if not auto:
            print('(%s) %s' % (str(num + 1), song_title))  # Prints list
            num = num + 1

        elif auto:
            print(song_title)
            return list(youtube_list.values())[0], list(youtube_list.keys())[0]

    # Checks if YouTube search return no results
    if youtube_list == {}:
        log.log_error('No match found!')
        exit()

    # Gets the demanded song title and url
    song_url, song_title = prompt(youtube_list)

    return song_url, song_title  # Returns Name of Song and URL of Music Video


def prompt(youtube_list):
    '''
    Prompts for song number from list of songs
    '''

    option = int(input('\nEnter song number > '))
    try:
        song_url = list(youtube_list.values())[option - 1]
        song_title = list(youtube_list.keys())[option - 1]
    except IndexError:
        log.log_error('Invalid Input')
        exit()

    system('clear')
    print('Download Song: ')
    print(song_title)
    print('Y/n?')
    confirm = input('>')
    if confirm == '' or confirm.lower() == 'y':
        pass
    elif confirm.lower() == 'n':
        exit()
    else:
        log.log_error('Invalid Input')
        exit()

    return song_url, song_title


def download_song(song_url, song_title):
    '''
    Downloads song from youtube-dl
    '''
    outtmpl = song_title + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'},
        ],

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(song_url, download=True)


def main():
    '''
    Starts here, handles arguments
    '''

    system('clear') # Must be system('cls') for windows

    setup()

    parser = argparse.ArgumentParser(
        description='Download songs with album art and metadata!')
    parser.add_argument('-c', '--config', action='store_true',
                        help='Set your API keys')
    parser.add_argument('-m', '--multiple', action='store', dest='multiple_file',
                        help='Download multiple songs from a text file list')
    parser.add_argument('-a', '--auto', action='store_true',
                        help='Automatically chooses top result')
    parser.add_argument('--album', action='store_true',
                        help='Downloads all songs from an album')
    args = parser.parse_args()
    arg_multiple = args.multiple_file or None
    arg_auto = args.auto or None
    arg_album = args.album or None
    arg_config = args.config


    if arg_config:
        add_config()

    elif arg_multiple and arg_album:
        log.log_error("Can't do both!")

    elif arg_album:
        album_name = input('Enter album name : ')
        try:
            tracks = get_tracks_from_album(album_name)
            for songs in tracks:
                print(songs)
            confirm = input(
                '\nAre these the songs you want to download? (Y/n)\n> ')

        except IndexError:
            log.log_error("Couldn't find album")
            exit()

        if confirm == '' or confirm.lower() == ('y'):
            for track_name in tracks:
                track_name = track_name + ' song'
                song_url, file_name = get_url(track_name, arg_auto)
                download_song(song_url, file_name)
                system('clear')
                repair.fix_music(file_name + '.mp3')

        elif confirm.lower() == 'n':
            log.log_error("Sorry, if appropriate results weren't found")
            exit()
        else:
            log.log_error('Invalid Input')
            exit()

    elif arg_multiple:
        with open(arg_multiple, "r") as f:
            file_names = []
            for line in f:
                file_names.append(line.rstrip('\n'))

        for files in file_names:
            files = files + ' song'
            song_url, file_name = get_url(files, arg_auto)
            download_song(song_url, file_name)
            system('clear')
            repair.fix_music(file_name + '.mp3')

    else:
        query = input('Enter Song Name : ')
        song_url, file_name = get_url(query, arg_auto)  # Gets YT url
        download_song(song_url, file_name)  # Saves as .mp3 file
        system('clear')
        repair.fix_music(file_name + '.mp3')


if __name__ == '__main__':
    main() 
