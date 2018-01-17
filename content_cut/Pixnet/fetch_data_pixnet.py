#將痞客邦資料中『 attributes 』的『 CSV 』轉型成『 json  』格式
def convert_to_json_attributes(file_name):
    count = 1
    dict_list = dict()

    #將『 key 』設成『 第 X 筆 』
    with open(file_name,"r") as pixnet_file :
        pixnet_data = csv.DictReader(pixnet_file)

        #將原始檔案中的每行資料讀進每個 key 成為 value 值
        for line in pixnet_data:
            dict_list["第"+str(count)+"筆"] = dict()
            for key,value in line.items() :
                dict_list["第"+str(count)+"筆"][key] = value
            count = count + 1

    #最後將結果存成一個新的檔，並重新命名
    with open ( "converted_pixnet_data/"+file_name[17:-4]+".json" ,"w") as file_converted :
        file_converted.write(json.dumps(dict_list,ensure_ascii=False,indent=4))
        file_converted.close()

#將痞客邦資料中『 content 』的『 CSV 』轉型成『 json  』格式
def convert_to_json_content(file_name):
    count = 1
    dict_list = dict()

    #將『 key 』設成『 第 X 筆 』
    with open(file_name,"r") as pixnet_file :
        pixnet_data = csv.DictReader(pixnet_file)

        #將原始檔案中的每行資料讀進每個 key 成為 value 值
        for line in pixnet_data:
            dict_list["第"+str(count)+"筆"] = dict()
            for key,value in line.items() :
                dict_list["第"+str(count)+"筆"][key] = value
            count = count + 1

    #最後將結果存成一個新的檔，並重新命名
    with open ( "converted_pixnet_data/"+file_name[14:-4]+".json" ,"w") as file_converted :
        file_converted.write(json.dumps(dict_list,ensure_ascii=False,indent=4))
        file_converted.close()

#取得『 attributes json 』檔案的資料，並『 load 』進來後，做斷詞，且將統計斷詞後的結果，個別存成新檔
def fetch_data_attributes(file_name):
    with open(file_name,"r") as pixnet_file :

        #讀檔案
        pixnet_data = json.loads(pixnet_file.read())

        #將資料斷詞
        jieba_cut_attributes(pixnet_data,"title")

        #另存新檔
        save_file(file_name,count_data,"title")

##取得『 content json 』檔案的資料，並『 load 』進來後，做斷詞，且將統計斷詞後的結果，個別存成新檔
def fetch_data_content(file_name):
    with open(file_name,"r") as pixnet_file :

        #讀檔案
        pixnet_data = json.loads(pixnet_file.read())

        #將資料斷詞
        jieba_cut_content(pixnet_data,"content")

        #另存新檔
        save_file(file_name,count_data,"content")

#專門處理 attributes_after 的 json 資料
def fetch_data_content_after(content_file_name,attr_file_name):
    pixnet_attr = dict()
    pixnet_content = dict()

    #打開 attributes_after，抓出資料
    with open(attr_file_name,"r") as pixnet_attr_file:

        #讀檔案
        pixnet_attr = json.loads(pixnet_attr_file.read())

    #打開 content，抓出資料
    with open(content_file_name,"r") as pixnet_content_file :

        #讀檔案
        pixnet_content = json.loads(pixnet_content_file.read())

    #將 attributes 跟 content 檔案進行比對
    final_match = match_content(pixnet_attr,pixnet_content)

    #將資料斷詞
    jieba_cut_content(final_match,"content")

    #另存新檔
    save_file(content_file_name,count_data,"content")

#比對資料，把符合 filter_after json 檔的 content 資料抓出來，丟進一個 dict ，並回傳
def match_content(pixnet_attr,pixnet_content):
    final_match = dict()
    for attr_key,attr_value in pixnet_attr.items():
        for content_key,content_value in pixnet_content.items():
            if attr_key == content_key :
                final_match[attr_key] = content_value
                print(attr_key + " : {")
                print(content_value)
                print("}")
                break
    return final_match

#將『 attributes 』的資料進行斷詞
def jieba_cut_attributes(each_kinds,name):
    segment = str()

    #將標點符號或是不必要的字列成字串，每筆文字資料將與之作比對
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    punctuations += "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわをんがぎぐげござじずぜぞだぢずでどばびぶべぼぱぴぷぺぽきゃきゅきょぎゃぎゅぎょしゃしゅしょじゃじゅじょちゃちゅちょにゃにゅにょひゃひゅひょびゃびゅびょぴゃぴゅぴょみゃみゅみょりゃりゅりょ"
    punctuations += "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨワヲンガギグゲゴザジズゼゾダヂズデドバビブベボパピプペポキャキュキョギャギュギョシャシュショジャジュジョチャチュチョニャニュニョヒャヒュヒョビャビュビョピャピュピョミャミュミョリャリュリョ"
    punctuations += "ヴるっれらろüルラヶレ㈱ッァ】×ィ\\n"
    punctuations += "【 『』「」（），。；、？％︿＆＊＄＃＠＠！～—｜＼"
    punctuations += "abcdefghijklmnopqrstuvwxyz"

    #依序處理每筆資料
    for each_id,each_content in each_kinds.items() :
        for small_title , small_content in each_content.items() :

            #處理『 key 』為 title 的 value 值
            if small_title == name :
                segment = ""
                no_punct = ""
                content = small_content

                #如果 content 為 None，則給予空值
                if content == None :
                    segment = ""
                else :

                    #檢查值裡面有沒有 punctuations
                    for char in content:
                       if char not in punctuations:
                           no_punct = no_punct + char

                    #將篩選過字句的結果進行斷詞
                    segment = jieba.cut(no_punct, cut_all=False)
            else :
                pass

            #將斷詞結果統計並存在 dict 裡面
            check_count(segment,name)

