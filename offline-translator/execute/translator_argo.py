import subprocess
from subprocess import PIPE
import pickle
import re
import sys
import opencc
import time
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
terms_dict_path = dir_path+"/terms_dict_all.pickle"

def test_kw_filter():
    user_input_list = ["0", "1", "[2]", "3", "4","5","6","7","8","9","10","11","22","33","44","55"]
    n = 2
    term_n_dict = {'0 1':'0-1', '44 55':'44-55'}
    new_list = filter_keywords(n, user_input_list, term_n_dict)
    print(new_list)
    user_input_list = ["I", "am", "from", "[NTHU CS]", ".","I","love","to","play","game","and","read","papers",".","So","cool"]
    n = 2
    term_n_dict = {'so cool':'poor', "play game":"do research 24/7 until i graduate"}
    new_list = filter_keywords(n, user_input_list, term_n_dict)
    print(new_list)

def bash_execute(from_code, to_code, input_str):
    # bash
    bash_string = f'argos-translate --from-lang {from_code} --to-lang {to_code} "{input_str}"'
    # print(bash_string)
    process = subprocess.Popen(bash_string
                               ,stdout=PIPE, stderr=PIPE, shell=True)
    output, error = process.communicate()
    # print(error)
    process.kill
    translatedText = output.decode('utf8').strip('\n')
    return translatedText

def zhtozhtw(translatedText):
    """turn zh to zh-tw"""
    converter = opencc.OpenCC('s2t')
    translatedText = converter.convert(translatedText)
    return translatedText

def en_string_clean(enString):

    enString = enString.replace(r'"', r"'")
    enString = enString.replace(r'&quot;', r"'")

    return enString
    
def local_f_kw(n, usr_i_list, term_n_dict, new_list):
    """處理 [] 之前的詞，切分, 比對
    待改
    """
    shift = 0
    for it in range(len(usr_i_list)-n+1):
        if it+shift > (len(usr_i_list)-n+1): # 貼上剩餘不足的長度
            new_list.extend(usr_i_list[it+shift:])
            break
        elif shift !=0:
            shift -=1
        else:
            seg = usr_i_list[it:it+n]
            seg_string = " ".join(seg).strip(".")
            # print(seg_string)
            f = 0 # flag of 
            # terms filter
            for term in term_n_dict.keys():
                term = term.lower()
                if seg_string == term:
                    f = 0
                    new_list.append(f"[{term_n_dict[term]}]")
                    shift = n-1
                    break
                else:
                    f = 1
            if f==1: # seg != any term
                shift = 0
                new_list.append(usr_i_list[it])
                # last seg
                if it == (len(usr_i_list)-n):
                    new_list.extend(usr_i_list[it+1:it+n])
    
    return new_list

def filter_keywords(n, user_input_list, term_n_dict):
    """ Return : 
    (ex: n=3) list1 [w1, w2, [zh], w6, w7...]
    """
    # 將輸入，n個字一組
    new_list = []
    ignore_flag = [re.match("\[", s) for s in user_input_list]
    # if None => is able to be pair
    usr_i_list = [] # part of user_input_list, for split latter
    for i in range(len(ignore_flag)):
        if ignore_flag[i] is None: 
            usr_i_list.append(user_input_list[i])
        else:
            if len(usr_i_list) <= n:
                new_list.extend(usr_i_list)
                new_list.append(user_input_list[i]) # 之前處理過的翻譯
                usr_i_list = []
            else:
                # create pair and match with terms
                new_list = local_f_kw(n, usr_i_list, term_n_dict, new_list)
                new_list.append(user_input_list[i])
                usr_i_list = []

    if len(usr_i_list)!=0: # deal with the rest words
        new_list = local_f_kw(n, usr_i_list, term_n_dict, new_list)
    return new_list

def keywords_translator(user_input):
    """read keywords and translate first
    類似遞迴方式從字數長的詞開始過濾，先把英文替換成"[中文翻譯]"後，
    把剩餘沒有翻譯的英文中“[中文翻譯]”替換成[...]，進入argo翻譯，
    完成後依序填回字典翻譯的中文
    """
    user_input_list = user_input.split(" ")
    length = len(user_input_list)

    with open(terms_dict_path, 'rb') as handle:
        terms_dict = pickle.load(handle) # 完整字典
    
    for n in range(length, 0, -1): #一次 拿字典中 所有長度等於n的詞
        try:
            term_n_dict = terms_dict[n]
        except KeyError: # no terms length is n
            continue

        user_input_list = filter_keywords(n, user_input_list, term_n_dict)
        # print(user_input_list)
    
    return user_input_list

