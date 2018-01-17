# 說明
```
這是社群與媒體資料分析第一組期末專題資料處理的部份
題目：東京奧運你打算怎麼玩
```

# 擁有的資料
```
1. 痞客邦PIXNET
敘述： 痞客邦提供之資料（這部份之後會再補上因為痞客邦他們有給一份很完整的欄位說明，我們使用的是6～8月的資料


2. PTT Japan_Travel
敘述：藉由<https://github.com/jwlin/ptt-web-crawler.git> 抓取6～8月份的資料，詳細的區間並不準確因為是用文章編號在抓並不是用時間

3. 景點名稱，經緯度
由兩位組員手動蒐集867個景點，非常辛苦
```

# Main Idea
```
目標：將我們所獲得的景點進行Rating

作法：在我們擁有的資料當中基本上幾乎都是字，因此我們的作法就是做text mining，用類似IR 的方式去尋找我們的Recall，
這邊我們使用的作法是借用tf-idf 的想法做term_count，我們是藉由景點的名稱作為relevant document的基礎，
不過由於景點名稱並不一定存在於pixnet 或是ptt 的文本裡面，所以我們先把我們需要的文本先切出來然後去找relevant 的文章（用標題去做match），
藉此獲得我們定義的relevant document，那獲得了relevant document 之後再把content 抽出來（也就是文章內容），變成新的文本，
然後反向把景點名稱一個一個下去找，做term_count這樣我們就可以獲得排名。
```


# Step 1 csv to json
```
csv 對於程式來說（javascript, python ）是個很難讀的東西，我跟我的組員們基本上都偏好用JSON所以就全部先parse 成JSON，這邊處理的只有pixnet的部份因為ptt 爬下來就已經是json了
```

# Step 2 Work Tokenize through Jieba
```
先處理景點的斷詞，想法是把景點的名稱斷詞然後建成一個term_counts 的base，以代表我們所想要獲得的資訊
``` 