#將『 content 』的資料進行斷詞
def jieba_cut_content(each_kinds,name):
    segment = str()

    #將標點符號或是不必要的字列成字串，每筆文字資料將與之作比對
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    punctuations += "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわをんがぎぐげござじずぜぞだぢずでどばびぶべぼぱぴぷぺぽきゃきゅきょぎゃぎゅぎょしゃしゅしょじゃじゅじょちゃちゅちょにゃにゅにょひゃひゅひょびゃびゅびょぴゃぴゅぴょみゃみゅみょりゃりゅりょ"
    punctuations += "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨワヲンガギグゲゴザジズゼゾダヂズデドバビブベボパピプペポキャキュキョギャギュギョシャシュショジャジュジョチャチュチョニャニュニョヒャヒュヒョビャビュビョピャピュピョミャミュミョリャリュリョ"
    punctuations += "ヴるっれらろüルラヶレ㈱ッァ】×ィ\\n"
    punctuations += "【 『』「」（），。；、？％︿＆＊＄＃＠＠！～—｜＼"
    punctuations += "abcdefghijklmnopqrstuvwxyz"

    #依序處理每筆資料
    for each_id,each_content in each_kinds.items() :
        for small_title , small_content in each_content.items() :

            #處理『 key 』為 title 的 value 值
            if small_title == name :
                segment = ""
                no_punct = ""

                #用 beautiful soup 將 content 中的 html 文字 parse 成 hmtl tag
                soup = BeautifulSoup(small_content, 'html.parser')

                #找到所有含有『 span 』tag 的文字、字句
                content_span = soup.find_all('span')

                #找到所有含有『 p 』tag 的文字、字句
                content_p = soup.find_all('p')

                #找到所有含有『 strong 』tag 的文字、字句
                content_strong = soup.find_all('strong')

                #依序找所有含有『 span 』tag 的文字、字句
                for span in content_span:
                    content = span.text
                    print(content)

                    #如果 content 為 None，則給予空值
                    if content == None :
                        segment = ""
                    else :

                        #檢查值裡面有沒有 punctuations
                        for char in content:
                           if char not in punctuations:
                               no_punct = no_punct + char

                #依序找所有含有『 p 』tag 的文字、字句
                for p in content_p:
                    content = p.text
                    print(content)

                    #如果 content 為 None，則給予空值
                    if content == None :
                        segment = ""
                    else :

                        #檢查值裡面有沒有 punctuations
                        for char in content:
                           if char not in punctuations:
                               no_punct = no_punct + char

                #依序找所有含有『 strong 』tag 的文字、字句
                for strong in content_strong:
                    content = strong.text
                    print(content)

                    #如果 content 為 None，則給予空值
                    if content == None :
                        segment = ""
                    else :

                        #檢查值裡面有沒有 punctuations
                        for char in content:
                           if char not in punctuations:
                               no_punct = no_punct + char

                #將該段內容篩選過後且 parse 過後的文字資料進行斷詞
                segment = jieba.cut(no_punct, cut_all=False)
            else :
                pass

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
def save_file(file_name,data,name):

    #將 count_data 中，數量少於 10 的資料刪掉
    #for key, value in data.copy().items():
    #    if int(value) < 10:
    #        del data[key]

    #最後將結果存成一個新的檔，並重新命名
    with open ( "Pixnet_data_count/" + file_name[22:-5] + "_count_jieba_after.json","w") as count :
        ordered_data = sorted(data.items(), key=lambda x:(-x[1], x[0]))
        count.write(json.dumps(OrderedDict(ordered_data),ensure_ascii=False,indent=4))
        count.close()

    #將 count_data 重新選告為空字典
    count_data = dict()

#引進相關會用到的函式庫
import csv,json,jieba,facebook,re,glob,sys
from collections import OrderedDict
from bs4 import BeautifulSoup
if __name__ == "__main__":

    #建立詞庫（字典）
    jieba.set_dictionary("data/dict.txt.big")
    jieba.load_userdict("data/userdict.txt")

    #讓『 大量 』資料可以讀
    csv.field_size_limit(sys.maxsize)

    # file name and dataset here
    attributes_filename = "pixnet_attributes/*.csv"
    attributes_each = glob.glob(attributes_filename)
    pixnet_filename_after = "converted_pixnet_data_after/*.json"
    pixnet_each_after = glob.glob(pixnet_filename_after)
    content_filename = "pixnet_content/*.csv"
    content_each = glob.glob(content_filename)
    file_index = 0
    #define a dict for counted data
    count_data = dict()

    #for file_name in attributes_each :

    #    #convert csv to json
    #    convert_to_json_attributes(file_name)

    #    #fetch and get each document of ppt_japan_data
    #    fetch_data_attributes("converted_pixnet_data/"+file_name[18:-4]+".json")

    for file_name in content_each :

        #convert csv to json
        #convert_to_json_content(file_name)

        #fetch and get each document of ppt_japan_data
        #print(pixnet_each_after)
        fetch_data_content_after("converted_pixnet_data/"+file_name[15:-4]+".json",pixnet_each_after[file_index])
        file_index += 1
