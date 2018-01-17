##取得『 json 』檔案的資料，並『 load 』進來後，做斷詞，且將統計斷詞後的結果，個別存成新檔
def fetch_data(file_name):
    with open(file_name,"r") as ppt_file :
        ppt_data = json.loads(ppt_file.read())
        articles = ppt_data["articles"]

        #取得『 article_title 』的資料，並儲存
        jieba_cut(articles,"article_title")
        save_file(count_data,"article_title")

        #取得『 content 』的資料，並儲存
        jieba_cut(articles,"content")
        save_file(count_data,"content")

        #取得『 messages 』的資料，並儲存
        jieba_cut_for_messages(articles,"messages")
        save_file(count_data,"push_content")

#特地處理『 messgaes 』中的資料，找出『 push_content 』
def jieba_cut_for_messages(articles,kind):

    #將標點符號或是不必要的字列成字串，每筆文字資料將與之作比對
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    punctuations += "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわをんがぎぐげござじずぜぞだぢずでどばびぶべぼぱぴぷぺぽきゃきゅきょぎゃぎゅぎょしゃしゅしょじゃじゅじょちゃちゅちょにゃにゅにょひゃひゅひょびゃびゅびょぴゃぴゅぴょみゃみゅみょりゃりゅりょ"
    punctuations += "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨワヲンガギグゲゴザジズゼゾダヂズデドバビブベボパピプペポキャキュキョギャギュギョシャシュショジャジュジョチャチュチョニャニュニョヒャヒュヒョビャビュビョピャピュピョミャミュミョリャリュリョ"
    punctuations += "ヴるっれらろüルラヶレ㈱ッァ】×ィ\\n"
    punctuations += "【 『』「」（），。；、？％︿＆＊＄＃＠＠！～—｜＼"
    punctuations += "abcdefghijklmnopqrstuvwxyz"

    #依序處理每筆資料
    for length in range(len(articles)) :
        no_punct = ""
        segment = ""
        messages = articles[length][kind]

        #將之進行斷詞
        jieba_cut(messages,"push_content")

#將資料進行斷詞
def jieba_cut(articles,name):

    #將標點符號或是不必要的字列成字串，每筆文字資料將與之作比對
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    punctuations += "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわをんがぎぐげござじずぜぞだぢずでどばびぶべぼぱぴぷぺぽきゃきゅきょぎゃぎゅぎょしゃしゅしょじゃじゅじょちゃちゅちょにゃにゅにょひゃひゅひょびゃびゅびょぴゃぴゅぴょみゃみゅみょりゃりゅりょ"
    punctuations += "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨワヲンガギグゲゴザジズゼゾダヂズデドバビブベボパピプペポキャキュキョギャギュギョシャシュショジャジュジョチャチュチョニャニュニョヒャヒュヒョビャビュビョピャピュピョミャミュミョリャリュリョ"
    punctuations += "ヴるっれらろüルラヶレ㈱ッァ】×ィ\\n"
    punctuations += "【 『』「」（），。；、？％︿＆＊＄＃＠＠！～—｜＼"
    punctuations += "abcdefghijklmnopqrstuvwxyz"

    #依序處理每筆資料
    for length in range(len(articles)) :
        no_punct = ""
        segment = ""

        #取得內容
        title = articles[length][name]

        #如果 content 為 None，則給予空值
        if title == None :
            segment = ""
        else :

            #檢查值裡面有沒有 punctuations
            for char in  title:
               if char not in punctuations:
                   no_punct = no_punct + char

            #將該段內容篩選過後的文字資料進行斷詞
            segment = jieba.cut(no_punct, cut_all=False)

        #將斷詞結果統計並存在 dict 裡面
        check_count(segment,name)

#將斷完詞後的結果，進行統計，存在『 count_data 』的 dict 裡面
def check_count(segment,name):
    global count_data
    for x in segment:

        #若一開始不在字典內，則給予初始值
        if x not in count_data:
            count_data[x] = 1

        #若在字典內，則進行累加
        else:
            count = count_data.get(x)
            count_data[x] = count + 1

#將 count_data 的 json 存成字典格式
def save_file(data,name):
    global count_data

    #將 count_data 中，數量少於 10 的資料刪掉
    #for key, value in data.copy().items():
    #    if int(value) < 10:
    #        del data[key]

    #最後將結果存成一個新的檔，並重新命名
    with open ( "PPT_japan_data_jieba/" + name + "_count_jieba.json","w") as count :
        ordered_data = sorted(data.items(), key=lambda x:(-x[1], x[0]))
        count.write(json.dumps(OrderedDict(ordered_data),ensure_ascii=False,indent=4))
        count.close()

    #將 count_data 重新選告為空字典
    count_data = dict()

#引進相關會用到的函式庫
import csv,json,jieba,facebook,re
from collections import OrderedDict
if __name__ == "__main__":

    #建立詞庫（字典）
    jieba.set_dictionary("data/dict.txt.big")
    jieba.load_userdict("data/userdict.txt")

    # file name here
    file_name = "ptt_after_filt.json"

    #define a dict for counted data
    count_data = dict()

    # fetch and get each document of ppt_japan_data
    fetch_data(file_name)
