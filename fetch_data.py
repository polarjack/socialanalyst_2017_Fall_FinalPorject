def fetch_data(file_name):
    with open(file_name,"r") as ppt_file :
        ppt_data = json.loads(ppt_file.read())
        articles = ppt_data["articles"]
        jieba_cut(articles,"article_title")
        save_file(count_data,"article_title")
        jieba_cut(articles,"content")
        save_file(count_data,"content")
        jieba_cut_for_messages(articles,"messages")
        save_file(count_data,"push_content")

def jieba_cut_for_messages(articles,kind):
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    for length in range(len(articles)) :
        no_punct = ""
        segment = ""
        messages = articles[length][kind]
        jieba_cut(messages,"push_content")


def jieba_cut(articles,name):
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    for length in range(len(articles)) :
        no_punct = ""
        segment = ""
        title = articles[length][name]
        if title == None :
            segment = "null"
        else :
            for char in  title:
               if char not in punctuations:
                   no_punct = no_punct + char

            segment = jieba.cut(no_punct, cut_all=False)

        check_count(segment,name)

def check_count(segment,name):
    global count_data
    for x in segment:
        if x not in count_data:
            count_data[x] = 1
        else:
            count = count_data.get(x)
            count_data[x] = count + 1

def save_file(data,name):
    global count_data
    for key, value in data.copy().items():
        if int(value) < 10:
            del data[key]
    with open ( "PPT_japan_data_jieba/" + name + "_count_jieba.json","w") as count :
        ordered_data = sorted(data.items(), key=lambda x:(-x[1], x[0]))
        #print(ordered_data)
        count.write(json.dumps(OrderedDict(ordered_data),ensure_ascii=False,indent=4))
        count.close()
    print(count_data)
    count_data = dict()
    print(count_data)

import csv,json,jieba
from collections import OrderedDict
if __name__ == "__main__":
    # jieba.set_dictionary("data/dict.txt.big")

    jieba.load_userdict("userdict.txt")
    # file name here
    file_name = "ppt_japan_data.json"

    #define a dict for counted data
    count_data = dict()

    # fetch and get each document of ppt_japan_data
    fetch_data(file_name)