def argoTranslator(user_input, src='en', dest='zh'):
    r"""
    情況一：英翻中 ex: en -> (專有名詞翻譯) -> zh
    情況二：非英語之其他語言翻中 ex: kr -> (en -> 專有名詞翻譯) -> zh
    情況三：非英語之其他語言互翻 ex: kr -> (en) -> vi
    Return
    --------
    Translated result
    """
    input_map = {'auto':'en', 'zh-TW':'zh'}
    try:
        from_code = input_map[src]
    except:
        from_code = src
    try:
        to_code = input_map[dest]
    except:
        to_code = dest

    # t1=time.time()
    # situation1 en-> zh
    if from_code=='en' and to_code =='zh':
        user_input = user_input.lower()
        mod_input_list = user_input.split(" ")
        # keywords filter
        mod_input_list = keywords_translator(user_input)
        ignore_flag = [re.match("\[", s) for s in mod_input_list]
        zh_words = []
        mod_input_str = []
        for idx in range(len(ignore_flag)):
            if ignore_flag[idx] == None:
                mod_input_str.append(mod_input_list[idx])
            else:
                zh_words.append(mod_input_list[idx].strip("[").strip("]"))
                mod_input_str.append("[...]") #找到[]先挑掉中文改成[...]

        mod_input_str = " ".join(mod_input_str)
        mod_input_str = en_string_clean(mod_input_str)
        translatedText = bash_execute(from_code, to_code, mod_input_str)
        for zhw in zh_words: #翻譯後，放回中文
            reg = r'\[.*?\]'
            translatedText = re.sub(reg, zhw, translatedText, 1)

    #  situation2 other -> zh
    elif from_code!="en" and to_code =="zh":
        # print('sol 2')
        engTranslatedText = bash_execute(from_code, "en", user_input)
        # print(engTranslatedText)
        # en to zh
        engTranslatedList = engTranslatedText.split(" ")
        # keywords filter
        engTranslatedList = keywords_translator(engTranslatedText)
        ignore_flag = [re.match("\[", s) for s in engTranslatedList]
        zh_words = []
        modEngStr = []
        for idx in range(len(ignore_flag)):
            if ignore_flag[idx] == None:
                modEngStr.append(engTranslatedList[idx])
            else:
                zh_words.append(engTranslatedList[idx].strip("[").strip("]"))
                modEngStr.append("[...]") #找到[]先挑掉中文改成[...]

        modEngStr = " ".join(modEngStr)
        # print(modEngStr)
        modEngStr = en_string_clean(modEngStr)
        # print(modEngStr)
        translatedText = bash_execute("en", to_code, modEngStr)
        # print(translatedText)
        for zhw in zh_words: #翻譯後，放回中文
            reg = r'\[.*?\]'
            translatedText = re.sub(reg, zhw, translatedText, 1)

    #  situation3 other -> other
    else:
        #from_code!="en" and to_code !="zh":
        translatedText = bash_execute(from_code, to_code, user_input)

    if to_code =="zh":
        translatedText = zhtozhtw(translatedText)
    
    # print(time.time()-t1)
    
    return translatedText


def argoTranslatorWithoutDict(user_input, src='en', dest='zh'):
    r"""
    Not using Dictionary
    情況一：英翻中 ex: en -> zh
    Return
    --------
    Translated result
    """
    input_map = {'auto':'en', 'zh-TW':'zh'}
    try:
        from_code = input_map[src]
    except:
        from_code = src
    try:
        to_code = input_map[dest]
    except:
        to_code = dest

    # t1=time.time()
    translatedText = bash_execute(from_code, to_code, user_input)
    if to_code =="zh":
        translatedText = zhtozhtw(translatedText)
    
    # print(time.time()-t1)
    
    return translatedText

# if __name__=="__main__":

#     text = "1995年に放送を開始した「映像の世紀」の新シリーズ。"
#     print(argoTranslatorWithoutDict(text, 'ja', 'zh'))
#     t1=time.time()
#     text = "Office of Taiwan Coordination. Bureau of East Asia and Pacific Affairs. DOS. It is 50 km away from here. They might have nuclear weapons"
#     print(argoTranslatorWithoutDict(text, 'en', 'zh'))
#     print(time.time()-t1)

#     t1=time.time()
#     text = "Office of Taiwan Coordination. Bureau of East Asia and Pacific Affairs. DOS. It is 50 km away from here. They might have nuclear weapons"
#     print(argoTranslator(text, 'en', 'zh'))
#     print(time.time()-t1)

#     print(argoTranslatorWithoutDict('你好', 'zh', 'es'))