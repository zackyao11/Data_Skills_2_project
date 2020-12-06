class Settings:
    def __init__(self):

        # Toggle button, if it is true, crawl the playlist of search results, 
        # if it is false, crawl a single playlist
        
        self.toggle = True
        # Set search keywords
        self.search_keyword = '中文说唱'
        # Set result limit
        self.result_limit = 50

        # Set playlist url, only when crawling one playlist
        self.playlist_url = 'https://music.163.com/#/discover/toplist?id=991319590'
        self.playlist_title = '中文说唱'
        # Set the strength of word segmentation filtering
        self.more = 'm'  
        # Divided into ``,'m' to go to the tone,'e' to go to English and tone.
        # 'en' to remove high-frequency English
        # Print ranking
        self.word_rank = True
        self.num = 100  

        if self.toggle == True:
            self.csv_fname = self.search_keyword
        else:
            self.csv_fname = self.playlist_title


