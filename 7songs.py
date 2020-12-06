import random
import time

from bs4 import BeautifulSoup
import re
import functions as func


class Songs:
    def __init__(self):
        # Initial playlist
        self.songs = {}
        self.songs['id'] = []
        self.songs['name'] = []
        self.songs['url'] = []
        self.only_lyric = []

    def get_plist(self, url, st):
        # Create playlist
        content = func.get_page(url).text
        # New bs object
        soup = BeautifulSoup(content, 'lxml')
        # print(soup)
        # exit(1)
        plist = soup.find(name='ul',
                          attrs={'class': 'f-hide'})
        # Pass the csv file name according to the toggle
        if st.toggle == False:
            st.csv_fname = st.playlist_title = soup.find(name='h2', class_='f-ff2').string
        # Filter data
        for song in plist.find_all(name='li'):
            # id
            id = re.search('=([0-9]+)', song.a['href'])
            # Avoid repetitive recording of song names
            id_foo = id.group(1)
            if id_foo not in self.songs['id']:
                self.songs['id'].append(id_foo)
                # name
                song_name = song.a.string
                self.songs['name'].append(song_name)
                # url
                song_url = 'https://music.163.com' + song.a['href']
                self.songs['url'].append(song_url)
    #Crawl information such as song artist and album
    def get_detail(self):
        self.songs['songer'] = []
        self.songs['fee'] = []
        self.songs['album'] = []
        self.songs['publishTime'] = []
        self.songs['company'] = []
        self.songs['popularity'] = []
        self.songs['duration'] = []
        self.songs['score'] = []

        total = len(self.songs['id'])
        for song_id in self.songs['id']:
            url ='http://music.163.com/api/song/detail/?id='+ song_id \
                 +'&ids=%5B'+song_id+'%5D'
            # Get song detail
            content = func.get_page(url).json()
            name = content['songs'][0]['artists'][0]['name']
            fee = content['songs'][0]['fee']
            album= content['songs'][0]['album']['name']
            publishTime = content['songs'][0]['album']['publishTime']
            company = content['songs'][0]['album']['company']
            popularity= content['songs'][0]['popularity']
            duration=content['songs'][0]['duration']
            score= content['songs'][0]['score']

            if  name is not None and name!='':
                self.songs['songer'].append(name)
            else:
                self.songs['songer'].append('UnKown')
            if  fee is not None:
                self.songs['fee'].append(fee)
            else:
                self.songs['fee'].append(0)
            if album is not None and album!='':
                self.songs['album'].append(album)
            else:
                self.songs['album'].append('UnKown')
            if publishTime is not None:
                self.songs['publishTime'].append(publishTime)
            else:
                self.songs['publishTime'].append(1568304000000)
            if company is not None and company!='':
                self.songs['company'].append(company)
            else:
                self.songs['company'].append('UnKown')
            if popularity is not None:
                self.songs['popularity'].append(popularity)
            else:
                self.songs['popularity'].append(50)
            if duration is not None:
                self.songs['duration'].append(duration)
            else:
                self.songs['duration'].append(93000)
            if score is not None:
                self.songs['score'].append(score)
            else:
                self.songs['score'].append(50)
            print('completed detail' + str(round(self.songs['id'].index(song_id) / total * 100, 2)) + '% ', end='')
            print('added detail id: ' + song_id)
            time.sleep( random.uniform(1,2))

    def get_lyric(self):
        """获得歌词"""
        self.songs['lyric'] = []
        total = len(self.songs['id'])
        for song_id in self.songs['id']:
            url = 'http://music.163.com/api/song/lyric?os=pc&id=' \
                  + song_id \
                  + '&lv=-1&kv=-1&tv=-1'
            # Get lyrics content
            content = func.get_page(url).json()
            # print(content)
            # exit(1)
            if 'lrc' in content and 'nolyric' not in content and content['lrc'] is not None:
                lyric = content['lrc']['lyric']
                # Clean the lyrics, clean the time, clean the arrangement, etc.
                lyric = re.sub('\[.*?\]', '', lyric)
                templist = lyric.split('\n')
                lyric = ''

                for t in templist:
                    #print(len(re.findall(':', t)))
                    if  len(re.findall(':',t))!=0 or len(re.findall('：',t))!=0:
                        continue
                    else:
                        lyric = lyric + t + '\n'
                # print(lyric)
                # exit(1)
                self.songs['lyric'].append(lyric)
                self.only_lyric.append(lyric)
                print('completed lyric' + str(round(self.songs['id'].index(song_id) / total * 100, 2)) + '% ', end='')
                print('added lyric id: ' + song_id)
            else:
                # Fill to avoid null values of floating point numbers
                self.songs['lyric'].append('ThisShallBeIgnored')
