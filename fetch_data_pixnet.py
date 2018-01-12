def convert_to_json_attributes(file_name):
    count = 1
    dict_list = dict()
    with open(file_name,"r") as pixnet_file :
        pixnet_data = csv.DictReader(pixnet_file)
        for line in pixnet_data:
            dict_list["第"+str(count)+"筆"] = dict()
            for key,value in line.items() :
                dict_list["第"+str(count)+"筆"][key] = value
            count = count + 1

    with open ( "converted_pixnet_data/"+file_name[17:-4]+".json" ,"w") as file_converted :
        file_converted.write(json.dumps(dict_list,ensure_ascii=False,indent=4))
        file_converted.close()

def convert_to_json_content(file_name):
    count = 1
    dict_list = dict()
    with open(file_name,"r") as pixnet_file :
        pixnet_data = csv.DictReader(pixnet_file)
        for line in pixnet_data:
            dict_list["第"+str(count)+"筆"] = dict()
            for key,value in line.items() :
                dict_list["第"+str(count)+"筆"][key] = value
            count = count + 1

    with open ( "converted_pixnet_data/"+file_name[14:-4]+".json" ,"w") as file_converted :
        file_converted.write(json.dumps(dict_list,ensure_ascii=False,indent=4))
        file_converted.close()

def fetch_data_attributes(file_name):
    with open(file_name,"r") as pixnet_file :
        pixnet_data = json.loads(pixnet_file.read())
        jieba_cut_attributes(pixnet_data,"title")
        save_file(file_name,count_data,"title")

def fetch_data_content(file_name):
    with open(file_name,"r") as pixnet_file :
        pixnet_data = json.loads(pixnet_file.read())
        jieba_cut_content(pixnet_data,"content")
        save_file(file_name,count_data,"content")

def jieba_cut_attributes(each_kinds,name):
    segment = str()
    punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。n、＠@#$%^&* ＝】【+‧》|《」「／『』．★－│▌＊─☆▋｜（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    for each_id,each_content in each_kinds.items() :
        for small_title , small_content in each_content.items() :
            if small_title == name :
                segment = ""
                no_punct = ""
                content = small_content
                if content == None :
                    segment = ""
                else :
                    for char in content:
                       if char not in punctuations:
                           no_punct = no_punct + char

                    segment = jieba.cut(no_punct, cut_all=False)
            else :
                pass

            check_count(segment,name)

def jieba_cut_content(each_kinds,name):
    segment = str()
    punctuations = '''。🤓🏻!！^___^……~，　►()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝】n【+‧》|《」「／『』．★－│▌＊─☆▋｜（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
    for each_id,each_content in each_kinds.items() :
        for small_title , small_content in each_content.items() :
            if small_title == name :
                segment = ""
                no_punct = ""
                soup = BeautifulSoup(small_content, 'html.parser')
                content_span = soup.find_all('span')
                content_p = soup.find_all('p')
                content_strong = soup.find_all('strong')
                for span in content_span:
                    content = span.text
                    print(content)
                    if content == None :
                        segment = "null"
                    else :
                        for char in content:
                           if char not in punctuations:
                               no_punct = no_punct + char
                for p in content_p:
                    content = p.text
                    print(content)
                    if content == None :
                        segment = "null"
                    else :
                        for char in content:
                           if char not in punctuations:
                               no_punct = no_punct + char
                for strong in content_strong:
                    content = strong.text
                    print(content)
                    if content == None :
                        segment = "null"
                    else :
                        for char in content:
                           if char not in punctuations:
                               no_punct = no_punct + char

                segment = jieba.cut(no_punct, cut_all=False)
            else :
                pass

            check_count(segment,name)

def check_count(segment,name):
    global count_data
    for x in segment:
        if x not in count_data:
            count_data[x] = 1
        else:
            count = count_data.get(x)
            count_data[x] = count + 1

def save_file(file_name,data,name):
    for key, value in data.copy().items():
        if int(value) < 10:
            del data[key]
    with open ( "Pixnet_data_count/" + file_name[22:-5] + "_count_jieba.json","w") as count :
        ordered_data = sorted(data.items(), key=lambda x:(-x[1], x[0]))
        count.write(json.dumps(OrderedDict(ordered_data),ensure_ascii=False,indent=4))
        count.close()
    count_data = dict()

import csv,json,jieba,glob,sys
from collections import OrderedDict
from bs4 import BeautifulSoup
if __name__ == "__main__":
    jieba.set_dictionary("data/dict.txt.big")
    csv.field_size_limit(sys.maxsize)

    # file name and dataset here
    attributes_filename = "pixnet_attributes/*.csv"
    attributes_each = glob.glob(attributes_filename)
    content_filename = "pixnet_content/*.csv"
    content_each = glob.glob(content_filename)

    #define a dict for counted data
    count_data = dict()

    for file_name in attributes_each :
        #convert csv to json
        convert_to_json_attributes(file_name)
        #fetch and get each document of ppt_japan_data
        fetch_data_attributes("converted_pixnet_data/"+file_name[18:-4]+".json")

    for file_name in content_each :
        #convert csv to json
        convert_to_json_content(file_name)
        #fetch and get each document of ppt_japan_data
        fetch_data_content("converted_pixnet_data/"+file_name[15:-4]+".json")
