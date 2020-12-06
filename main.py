from songs import Songs
from playlists import Playlists
from wordpool import WordPool
from settings import Settings
import functions as func
import os
import pic
import LyricSentiment as Lyc

def search_and_save():
    pls = Playlists()
   
    pls.get_playlists(st)

    if not os.path.exists('res/' + st.csv_fname + '.csv'):
        pls.recur_playlists(st)


def single_playlist():
    if not os.path.exists('res/' + st.csv_fname + '.csv'):
        s = Songs()
        s.get_plist(st.playlist_url, st)
        s.get_lyric()
        s.get_detail()
        func.songs_to_csv(s.songs, st)


if __name__ == "__main__":
    st = Settings()
    # 新建一个词池
    st.search_keyword = '中文说唱'
    st.playlist_title = '中文说唱'
    st.csv_fname = '中文说唱'
    st.result_limit = 50
    w = WordPool()
    #
    if st.toggle == True:
        search_and_save()
    else:
        single_playlist()
    # 词云
    st.more = 'en'
    w.get_wordpool(st)
    if st.word_rank:
        w.word_freq(st)
    w.generate_wordcloud(st)

    st.search_keyword = '英文说唱'
    st.playlist_title = '英文说唱'
    st.csv_fname = '英文说唱'
    st.result_limit = 40
    #
    if st.toggle == True:
        search_and_save()
    else:
        # 单个播放列表爬取
        single_playlist()
    #次云
    st.more = 'm'
    w.get_wordpool(st)
    if st.word_rank:
        w.word_freq(st)
    w.generate_wordcloud(st)
    #画图
    pic.RAP_SCORE_scatter()
    pic.RAP_year_bar()
    pic.RAP_song_company_pie()
    pic.RAP_singner_barH()

    # 情感分析
    Lyc.RAP_sentiment('中文说唱')
    Lyc.RAP_sentiment('英文说唱')
    pic.RAP_sentiment_BAR()