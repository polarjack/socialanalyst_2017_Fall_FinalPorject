def targetcut():
  items = json.load(open('target.json'))
  unique_terms = 0

  for (i, item) in enumerate(items["table"]):
    no_punct = ""
    segment = ""
    item = item["title"]
    if item == None:
      segment = ""
    else:
      for char in item:
        if char not in punctuations:
          no_punct = no_punct + char
      
      segment = jieba.cut(no_punct, cut_all=False)
      # print(item + ": ")
      # print(", ".join(segment))
    
    for each in segment:
      if each in output:
        output[each] += 1
      else:
        output[each] = 1
        unique_terms += 1

  # print(unique_terms)
  # print(output)

  # with open('target_cut.json', 'w') as out:
  #   json.dump(output, out)


def pttfunc():
  items = json.load(open('ptt_japan_data.json'))
  unique_terms = 0
  for (i, title) in enumerate(items["articles"]):
    item = title["article_title"]
    no_punct = ""
    if item == None:
      segment = ""
    else:
      for char in item:
        if char not in punctuations:
          no_punct += char
      
      segment = jieba.cut(no_punct, cut_all=False)
      # print(item + ": ")
      # print(", ".join(segment))
    
    for each in segment:
      if each in output:
        ptt["articles"].append(title)
        unique_terms += 1
        break
  
  print(unique_terms)
  with open('ptt_after_filt.json', 'w') as out:
    json.dump(ptt, out)

def pixnetfunc(filename):
  pixnet = {}
  items = json.load(open(filename+".json"))
  # item7 = json.load(open('201707_attributes.json'))
  # item8 = json.load(open('201708_attributes.json'))
  unique_terms = 0
  for (i, index) in enumerate(items):
    item = items[index]["title"]
    article_id = items[index]["article_id"]
    no_punct = ""
    if item == None:
      segment = ""
    else:
      for char in item:
        if char not in punctuations:
          no_punct += char
      
      segment = jieba.cut(no_punct, cut_all=False)
      # print(item + ": ")
      # print(", ".join(segment))
    for each in segment:
      if each in output:
        ouput_index = "第" + str(i) + "筆"
        pixnet[ouput_index] = items[index]
        unique_terms += 1
        break

  print(unique_terms)
  with open(filename+ "_after.json", 'w') as out:
    json.dump(pixnet, out)
  

import jieba, csv, json

punctuations = '''。🤓🏻!！^___^……~，()-[]{};:'"\,<>./?？！。、＠@#$%^&* ＝（）：=_~❤️😅๑・ω～♥”3😱😳😆❤😁💪🏼🤣😊😣😂💪😝😍👍👏😔01234566789的了嗎我你是要去都就也與在很不到吃會好到有們跟後人和想上'''
punctuations += "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわをんがぎぐげござじずぜぞだぢずでどばびぶべぼぱぴぷぺぽきゃきゅきょぎゃぎゅぎょしゃしゅしょじゃじゅじょちゃちゅちょにゃにゅにょひゃひゅひょびゃびゅびょぴゃぴゅぴょみゃみゅみょりゃりゅりょ"
punctuations += "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨワヲンガギグゲゴザジズゼゾダヂズデドバビブベボパピプペポキャキュキョギャギュギョシャシュショジャジュジョチャチュチョニャニュニョヒャヒュヒョビャビュビョピャピュピョミャミュミョリャリュリョ"
punctuations += "ヴるっれらろüルラヶレ㈱ッァ】×ィ\\n"
punctuations += "【 『』「」（），。；、？％︿＆＊＄＃＠＠！～—｜＼"
punctuations += "abcdefghijklmnopqrstuvwxyz"

# pixnet = {}
output = {}
ptt = { "articles": []}

if __name__ == "__main__":
  jieba.load_userdict("userdict.txt")

  targetcut()
  
  # pttfunc()

  pixnetfunc("201706_attributes")
  pixnetfunc("201707_attributes")
  pixnetfunc("201708_attributes")
  