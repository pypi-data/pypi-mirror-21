#!/usr/bin/env python

'''
Tries to find the metadata of songs based on the file name
https://github.com/lakshaykalbhor/MusicRepair
'''

try:
    from . import albumsearch
    from . import improvename
    from . import log
except:
    import albumsearch
    import improvename
    import log

from os import rename, environ
from os.path import realpath, basename
import difflib
import six
import configparser

from bs4 import BeautifulSoup

from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File
import requests
import spotipy

if six.PY2:
    from urllib2 import urlopen
    from urllib2 import quote
    Py3 = False
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen
    Py3 = True



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


def matching_details(song_name, song_title, artist):
    '''
    Provides a score out of 10 that determines the
    relevance of the search result
    '''

    match_name = difflib.SequenceMatcher(None, song_name, song_title).ratio()
    match_title = difflib.SequenceMatcher(None, song_name, artist + song_title).ratio()

    if max(match_name,match_title) >= 0.55:
        return True, max(match_name,match_title)

    else:
        return False, (match_name + match_title) / 2


def get_lyrics_letssingit(song_name):
    '''
    Scrapes the lyrics of a song since spotify does not provide lyrics
    takes song title as arguement
    '''

    lyrics = ""
    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + \
        quote(song_name.encode('utf-8'))
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})

    try:
        link = link.get('href')
        link = urlopen(link).read()
        soup = BeautifulSoup(link, "html.parser")

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]

        except AttributeError:
            lyrics = ""

    except:
        lyrics = ""

    return lyrics

def get_lyrics_genius(song_title):
    '''
    Scrapes the lyrics from Genius.com
    '''
    base_url = "http://api.genius.com"
    headers = {'Authorization': 'Bearer %s' %(GENIUS_KEY)}
    search_url = base_url + "/search"
    data = {'q': song_title}

    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    song_api_path = json["response"]["hits"][0]["result"]["api_path"]

    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path

    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    div = soup.find('div',{'class': 'song_body-lyrics'})
    lyrics = div.find('p').getText()
  
    return lyrics


def get_details_spotify(song_name):
    '''
    Tries finding metadata through Spotify
    '''

    song_name = improvename.songname(song_name)

    spotify = spotipy.Spotify()
    results = spotify.search(song_name, limit=1)  # Find top result

    log.log_indented('* Finding metadata from Spotify.')

    try:
        album = (results['tracks']['items'][0]['album']
                 ['name'])  # Parse json dictionary
        artist = (results['tracks']['items'][0]['album']['artists'][0]['name'])
        song_title = (results['tracks']['items'][0]['name'])
        try:
            log_indented("* Finding lyrics from Genius.com")
            lyrics = get_lyrics_genius(song_title)
        except:
            log_error("* Could not find lyrics from Genius.com, trying something else")
            lyrics = get_lyrics_letssingit(song_title)

        match_bool, score = matching_details(song_name, song_title, artist)
        if match_bool:
            return artist, album, song_title, lyrics, match_bool, score
        else:
            return None

    except IndexError:
        log.log_error(
            '* Could not find metadata from spotify, trying something else.', indented=True)
        return None


def get_details_letssingit(song_name):
    '''
    Gets the song details if song details not found through spotify
    '''

    song_name = improvename.songname(song_name)

    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + \
        quote(song_name.encode('utf-8'))
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})
    try:
        link = link.get('href')
        link = urlopen(link).read()

        soup = BeautifulSoup(link, "html.parser")

        album_div = soup.find('div', {'id': 'albums'})
        title_div = soup.find('div', {'id': 'content_artist'}).find('h1')

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]
        except AttributeError:
            lyrics = ""
            log.log_error("* Couldn't find lyrics", indented=True)

        try:
            song_title = title_div.contents[0]
            song_title = song_title[1:-8]
        except AttributeError:
            log.log_error("* Couldn't reset song title", indented=True)
            song_title = song_name

        try:
            artist = title_div.contents[1].getText()
        except AttributeError:
            log.log_error("* Couldn't find artist name", indented=True)
            artist = "Unknown"

        try:
            album = album_div.find('a').contents[0]
            album = album[:-7]
        except AttributeError:
            log.log_error("* Couldn't find the album name", indented=True)
            album = artist

    except AttributeError:
        log.log_error("* Couldn't find song details", indented=True)

        album = song_name
        song_title = song_name
        artist = "Unknown"
        lyrics = ""

    match_bool, score = matching_details(song_name, song_title, artist)

    return artist, album, song_title, lyrics, match_bool, score


def add_albumart(albumart, song_title):
    '''
    Adds the album art to the song
    '''

    try:
        img = urlopen(albumart)  # Gets album art from url

    except Exception:
        log.log_error("* Could not add album art", indented=True)
        return None

    audio = EasyMP3(song_title, ID3=ID3)
    try:
        audio.add_tags()
    except _util.error:
        pass

    audio.tags.add(
        APIC(
            encoding=3,  # UTF-8
            mime='image/png',
            type=3,  # 3 is for album art
            desc='Cover',
            data=img.read()  # Reads and adds album art
        )
    )
    audio.save()
    log.log("> Added album art")


def add_details(file_name, title, artist, album, lyrics=""):
    '''
    Adds the details to song
    '''

    tags = EasyMP3(file_name)
    tags["title"] = title
    tags["artist"] = artist
    tags["album"] = album
    tags.save()

    tags = ID3(file_name)
    uslt_output = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
    tags["USLT::'eng'"] = uslt_output

    tags.save(file_name)

    log.log("> Adding properties")
    log.log_indented("[*] Title: %s" % title)
    log.log_indented("[*] Artist: %s" % artist)
    log.log_indented("[*] Album: %s " % album)


def fix_music(file_name):
    '''
    Searches for '.mp3' files in directory (optionally recursive)
    and checks whether they already contain album art and album name tags or not.
    '''

    setup()

    if not Py3:
        file_name = file_name.encode('utf-8')

    tags = File(file_name)

    log.log(file_name)
    log.log('> Adding metadata')

    try:
        artist, album, song_name, lyrics, match_bool, score = get_details_spotify(
            file_name)  # Try finding details through spotify

    except Exception:
        artist, album, song_name, lyrics, match_bool, score = get_details_letssingit(
            file_name)  # Use bad scraping method as last resort

    try:
        log.log_indented('* Trying to extract album art from Google.com')
        albumart = albumsearch.img_search_google(artist+' '+album)
    except Exception:
        log.log_indented('* Trying to extract album art from Bing.com')
        albumart = albumsearch.img_search_bing(artist+' '+album)

    if match_bool:
        add_albumart(albumart, file_name)
        add_details(file_name, song_name, artist, album, lyrics)

        try:
            rename(file_name, artist+' - '+song_name+'.mp3')
        except Exception:
            log.log_error("Couldn't rename file")
            pass
    else:
        log.log_error(
            "* Couldn't find appropriate details of your song", indented=True)

    log.log("Match score: %s/10.0" % round(score * 10, 1))
    log.log(LOG_LINE_SEPERATOR)
    log.log_success()


if __name__ == '__main__':
    main()
