#Lyrics sentiment analysis
#Baidu sentiment analysis API interface

'''
API call description

Request parameter
Parameter Type Description
text string text content, maximum 2048 bytes

Return parameter
Parameter Description Description
log_id uint64 Request unique identification code
sentiment int represents the result of sentiment polarity classification, 0: negative, 1: neutral, 2: positive
Confidence float represents the confidence of the classification, the value range is [0,1]
positive_prob float represents the probability of belonging to the positive category, the value range is [0,1]
negative_prob float represents the probability of belonging to the negative category, the value range is [0,1]

Note:
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
    # sentiment
     # int
     # Indicates the result of emotional polarity classification, -1: negative, 0: neutral, 1: positive
     # confidence
     # float
     # Indicates the confidence of classification, the range of values is [0, 1]
     # positive_prob
     # float
     # Indicates the probability of belonging to the positive category, the value range is [0, 1]
     # negative_prob
     # float
     # Indicates the probability of belonging to the negative category, the value range is [0, 1]
    local_main2 = './res/'+Name+'-Emotion_classification.csv'
    if not os.path.exists(local_main2):
        # Download playlist recursively
        data = pd.DataFrame(columns = ['song_id','song_name','song_songer','song_publishTime','sentiment','confidence','positive_prob','negative_prob'])
        data.to_csv(local_main2, index = None, encoding = 'utf_8_sig')
    else:
        print(Name+' Emotion analysis result file exists.')
        return
    access_token='24.65051f487401f5c9d61249a0aa7634dd.2592000.1609323856.282335-23069052' 
    http=urllib3.PoolManager()
    if Name=='Chinese_Rap':
        url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token='+access_token
    elif Name=='English_Rap':
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
            print(Name+"  Emotional analysis progress of lyrics：{:.2f}%".format(100*i/n),end="\n")
            document = df[i:i+1]
            #print(document['song_id'][i])
            song_id = document['song_id'][i]
            if song_id not in havecodelist:
                song_name = document['song_name'][i]
                song_songer = document['song_songer'][i]
                song_publishTime = document['song_publishTime'][i]

                lyric = str(document['song_lyric'][i]).replace(";","").replace("?","")
                #print(lyric)
                if Name=='Chinese_Rap':
                #API call has a character limit, 2048 bytes, which is 1024 Chinese characters. 
                # To be conservative, if the number of lyrics exceeds 1000 characters, 
                # only the first 1000 characters are used for calculation
                    if len(lyric)>1000:
                        lyric = lyric[:1000]
                elif  Name=='English_Rap':
                    if len(lyric) > 1000:
                        lyric = lyric[:1000]

                if (i+1)%20==0:
                    time.sleep(1)
                if lyric =='\n' or lyric=='' or lyric== '\n\n':
                    lyric = 'NA'
                params = {'text':lyric}
                if Name == 'Chinese_Rap':
                    encoded_data = json.dumps(params).encode('GBK')
                elif Name == 'English_Rap':
                    encoded_data = json.dumps(params).encode('UTF-8')
                # print(encoded_data)
                # exit(1)
                request=http.request('POST',
                                      url,
                                      body=encoded_data,
                                      headers={'Content-Type':'application/json'})
                if Name == 'Chinese_Rap':
                    result = str(request.data,'GBK')
                elif Name == 'English_Rap':
                    result = str(request.data, 'UTF-8')
                #print(result)
                a =json.loads(result)
                try:
                    a1 =a['items'][0]
                except Exception as e:
                    print('Request overclocking, sleep for 1 second'+result)
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
