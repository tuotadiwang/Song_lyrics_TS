import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


# all lyrics
TS_lyrics = pd.read_csv('/Users/BettyX/Documents/Data/TS_songs/song_lyrics.csv')
TS_lyrics = TS_lyrics.rename(columns={'Song ': 'song', 'Artist(s) ': 'artists', 'Writer(s) ': 'writers', 'Album ': 'album', 'Year ': 'year', 'Ref. ': 'ref'})
TS_lyrics['year'] = TS_lyrics['year'].astype(int)
TS_lyrics['lyrics'] = TS_lyrics['lyrics'].astype('string')

TS_lyrics['word_count'] = TS_lyrics['lyrics'].apply(lambda x: x.split(' ')).apply(len)

words_per_year = TS_lyrics.groupby('year')['word_count'].mean()
words_per_year.plot.bar(x='year', y='word_count', title='Average number of words per song in each year')
# plt.show()
plt.savefig('/Users/BettyX/Documents/Data/TS_songs/all_length_year.png')


words_per_album = TS_lyrics.groupby('album').mean().sort_values('year', ascending=True)['word_count']
words_per_album.plot.bar(x='year', y='word_count', title='Average number of words per song in each album')
plt.xticks(fontsize=8)
plt.tight_layout()
# plt.show()
plt.savefig('/Users/BettyX/Documents/Data/TS_songs/all_length_album.png')

# word cloud for the song lyrics
all_lyrics = ' '.join(TS_lyrics.lyrics.tolist())
stopwords = set(STOPWORDS)
wordcloud_all_lyrics = WordCloud(stopwords=stopwords,background_color='white').generate(all_lyrics)
plt.figure()
plt.imshow(wordcloud_all_lyrics, interpolation='bilinear')
plt.axis('off')
# plt.show()
wordcloud_all_lyrics.to_file('/Users/BettyX/Documents/Data/TS_songs/all_lyrics.png')



# regular_lyrics: only contains songs that are from regular albums or singles
regular_albums = {'Taylor Swift':2006, 'Fearless':2008, 'Speak Now':2010, 'Red':2012, '1989':2014, 'Reputation':2017, 'Lover':2019, 'Folklore':2020}

regular = []
stem = []
release = []
for index, row in TS_lyrics.iterrows():
    album_stem = re.sub(r'\([^)]*\)', '', row.album)
    stem.append(album_stem)
    if 'single' in album_stem:
        regular.append(True)
        release.append('single')
    elif album_stem.rstrip() in regular_albums.keys():
        regular.append(True)
        release.append(album_stem.rstrip())
    else:
        regular.append(False)
        release.append('other')

TS_lyrics['regular'] = regular
TS_lyrics['release'] = release

TS_regular_lyrics = TS_lyrics[TS_lyrics['regular']==True]

words_per_year = TS_regular_lyrics.groupby('year')['word_count'].mean()
words_per_year.plot.bar(x='year', y='word_count', title='Average number of words per song in each year (regular album & singles)')
# plt.show()
plt.savefig('/Users/BettyX/Documents/Data/TS_songs/regular_length_year.png')


words_per_album = TS_regular_lyrics.groupby('release').mean().sort_values('year', ascending=True)['word_count']
words_per_album.plot.bar(x='year', y='word_count', title='Average number of words per song in each album (regular album & singles)')
plt.xticks(fontsize=8)
plt.tight_layout()
# plt.show()
plt.savefig('/Users/BettyX/Documents/Data/TS_songs/all_length_album.png')

# word cloud for the song lyrics
all_lyrics = ' '.join(TS_regular_lyrics.lyrics.tolist())
stopwords = set(STOPWORDS)
wordcloud_regular_lyrics = WordCloud(stopwords=stopwords,background_color='white').generate(all_lyrics)
plt.figure()
plt.imshow(wordcloud_regular_lyrics, interpolation='bilinear')
plt.axis('off')
# plt.show()
wordcloud_regular_lyrics.to_file('/Users/BettyX/Documents/Data/TS_songs/regular_lyrics.png')
# Woo, a lot of (sad) love stories: never know love


def draw_wordcloud(text):
    stopwords = set(STOPWORDS)
    wordcloud_album_lyrics = WordCloud(stopwords=stopwords,background_color='white').generate(text)
    plt.figure()
    plt.imshow(wordcloud_regular_lyrics, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    return wordcloud_album_lyrics


for album in set(TS_regular_lyrics.release):
    text = ' '.join(TS_regular_lyrics[TS_regular_lyrics['release'] == album].lyrics.tolist())
    wordcloud_album_lyrics = draw_wordcloud(text)
    wordcloud_album_lyrics.to_file('/Users/BettyX/Documents/Data/TS_songs/{}_lyrics.png'.format(album))
    plt.clf()

