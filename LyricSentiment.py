#Lyrics sentiment analysis
#Call Baidu sentiment analysis API interface

'''
API description


parameter type  description
text	string	Text content, up to 2048 bytes

Return parameter
parameter	Description	
log_id	uint64	Request a unique identification code
sentiment	int	Indicates the result of emotional polarity classification, 0: negative, 1: neutral, 2: positive
confidence	float	Indicates the confidence of classification, the value range is [0,1]
positive_prob	float	Indicates the probability of belonging to the positive category, the value range is [0,1]
negative_prob	float	Indicates the probability of belonging to the negative category, the value range is [0,1]

注：
1. In the actual call, it was found that the text containing semicolons and excluding semicolons had a great impact on the results, and some results directly changed from positive to negative, and the non-Chinese symbols in the text were removed during analysis.
2. In order to facilitate further analysis, the sentiment polarity classification is changed to -1,0,1
'''


import urllib3
import json
import time
import pandas as pd
import numpy as np
import os

def RAP_sentiment(Name):
    local_main2 = './res/'+Name+'-情感分类.csv'
    if not os.path.exists(local_main2):
     
        data = pd.DataFrame(columns = ['song_id','song_name','song_songer','song_publishTime','sentiment','confidence','positive_prob','negative_prob'])
        data.to_csv(local_main2, index = None, encoding = 'utf_8_sig')

    access_token='24.65051f487401f5c9d61249a0aa7634dd.2592000.1609323856.282335-23069052'  

    http=urllib3.PoolManager()
    if Name=='中文说唱':
        url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token='+access_token
    elif Name=='英文说唱':
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=' + access_token+'&charset=UTF-8'

    file = pd.read_csv('./res/'+Name+'.csv',encoding="utf_8_sig",low_memory=False)
    try:
        fileout = pd.read_csv(local_main2, encoding="utf_8_sig", low_memory=False)
    except:
        fileout = pd.read_csv(local_main2, encoding="gb18030", low_memory=False)

    df = pd.DataFrame(file)
    df1 = pd.DataFrame(fileout)

    havecodelist = list(df1['song_id'])


    confidence_s =[]
    positive_prob_s=[]
    negative_prob_s=[]
    sentiment_s =[]

    n = len(df) # n=233243

    for i in range(n):
        for iii in range(10000):
            #if i%50 == 0:
            print(Name+"  歌词情感分析进度：{:.2f}%".format(100*i/n),end="\n")
            document = df[i:i+1]
            #print(document['song_id'][i])
            song_id = document['song_id'][i]
            if song_id not in havecodelist:
                song_name = document['song_name'][i]
                song_songer = document['song_songer'][i]
                song_publishTime = document['song_publishTime'][i]

                lyric = str(document['song_lyric'][i]).replace(";","").replace("?","")
                #print(lyric)
                if Name=='中文说唱':
                    if len(lyric)>1000:
                        lyric = lyric[:1000]
                elif  Name=='英文说唱':
                    if len(lyric) > 1000:
                        lyric = lyric[:1000]

                if (i+1)%20==0:
                    time.sleep(1)
                if lyric =='\n' or lyric=='' or lyric== '\n\n':
                    lyric = 'NA'
                params = {'text':lyric}
                if Name == '中文说唱':
                    encoded_data = json.dumps(params).encode('GBK')
                elif Name == '英文说唱':
                    encoded_data = json.dumps(params).encode('UTF-8')
                # print(encoded_data)
                # exit(1)
                request=http.request('POST',
                                      url,
                                      body=encoded_data,
                                      headers={'Content-Type':'application/json'})
                if Name == '中文说唱':
                    result = str(request.data,'GBK')
                elif Name == '英文说唱':
                    result = str(request.data, 'UTF-8')
                #print(result)
                a =json.loads(result)
                try:
                    a1 =a['items'][0]
                except Exception as e:
                    print('请求超频，休眠1秒'+result)
                    time.sleep(1)
                    continue
                #print(a1)
                sentiment_s.append(a1['sentiment'])
                positive_prob_s.append(a1['positive_prob'])
                negative_prob_s.append(a1['negative_prob'])  #
                confidence_s.append(a1['confidence'])  #

                #print(a1)
                data1 = pd.DataFrame({'song_id':song_id,
                                      'song_name':song_name,
                                      'song_songer':song_songer,
                                      'song_publishTime':song_publishTime,
                                      'sentiment':a1['sentiment']-1,
                                     'confidence':a1['confidence'],
                                     'positive_prob': a1['positive_prob'],
                                     'negative_prob': a1['negative_prob']},
                                     columns = ['song_id',
                                                'song_name',
                                                'song_songer',
                                                'song_publishTime',
                                                'sentiment',
                                                'confidence',
                                                'positive_prob',
                                                'negative_prob'], index=[0])
                data1.to_csv(local_main2, index = None, mode = 'a', header = None, sep = ',', encoding = "utf_8_sig")
                break
            else:
                break
#RAP_sentiment('中文说唱')
#RAP_sentiment('英文说唱')