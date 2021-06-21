import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import csv
import time
import random

n = input("請輸入新的csv檔名稱:")
#讀取檔案
data_name = []
with open("Organisms-for-RNA-Seq-pipeline.csv", 'r', encoding='utf-8-sig', errors='ignore') as f:
    csvReader = csv.DictReader(f)#讀出是字典
    for data in csvReader:
        # print(data["organism"])
        data_name.append(data["organism"])
 
change_id_name = []
for i in range(len(data_name)):
    change_id_name.append(data_name[i].replace(" ","+")) 
# print(change_id_name)   #['Amyelois+transitella', 'Zeugodacus+cucurbitae',...]


def main():
    baseurl = "https://www.ncbi.nlm.nih.gov/taxonomy/?term="
    #1.爬取網页
    toxid = getData(baseurl)
    print(toxid)
    savedata(n)


#爬取網页   
def getData(baseurl):
    datalist = []
    for i in range(len(change_id_name)):
        url = baseurl+change_id_name[i]
        html = askURL(url) 
    # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        # pattern = r"ncbi_uid=(\d+)"
        # result = re.search(pattern,soup)#soup不行，要str
        # for item in result:
        #     print(result.group(1))
        for item in soup.find_all('div',class_="rprt"): 
            # data = []
            item = str(item)
            pattern = r"ncbi_uid=(\d+)"
            result = re.search(pattern,item)
            datalist.append(result.group(1))
            

    return datalist        

#得到指定一个URL的網页内容
def askURL(url):
    head = {                #模拟瀏覽器信息，向伺服器發送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    # request = requests.get(url,headers=head)
    request = urllib.request.Request(url,headers=head)
    time.sleep(random.uniform(1, 5))# [WinError 10054] 遠端主機已強制關閉一個現存的連線。，你的網路IP被訪問的主機踢掉
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except Exception as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#創立新的CSV檔案
def savedata(newcsv):
    with open('Organisms-for-RNA-Seq-pipeline.csv', 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        ans=[]
        for i in lines:
            ans.append(i.strip().split(','))
        
    with open("%s"%newcsv, 'w', encoding='utf-8') as f2:
        for i in range(len(ans)):
            if i ==0: f2.writelines(','.join(ans[i])+'\n')
            else:
                ans[i][2] = toxid[i-1]
                f2.writelines(','.join(ans[i])+'\n')
                # print(ans)
    print("檔案存入成功")

#當程式進行時
if __name__ == "__main__":          
#調用函数
    main()
    print("爬取完畢！")

# [WinError 10054] 遠端主機已強制關閉一個現存的連線。*N
# 你的網路IP被訪問的主機踢掉

# [WinError 10060] 連線嘗試失敗，因為連線對象有一段時間並未正確回應，或是連線建立失敗，因為連線的主機無法回應。
# ['28588', '27457', '7038', 有些被關掉

"""
# 以正規表示法比對超連結網址
 </div>
        <div><div class="rprt"><p class="title"><a href="/Taxonomy/Browser/wwwtax.cgi?id=680683" ref="ncbi_uid=680683&amp;link_uid=680683&amp;ordinalpos=1"><b>Amyelois transitella</b></a></p><div class="supp"><p class="desc">species, moths</p></div><div class="aux"><p class="links"><a class="dblinks" href="/nucleotide?term=txid680683[Organism]" ref="ordinalpos=1">Nucleotide</a> <a class="dblinks" href="/protein?term=txid680683[Organism]" ref="ordinalpos=1">Protein</a> </p></div></div></div>
        <div id="messagearea_bottom"
"""