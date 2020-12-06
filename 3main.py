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
    # Get the top 50 playlists
    pls.get_playlists(st)

    if not os.path.exists('res/' + st.csv_fname + '.csv'):
        # Download playlist recursively
        pls.recur_playlists(st)


def single_playlist():
    if not os.path.exists('res/' + st.csv_fname + '.csv'):
        # Create a new playlist category
        s = Songs()
        s.get_plist(st.playlist_url, st)
        s.get_lyric()
        s.get_detail()
        func.songs_to_csv(s.songs, st)


if __name__ == "__main__":
    st = Settings()
    # Create a new word pool
    st.search_keyword = '中文说唱'
    st.playlist_title = '中文说唱'
    st.csv_fname = 'Chinese_Rap'
    st.result_limit = 50
    w = WordPool()
    #
    if st.toggle == True:
        search_and_save()
    else:
        #Single playlist crawl
        single_playlist()
    # Word cloud
    st.more = 'en'
    w.get_wordpool(st)
    if st.word_rank:
        w.word_freq(st)
    w.generate_wordcloud(st)

    st.search_keyword = '英文说唱'
    st.playlist_title = '英文说唱'
    st.csv_fname = 'English_Rap'
    st.result_limit = 40
    #
    if st.toggle == True:
        search_and_save()
    else:
        # Single playlist crawl
        single_playlist()
    #Word cloud
    st.more = 'm'
    w.get_wordpool(st)
    if st.word_rank:
        w.word_freq(st)
    w.generate_wordcloud(st)
    #Drawing
    pic.RAP_SCORE_scatter()
    pic.RAP_year_bar()
    pic.RAP_song_company_pie()
    pic.RAP_singner_barH()

    # emotion analysis
    Lyc.RAP_sentiment('Chinese_Rap')
    Lyc.RAP_sentiment('English_Rap')
    pic.RAP_sentiment_BAR()