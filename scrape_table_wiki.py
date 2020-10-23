from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

song_url = 'https://en.wikipedia.org/wiki/List_of_songs_recorded_by_Taylor_Swift'

song_doc = requests.get(song_url).text

soup_song = BeautifulSoup(song_doc, 'lxml')
# print (soup.prettify())

song_table = soup_song.find_all('table', {'class': 'wikitable sortable plainrowheaders'})[0] # one-member array
song_table

# songs
# parser does not work well because of rowspan/colspan

# function to parse wikitables
def process_wikitable(table):
    rows = [x for x in table.find_all('tr')]
    nrows = len(rows)
    ncols = max([len(row.find_all(['th','td'])) for row in rows])
    # print(nrows, ncols)
    # cell: <td><td> or <th><th>

    return rows, nrows, ncols

def get_cell_dimension(cell):
    if cell.has_attr('rowspan'):
        rowD = int(cell.attrs['rowspan'])
    else:
        rowD = 1
    if cell.has_attr('colspan'):
        colD = int(cell.get['colspan'])
    else:
        colD = 1
    return rowD, colD


def process_rows(rows, nrows, ncols):
    import pandas as pd
    import numpy as np
    data = pd.DataFrame(np.ones((nrows, ncols))*np.nan)
    for i, row in enumerate(rows):
        col = data.iloc[i,:][data.iloc[i,:].isnull()].index[0]
        for j, cell in enumerate(row.find_all(['th','td'])):
            rowD, colD = get_cell_dimension(cell)
            while any(data.iloc[i, col:col+colD].notnull()):
                col += 1

            data.iloc[i:i+rowD, col:col+colD] = cell.getText()
            if col < data.shape[1]-1:
                col += colD
    return data

rows, nrows, ncols = process_wikitable(song_table)
df = process_rows(rows, nrows, ncols)
df.replace(r'\s+|\\n', ' ', regex=True, inplace=True)
headers = df.iloc[0]
new_df = pd.DataFrame(df.values[1:], columns=headers)
new_df.to_csv('/my_path/song_list.csv')


# albums
regular_albums = {'Taylor Swift':2006, 'Fearless':2008, 'Speak Now':2010, 'Red':2012, '1989':2014, 'Reputation':2017, 'Lover':2019, 'Folklore':2020}
