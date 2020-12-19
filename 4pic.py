import os
import datetime as dt
import time
#from snownlp import SnowNLP
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.width', 1000)

pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)

matplotlib.rcParams['font.sans-serif']='Microsoft Yahei'

def base_graph(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    return ax


def RAP_SCORE_scatter():
    CH_path = os.path.join('./res/', 'Chinese_Rap.csv')
    EN_path = os.path.join('./res/', 'English_Rap.csv')
    df_CN = pd.read_csv(CH_path, low_memory=False)
    df_EN = pd.read_csv(EN_path, low_memory=False)

    X_CN=[] #JL: more descriptive names
    song_score_CN=[]
    X_EN = []
    song_score_EN = []
    for i, r in df_CN.iterrows(): #JL: you should almost never iterate over dataframe rows. use map or apply
        #print(int(r['song_publishTime']))
        timeDate = time.strftime('%Y-%m-%d', time.localtime(int(r['song_publishTime'])/ 1000) ) #JL: don't use mixed case variable names
        #print(timeDate)
        song_score_CN.append(int(r['song_score']))
        #if timeDate not in X_CN:
        X_CN.append(timeDate)

    for i, r in df_EN.iterrows():
        timeDate = time.strftime('%Y-%m-%d', time.localtime(int(r['song_publishTime']) / 1000))
        song_score_EN.append(int(r['song_score']))
        # if timeDate not in X_CN:
        X_EN.append(timeDate)
    yearlist=[]
    for m in X_CN+X_EN:
        year = m.replace('-','')[0:4]
        if year not in yearlist:
            yearlist.append(year)
    yearlist.sort()

    up_colors = ['SkyBlue', 'IndianRed', 'LimeGreen']

    fig, axs = plt.subplots(2, 1, figsize=(16, 9))
    axs = [base_graph(ax) for ax in axs]

    area = np.pi * 4 ** 2
    axs[0].scatter(X_CN, song_score_CN, s=area, c=up_colors[0], alpha=0.4, label='RAP Score CN')
    axs[1].scatter(X_EN, song_score_EN, s=area, c=up_colors[1], alpha=0.4, label='RAP Score EN')

    axs[1].xaxis.set_ticklabels([], minor=True)
    axs[0].xaxis.set_ticklabels([], minor=True)


    axs[0].set_xlabel('')
    axs[1].set_xlabel('')

    handles_top, labels_top = axs[0].get_legend_handles_labels()
    #handles_mid, labels_mid = axs[1].get_legend_handles_labels()
    handles_bot, labels_bot = axs[1].get_legend_handles_labels()

    legend_top = fig.legend(handles_top, '', loc=(0.80, 0.75), title='RAP Score CN')
    #legend_mid = fig.legend(handles_mid, states_up, loc=(0.80, 0.45), title='Rate of percent_submit,Eng')
    legend_bot = fig.legend(handles_bot, '', loc=(0.80, 0.15), title='RAP Score EN')

    fig.add_artist(legend_top)
    #fig.add_artist(legend_mid)
    fig.add_artist(legend_bot)
    fig.subplots_adjust(right=0.82)
    fig.text(0.04, 0.5, 'Scatter chart of CN/EN RAP SCORE', va='center', rotation='vertical')
    png_path = os.path.join('./res/', 'Scatter_chart_of_CN-EN_RAP_SCORE.png')

    ind = np.arange(len(yearlist))*16.4
    #plt.setp(axs[0].get_xticklabels(), visible=False)

    plt.xticks(ind, yearlist, rotation='vertical')
    axs[0].set_xticks([])
    #plt.xticks([])
    plt.savefig(png_path)
    plt.show()
    print('Scatter Image saved: ', png_path)
    plt.close()

def RAP_year_bar():

    CH_path = os.path.join('./res/', 'Chinese_Rap.csv')
    EN_path = os.path.join('./res/', 'English_Rap.csv')
    df_CN = pd.read_csv(CH_path, low_memory=False)
    df_EN = pd.read_csv(EN_path, low_memory=False)


    song_publish_dict = {}
    for i, r in df_CN.iterrows():
        #print(int(r['song_publishTime']))
        timeDate = time.strftime('%Y-%m-%d', time.localtime(int(r['song_publishTime'])/ 1000) )
        year = timeDate[0:4]
        if year not in song_publish_dict:
            song_publish_dict[year]=(1,0)
        else:
            song_publish_dict[year] = (song_publish_dict[year][0]+1, song_publish_dict[year][1])

    for i, r in df_EN.iterrows():
        #print(int(r['song_publishTime']))
        timeDate = time.strftime('%Y-%m-%d', time.localtime(int(r['song_publishTime'])/ 1000) )
        year = timeDate[0:4]
        if year not in song_publish_dict:
            song_publish_dict[year]=(0,1)
        else:
            song_publish_dict[year] = (song_publish_dict[year][0], song_publish_dict[year][1]+1)
    #print(song_publish_dict)
    song_publish_dict = sorted(song_publish_dict.items(), key=lambda d: d[0])


    yearlist=[]
    X_CN=[]
    X_EN=[]
    for m,v in song_publish_dict:
        year = m
        if year not in yearlist:
            X_CN.append(v[0])
            X_EN.append(v[1])
            yearlist.append(year)

    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    axs = base_graph(ax)
    ind = np.arange(len(yearlist))
    width = 0.3  # the width of the bars

    up_colors = ['SkyBlue', 'IndianRed', 'LimeGreen']

    for i in range(2):
        if i == 0:
            axs.bar(ind - 1 * width / 2, X_CN, width, color=up_colors[2], label='CN')
        elif i == 1:
            axs.bar(ind + width / 2, X_EN, width, color=up_colors[1], label='EN')


    handles_top, labels_top = axs.get_legend_handles_labels()

    legend_top = fig.legend(handles_top, labels_top, loc=(0.3, 0.334), title='publish num distribute ')

    fig.add_artist(legend_top)
    fig.subplots_adjust(right=0.82)
    fig.text(0.04, 0.5, 'Most popular rap publish time', va='center', rotation='vertical')
    plt.xticks(ind, yearlist,rotation = 45)

    png_path = os.path.join('./res', 'The_most_popular_Chinese-English_rap_publish_time_distribution.png')
    plt.savefig(png_path)
    print('Image saved: ', png_path)
    plt.show()
    plt.close() #JL: plt.show() will also run close(), so you only need this if you skip show

def RAP_song_company_pie():
    #exp =[0.1,0,0,0,0,0,0,0]

    CH_path = os.path.join('./res/', 'Chinese_Rap.csv')
    EN_path = os.path.join('./res/', 'English_Rap.csv')
    df_CN = pd.read_csv(CH_path, low_memory=False)
    df_EN = pd.read_csv(EN_path, low_memory=False)

    company_CN = {}
    company_EN = {}
    allCN=0
    allEN=0

    for i, r in df_CN.iterrows():
        # print(int(r['song_publishTime']))
        song_company = r['song_company']
        if song_company not in company_CN:
            company_CN[song_company]=1
        else:
            company_CN[song_company] =company_CN[song_company]+1
        allCN=allCN+1
    for i, r in df_EN.iterrows():
        # print(int(r['song_publishTime']))
        song_company = r['song_company']
        if song_company not in company_EN:
            company_EN[song_company] = 1
        else:
            company_EN[song_company] = company_EN[song_company] + 1
        allEN=allEN+1

    company_CN = sorted(company_CN.items(), key=lambda kv: kv[1], reverse=True)
    company_EN = sorted(company_EN.items(), key=lambda kv: kv[1], reverse=True)

    label_CN=[]
    piev_CN = []
    for ii in company_CN:
        if ii[0]=='UnKown':
            label_CN.append('个人网络发行')
            piev_CN.append(round(int(ii[1])/allCN,6))
        else:
            label_CN.append(ii[0])
            piev_CN.append(round(int(ii[1])/allCN,6))

    label_EN = []
    piev_EN = []
    for ii in company_EN:
        #print(ii)
        if ii[0]=='UnKown':
            label_EN.append('个人网络发行')
            piev_EN.append(round(int(ii[1])/allEN,6))
        else:
            label_EN.append(ii[0])
            piev_EN.append(round(int(ii[1])/allEN,6))


    up_colors = ['SkyBlue', 'IndianRed', 'LimeGreen']


    fig, axs = plt.subplots(2, 1, figsize=(8, 6))
    axs = [base_graph(ax) for ax in axs]
    #print(np.sum(piev_CN))

    patches, l_text, p_text =axs[0].pie(piev_CN[0:10],pctdistance=0.7,autopct='%.1f%%',startangle=90, labels=label_CN[0:10])
    axs[0].axis("equal")  # 设置x轴和y轴等长，否则饼图将不是一个正圆
    patches, l_text1, p_text1 =axs[1].pie(piev_EN[0:10],autopct='%.1f%%',startangle=90, labels=label_EN[0:10])
    axs[1].axis("equal")  # 设置x轴和y轴等长，否则饼图将不是一个正圆

    axs[0].legend(label_CN[0:10])
    axs[1].legend(label_EN[0:10])
    axs[0].legend(loc='center left')
    axs[1].legend(loc='center right')
    for t in p_text:
        t.set_size(5)

    for t in l_text:
        t.set_size(6)

    for t in p_text1:
        t.set_size(5)

    for t in l_text1:
        t.set_size(6)

    handles_top, labels_top = axs[0].get_legend_handles_labels()
    # handles_mid, labels_mid = axs[1].get_legend_handles_labels()
    handles_bot, labels_bot = axs[1].get_legend_handles_labels()

    legend_top = fig.legend(handles_top, '', loc=(0.06, 0.94), title='RAP Company CN')
    # legend_mid = fig.legend(handles_mid, states_up, loc=(0.80, 0.45), title='Rate of percent_submit,Eng')
    legend_bot = fig.legend(handles_bot, '', loc=(0.80, 0.45), title='RAP Company EN')

    fig.add_artist(legend_top)
    # fig.add_artist(legend_mid)
    fig.add_artist(legend_bot)

    plt.title('Proportion of top 10 Chinese and English rap companies')
    plt.savefig('./res/Top_10_Chinese-English_rap_companies.png')
    plt.show()
    print('Scatter Image saved: ', './res/Top_10_Chinese-English_rap_companies.png')
    plt.close()

def RAP_singner_barH():
    CH_path = os.path.join('./res/', 'Chinese_Rap.csv')
    EN_path = os.path.join('./res/', 'English_Rap.csv')
    df_CN = pd.read_csv(CH_path, low_memory=False)
    df_EN = pd.read_csv(EN_path, low_memory=False)

    company_CN = {}
    company_EN = {}
    allCN=0
    allEN=0

    for i, r in df_CN.iterrows():
        # print(int(r['song_publishTime']))
        song_company = r['song_songer']
        if song_company not in company_CN:
            company_CN[song_company]=1
        else:
            company_CN[song_company] =company_CN[song_company]+1
        allCN=allCN+1
    for i, r in df_EN.iterrows():
        # print(int(r['song_publishTime']))
        song_company = r['song_songer']
        if song_company not in company_EN:
            company_EN[song_company] = 1
        else:
            company_EN[song_company] = company_EN[song_company] + 1
        allEN=allEN+1

    company_CN = sorted(company_CN.items(), key=lambda kv: kv[1], reverse=True)
    company_EN = sorted(company_EN.items(), key=lambda kv: kv[1], reverse=True)
    X_CN=[]
    Y_CN=[]
    for ii in company_CN:
        X_CN.append(ii[0])
        Y_CN.append(ii[1])
    X_EN = []
    Y_EN = []
    for ii in company_EN:
        X_EN.append(ii[0])
        Y_EN.append(ii[1])

    up_colors = ['SkyBlue', 'IndianRed', 'LimeGreen']
    fig, axs = plt.subplots(2, 1, figsize=(11, 6))
    axs = [base_graph(ax) for ax in axs]

    axs[0].barh( X_CN[0:10],Y_CN[0:10], align='center',color='SkyBlue', ecolor='black')
    axs[1].barh( X_EN[0:10],Y_EN[0:10], align='center',color='LimeGreen', ecolor='black')
    axs[0].set_xlim(0, 22)
    axs[1].set_xlim(0, 22)
    plt.xlabel("Number of songs")
    plt.ylabel("Singer")


    handles_top, labels_top = axs[0].get_legend_handles_labels()
    # handles_mid, labels_mid = axs[1].get_legend_handles_labels()
    handles_bot, labels_bot = axs[1].get_legend_handles_labels()

    legend_top = fig.legend(handles_top, '', loc=(0.80, 0.70), title='TOP 10 RAP SINGER CN')
    # legend_mid = fig.legend(handles_mid, states_up, loc=(0.80, 0.45), title='Rate of percent_submit,Eng')
    legend_bot = fig.legend(handles_bot, '', loc=(0.80, 0.30), title='TOP 10 RAP SINGER EN')

    fig.add_artist(legend_top)
    # fig.add_artist(legend_mid)
    fig.add_artist(legend_bot)
    #plt.title('中英文说唱前十歌手及上榜歌曲数目')
    plt.savefig('./res/Comparison_of_the_number_of_top10_Chinese_and_English_rap_singers_and_songs.png')
    plt.show()
    plt.close()
    print('Scatter Image saved: ', './res/Comparison_of_the_number_of_top10_Chinese_and_English_rap_singers_and_songs.png')

def RAP_sentiment_BAR():
    CH_path = os.path.join('./res/', 'Chinese_Rap-Emotion_classification.csv')
    EN_path = os.path.join('./res/', 'English_Rap-Emotion_classification.csv')
    df_EN = pd.read_csv(EN_path, low_memory=False,encoding="utf_8_sig")
    try:
        df_CN = pd.read_csv(CH_path, low_memory=False,encoding="utf_8_sig")
    except:
        df_CN = pd.read_csv(CH_path, low_memory=False, encoding="gb18030")


    S1=[]
    S2=[]
    S3 = []
    CN_up_all=0
    CN_down_all=0
    CN_normal_all=0
    EN_up_all = 0
    EN_down_all = 0
    EN_normal_all = 0

    for i,r, in df_CN.iterrows():
        if r['sentiment']==-1:
            CN_down_all=CN_down_all+1
        elif r['sentiment']==1:
            CN_up_all = CN_up_all + 1
        else:
            CN_normal_all=CN_normal_all+1

    S1.append(  round( CN_up_all/(CN_down_all+ CN_up_all+ CN_normal_all)*100,6) )
    S2.append( round( CN_down_all/(CN_down_all+ CN_up_all+ CN_normal_all)*100,6) )
    S3.append( round( CN_normal_all/(CN_down_all+ CN_up_all+ CN_normal_all)*100,6) )

    for i,r, in df_EN.iterrows():
        if r['sentiment']==-1:
            EN_down_all= EN_down_all+1
        elif r['sentiment']==1:
           EN_up_all = EN_up_all + 1
        else:
            EN_normal_all=EN_normal_all+1

    S1.append( round( EN_up_all/(EN_down_all+ EN_up_all+ EN_normal_all)*100,6) )
    S2.append(  round( EN_down_all/(EN_down_all+ EN_up_all+ EN_normal_all)*100,6))
    S3.append(  round( EN_normal_all/(EN_down_all+ EN_up_all+ EN_normal_all)*100,6))

    d = []
    for i in range(0, len(S1)):
        sum = S1[i] + S2[i]
        d.append(sum)

    print('中、英文说唱情感积极所占比例为：'+str(S1))
    print('中、英文说唱情感消极所占比例为：'+str(S2))
    print('中、英文说唱情感中性所占比例为：' + str(S3))
    ind = np.arange(2)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, S1, width, color='#d62728')  # , yerr=menStd)
    p2 = plt.bar(ind, S2, width,bottom=S1)  # , yerr=womenStd)
    p3 = plt.bar(ind, S3, width, bottom=d)

    plt.ylabel('Percentage') #JL: these operations should all be done on the axis object
    plt.title('Comparison of emotion classification between Chinese and English rap')
    plt.xticks(ind, ('CN', 'EN'))
    plt.yticks(np.arange(0, 110, 10))
    plt.legend((p1[0], p2[0], p3[0]), ('positive', 'negative', 'neutral'))

    plt.savefig('./res/Comparison-of-emotion-classification-between-Chinese-and-English-rap.png')
    plt.show()
    plt.close()
    print('Scatter Image saved: ', './res/Comparison-of-emotion-classification-between-Chinese-and-English-rap.png')
#RAP_SCORE_scatter()
#RAP_year_bar()
#RAP_song_company_pie()
#RAP_singner_barH()
#RAP_sentiment()
#RAP_sentiment_BAR()
