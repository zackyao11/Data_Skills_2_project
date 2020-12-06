class Settings:
    def __init__(self):

        # 切换按钮，如果为真，则执行爬取搜索结果的歌单，如果为假，则爬取单个歌单
        self.toggle = True
        # 设置搜索关键词
        self.search_keyword = '中文说唱'
        # 设置结果限制数
        self.result_limit = 50

        # 设置歌单url，仅爬一张歌单时
        self.playlist_url = 'https://music.163.com/#/discover/toplist?id=991319590'
        self.playlist_title = '中文说唱'
        # 设置分词过滤强度
        self.more = 'm'  # 分为''、'm'去语气、'e'去英文和语气.'en'去掉高频英文
        # 打印排名
        self.word_rank = True
        self.num = 100  # 前多少名

        if self.toggle == True:
            self.csv_fname = self.search_keyword
        else:
            self.csv_fname = self.playlist_title


