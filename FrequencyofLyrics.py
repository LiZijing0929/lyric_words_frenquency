
# coding: utf-8

import re
from bs4 import BeautifulSoup
import requests
import time
from collections import Counter


time.sleep(5)  
#proxies={'http':'http://203.146.82.253:3128','http':'http://145.239.93.189:80','http':'http://203.74.4.7:80','http':'http://36.83.69.97:80'}
proxies={'http':'http://178.62.51.6:8118','http':'http://180.254.192.31:9000','http':'http://5.189.133.231:80'}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36' }

#home page of the artist
name=re.sub(r' ','-',str(input("Singer's name").title()))
url="https://www.musixmatch.com/artist/"+name

#get the complete song list
urlset=[url+"/{}".format(i) for i in range(1, 10)]
lyric_dict={}
for url_forload in urlset:
    ty=requests.get(url_forload,headers=headers,proxies=proxies)
    time.sleep(3)
    tysoup=BeautifulSoup(ty.content,"lxml")
    finalsoup=tysoup.find_all("a",class_="title")
    
    #find tags contain links of songs  
    for tag in finalsoup:
        links=tag.get("href")
        if (re.search(".*((remix)|(acoustic)|(edition)|(feat.)).*",links))==None:
            #get rid of same songs            
            lyric_dict[re.sub("/lyrics","https://www.musixmatch.com/lyrics",links)]=_
            #requests only understands links start with "http"
        if tysoup.find(class_='empty')!=None:
            #stop reading when there's no more song 
            break

print(lyric_dict)    


#get a list of lyrics to process later        
        

def get_lyric_musix(url):
    music_soup=BeautifulSoup(url,'lxml')    
    music_content=music_soup.find_all(class_='mxm-lyrics__content')
    return ([content.get_text() for content in music_content])

print(lyric_dict)

for url in list(lyric_dict.keys()):
    tycontent=requests.get(url,proxies=proxies,headers=headers).content
    time.sleep(3)
    finalsoup=get_lyric_musix(tycontent)
    lyric_dict[url]=re.sub("\s+"," ",re.sub(r"[!?,.\"']","",re.sub(r"\n"," ","".join(finalsoup)))).lower()
    
    #remove useless parts
    
#get every single word to count frequency
lyricswords=[]
lyricswords_1=[]
for lyric in lyric_dict.values():
    lyricswords=lyricswords + list(set(sorted(lyric.split(' ')))) #unique words in one song
    lyricswords_1=lyricswords_1+lyric.split(' ')
#the 300 most frequent words    
ly_frenquency=Counter(sorted(lyricswords)).most_common(300)
ly_frenquency_1=Counter(sorted(lyricswords_1)).most_common(300)
for item in ly_frenquency:
    print(re.sub(r"[()']",'',str(item)))
print('Count every words in every song and the result will be:')
for item in ly_frenquency_1:
    print(re.sub(r'[()]','',str(item)))
