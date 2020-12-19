import random

import requests
from requests.exceptions import RequestException
import re
import pandas

"""
General grading comments:
- if you're going to split your code across files, make sure the files have descriptive names.
"""

def get_page(url):
    """获得网页"""

    url = re.sub('/#', '', url) #JL: not sure why a regex is used here
    replace = random.randint(1,9)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'music.163.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        'Origin': 'https://music.163.com',
        'Referer': 'https://music.163.com/song?id=4794{}30{}7'.format(replace,replace), #JL: I don't see replace defined anywhere, which means it's probably a global from a different file.  Definitely confusing.
        #'Cookie':'mail_psc_fingerprint=43648802dbd16a15fd8cf79f689c4f74; vjuids=d93e536fa.170c7be792b.0.67eea5392fa6; _ga=GA1.2.1811201610.1589957385; vinfo_n_f_l_n3=8b4690cc3c68f7e9.1.17.1567500991081.1587363388054.1592467172930; vjlast=1583899114.1593329098.21; NTES_CMT_USER_INFO=16207725%7Cwuchenvic%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7Cd3VjaGVudmljQDE2My5jb20%3D; OUTFOX_SEARCH_USER_ID_NCOO=591292138.5475522; _ntes_nnid=6{}b265e4c9846b6cfedc082e03cea82b,1{}98438026683; _ntes_nuid=6{}b265e4c9846b6cfedc082e03cea82b; UM_distinctid=17461b87624461-095b201e895592-46531b29-1fa400-17461b87625247; NMTID=00Ok4H01NpBqsJDN0z3qlHjqov_VcEAAAF08qDp9g; NTES_SESS=IwEx0IoLy3jZ4zvBTemFUiwrIZ7PD66qtsVpsgUfl4g4mVb8mPEkn1euYKi2g01NjIYna4883hKffoKZ0Gd6dJc2Bvbi8F6NNu._s9hdVDznb5vmHfhhA25.569AWzRMKqzHH2lajwwZ3GvHs8adtz0YwLeOMLtR73jGzc9TMUICHF3lkrXhHGBHukI.1GTWfsqwwO5vDUDrHaHoaPqxYU8cD; S_INFO=1605079719|0|3&80##|wuchenvic; P_INFO=wuchenvic@163.com|1605079719|0|mail163|11&18|sxi&1604499174&mail163#sxi&610100#10#0#0|159430&0|mail163|wuchenvic@163.com; nts_mail_user=wuchenvic@163.com:-1:1; MUSIC_EMAIL_U=3bb1d83a4bcdd09becd5e42e36b6018e90737e9479fc7775a4bc13a8b9d81998ce2e61fdb715cbf54ca041126e574fc6; playliststatus=visible; WNMCID=faafbg.1605079769937.01.0; WM_NI=%2BWaWpMVHBJiQAOKztx0gZ5EusrCoL1YKu62VwwPYQ%2BlulNfzhZLlYgEqE4A5F43h9bJ3a5CCZbbm7O22r7NlhYEAM87Jri7GvVDz2irbf97j7zoIVZcBhinxdAeBI12BZzE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7f16da9e7b7d3b54ab5b88ab7d45a828f8aabf143b3bca4b5ce79a5f09ca3cd2af0fea7c3b92ae989afb8f34796988eabec5b8391859bf774f4b996d6c87fb1ae8d90cf3b9b95bbd7b15eb5a9a0bad421b0aba4afe572ac86848ddc6d87af8bd5c43f86ecfd89bc6a8aedafd6c2499abeae8eb645f2eebed8cd68ac878ba2d034f596be8ab64db68a8c9bb163b2beaadab662f5a6a1aad552a19ea88aed74a89faba3cc3bf29e969bc837e2a3; WM_TID=lGAnkLXpe8BFFFRVFAZ4tLB6m%2FEbd0Ie; csrfToken=WWdEdniNVMMBLQXA3XBqu3Av; playerid=53102155; WEVNSM=1.0.0; JSESSIONID-WYYY=9JHGDa1NcVxloOxARlG3%5CiluFTFhu0gDPRDk6IvO6747E%2FPHd24Ut%2BFuRetBYez3nGzuhcVNzp9CqkA%5Csjmk%5C%2FyM5%5C7afwEADTQk6JQ2ytPTYKMIFuYZU2fBVmKWUffoJE2on%5Ce54GyCC9OW1%2FN9wpc0tx5ij%2F23%2B07GnV886kyi1Xmw%3A1605610577219; _iuqxldmzr_=32'.format(replace, replace, replace)
        #'Cookie': '_ntes_nnid=3{}533f97b25070a32c249f59513ad20c,1{}92582485123;_ntes_nuid = 3{}533f97b25070a32c249f59513ad20c;.............'.format(replace, replace, replace)
        'Cookie': 'mail_psc_fingerprint=43648802dbd16a15fd8cf79f689c4f74; vjuids=d93e536fa.170c7be792b.0.67eea5392fa6; _ga=GA1.2.1811201610.1589957385; vinfo_n_f_l_n3=8b4690cc3c68f7e9.1.17.1567500991081.1587363388054.1592467172930; vjlast=1583899114.1593329098.21; NTES_CMT_USER_INFO=16207725%7Cwuchenvic%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7Cd3VjaGVudmljQDE2My5jb20%3D; OUTFOX_SEARCH_USER_ID_NCOO=591292138.5475522; _ntes_nnid=65b265e4c9846b6cfedc082e03cea82b,1598438026683; _ntes_nuid=65b265e4c9846b6cfedc082e03cea82b; UM_distinctid=17461b87624461-095b201e895592-46531b29-1fa400-17461b87625247; NMTID=00Ok4H01NpBqsJDN0z3qlHjqov_VcEAAAF08qDp9g; NTES_SESS=IwEx0IoLy3jZ4zvBTemFUiwrIZ7PD66qtsVpsgUfl4g4mVb8mPEkn1euYKi2g01NjIYna4883hKffoKZ0Gd6dJc2Bvbi8F6NNu._s9hdVDznb5vmHfhhA25.569AWzRMKqzHH2lajwwZ3GvHs8adtz0YwLeOMLtR73jGzc9TMUICHF3lkrXhHGBHukI.1GTWfsqwwO5vDUDrHaHoaPqxYU8cD; S_INFO=1605079719|0|3&80##|wuchenvic; P_INFO=wuchenvic@163.com|1605079719|0|mail163|11&18|sxi&1604499174&mail163#sxi&610100#10#0#0|159430&0|mail163|wuchenvic@163.com; nts_mail_user=wuchenvic@163.com:-1:1; MUSIC_EMAIL_U=3bb1d83a4bcdd09becd5e42e36b6018e90737e9479fc7775a4bc13a8b9d81998ce2e61fdb715cbf54ca041126e574fc6; playliststatus=visible; WNMCID=faafbg.1605079769937.01.0; WM_NI=%2BWaWpMVHBJiQAOKztx0gZ5EusrCoL1YKu62VwwPYQ%2BlulNfzhZLlYgEqE4A5F43h9bJ3a5CCZbbm7O22r7NlhYEAM87Jri7GvVDz2irbf97j7zoIVZcBhinxdAeBI12BZzE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7f16da9e7b7d3b54ab5b88ab7d45a828f8aabf143b3bca4b5ce79a5f09ca3cd2af0fea7c3b92ae989afb8f34796988eabec5b8391859bf774f4b996d6c87fb1ae8d90cf3b9b95bbd7b15eb5a9a0bad421b0aba4afe572ac86848ddc6d87af8bd5c43f86ecfd89bc6a8aedafd6c2499abeae8eb645f2eebed8cd68ac878ba2d034f596be8ab64db68a8c9bb163b2beaadab662f5a6a1aad552a19ea88aed74a89faba3cc3bf29e969bc837e2a3; csrfToken=WWdEdniNVMMBLQXA3XBqu3Av; playerid=53102155; JSESSIONID-WYYY=EfCp1aSAfU4mfha5SCcQCepu5GZA38sNaBJTD%5CdEbQ78JYOGdrodaiECsIMzSvAI65QVk1SAXdWAgTlbqVHGX1Yu%2F%2BcH673phMUDKWlAbEeVO7wr900RRAIc%2Bcq0VwcwN%2FvxsS56V3EKowv5Sx6d5Rj9pn5RQoUt04I4AgP7xVUAe1cq%3A1605614059305; _iuqxldmzr_=32; WM_TID=lGAnkLXpe8BFFFRVFAZ4tLB6m%2FEbd0Ie; __remember_me=true; MUSIC_U=821b14011cd0311f373dd82e95493cd8498e9f475fcebf17c8f6599590466d720931c3a9fbfe3df2; __csrf=05521056c0c32c51d572a48da2c788ed; ntes_kaola_ad=1; WEVNSM=1.0.0'

    } #JL: don't leave brackets on empty lines in Python
 
    flag = 5 #JL: this could be better named/described
    while flag > 0:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flag = 0
                return response
        except RequestException:
            flag -= 1
            print('retry')
            if flag <= 0:
                return None


def songs_to_csv(songs, st):
    """输出为csv"""
    df = pandas.DataFrame({'song_id': songs['id'],
                           'song_name': songs['name'],
                           'song_url': songs['url'],
                           'song_lyric': songs['lyric'],
                           'song_songer': songs['songer'],
    'song_fee': songs['fee'],
    'song_album': songs['album'] ,
    'song_publishTime': songs['publishTime'] ,
    'song_company': songs['company'] ,
    'song_popularity': songs['popularity'],
    'song_duration': songs['duration'],
    'song_score': songs['score']
                           })
    df.to_csv('res/' + st.csv_fname + '.csv', index=False, sep=',', encoding='utf_8_sig') #JL: join Python paths using os or Path


def make_filter(word_pool, stoplist):

    new_word_pool = []
    for word in word_pool:
        l_word = word.lower()
        if l_word not in stoplist:
            new_word_pool.append(l_word)
    return new_word_pool
