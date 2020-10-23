# scrape song lyrics from Taylor Swift
import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd

# client_id = VqQs2ANcZR9jhS-PTAxPeKcjbBQKyqlObmKb1ADjgOt7aOyUNJmhD7f-Cnk5VAWz
# client_secret = NETck97eyXfZ-LrZUxKkBNGhfzzcbK50CNroTjN2vQpQl-mk6g-7-d357ezBQSYy56l0W_-lB2ns5VHZB8_N1A
access_token = 'q7XhzJuUCtiegzq8rIn4a_4E1P1l8UILLZTWTkYQln7SDKxR6Cr1VKhEwNtwP05t'
base = "https://api.genius.com"

def search_song(song_name, artist_name):
    search_url = base + '/search'
    token = 'Bearer {}'.format(access_token)
    data = {'q': song_name + artist_name}
    headers = {'Authorization': token}
    response = requests.get(search_url, data=data, headers=headers).json()
    song_hit = None
    song_api_path = None
    for hit in response['response']['hits']:
        if artist_name in hit['result']['primary_artist']['name']:
            song_hit = hit
            break
    if song_hit:
        song_api_path = song_hit['result']['api_path']
    return song_api_path


def get_song_lyric(song_api_path):
    song_url = base + str(song_api_path)
    token = 'Bearer {}'.format(access_token)
    headers = {'Authorization': token}
    response = requests.get(song_url, headers=headers).json()
    path = response['response']['song']['path']
    page_url = 'http://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'lxml')
    # remove script tags
    [h.extract() for h in html('script')]
    # updated css where the lyrics are based in HTML
    lyrics = html.find('div', class_='lyrics').get_text()
    # remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    # remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


TS_songs = pd.read_csv('/Users/BettyX/Documents/Data/TS_songs/song_list.csv')
string_columns = ['Song ', 'Artist(s) ', 'Writer(s) ', 'Album ', 'Ref. ']
TS_songs[string_columns] = TS_songs[string_columns].astype('string')

# two wrong pieces of info in the wikitable:
# Macavity is not a cover; American Girl is not a cover, instead a rolling stone song ft. TS
TS_songs['Song '][TS_songs['Song ']==' "Macavity" (cover) '] = "Macavity"
TS_songs = TS_songs[TS_songs['Song '] !='"American Girl" (cover) ']


for index, row in TS_songs.iterrows():
    song = row['Song ']
    search_name = None
    print(song)
    if 'album' in song:
        search_name = re.findall('"([^"]*)"', song)[0]
    if re.findall('single', song):
        search_name = re.sub(r'\([^)]*\)', '', song)
    if re.findall('remix', song):
        search_name = re.sub(r'\([^)]*\)', '', song) + 'remix'
    else:
        search_name = song
    print(search_name)


song_names = TS_songs['Song ']
song_paths =[]
song_lyrics = []
for song in song_names:
    search_name = None
    if 'remix' in song:
        search_name = re.sub(r'\([^)]*\)', '', song) + 'remix'
    elif 'single' in song:
        search_name = re.sub(r'\([^)]*\)', '', song)
    elif 'album' in song:
        search_name = re.sub(r'\([^)]*\)', '', song)
    else:
        search_name = song
    path = search_song(search_name, 'Taylor Swift')
    song_paths.append(path)
    lyrics = get_song_lyric(path)
    song_lyrics.append(lyrics)

TS_songs['genius_path'] = song_paths
TS_songs['lyrics'] = song_lyrics

TS_songs.to_csv('/Users/BettyX/Documents/Data/TS_songs/song_lyrics.csv')