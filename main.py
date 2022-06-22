import requests
import numpy as np
from bs4 import BeautifulSoup
import re
import itertools

artist_url = 'https://genius.com/artists/Kendrick-lamar'
filename = 'lyrics.txt'
song_links_list = []

# extract albums links from artist's link
def albums_links_extract(url=artist_url):
    response = requests.get(url, stream=True)

    soup = BeautifulSoup(response.text, "html.parser")

    soup_list = soup.find_all('a', class_="vertical_album_card")
    albums_links_list = []
    for i in soup_list:
        link = i.get('href')
        albums_links_list.append(link)
    return albums_links_list



#extract songs links from album's link
def song_links_from_album(url):
    response = requests.get(url, stream=True)
    soup = BeautifulSoup(response.text, "html.parser")
    soup_list = soup.find_all( class_="u-display_block")
    link_list = []
    
    for i in soup_list:
        link = i.get('href')
        link_list.append(link)
        
    return link_list





#extract & preproccess it for nlp model finetunning, then collect it to txt file
def song_lyrics(url, filename=filename):
    response = requests.get(url, stream=True)
    soup = BeautifulSoup(response.text, "html.parser")
    s = soup.get_text()
    text = s[s.find('['):s.find('EmbedCancel')-1]
    text = re.sub(r"\(.*?\)|\[.*?\]", '', text)
    t_=[]
    
#     text
#    following for loop is splitting strings like 'stringLike' into ['string','Like'], idk why this happend
    for word in text.split():
        if (word.isupper()==False) and (word.islower()==False) or (bool(re.search(r'\d', word))):
            for i in list(filter(None, re.findall(r'[A-Za-zА-Яа-я][^A-ZА-Я\d\-" "]*|\d+', word))):
                t_.append(i)
        else:
            t_.append(word)

    t_.append(' ')
    text =  ' '.join(t_)
    
    with open(filename, 'a') as f:
        f.write(text)
        
with open(filename, 'w') as f:
    f.truncate(0)

albums_links_list = albums_links_extract(artist_url)

for i in albums_links_list:
    song_links_list.append(song_links_from_album(i))
    
song_links_list = list(itertools.chain.from_iterable(song_links_list))

for i in song_links_list:
    song_lyrics(i)