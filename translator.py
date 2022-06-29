from googletrans import Translator

def googleTranslator(user_input, src='auto', dest='zh-TW'):
    """translate input string
    以google翻譯將text翻譯為目標語言

    :param user_input: 要翻譯的字串，接受UTF-8編碼。
    :param src: 輸入語言
    :param dest: 要翻譯的目標語言，參閱googletrans.LANGCODES語言列表。
    """
    translator = Translator()
    # Translate
    results = translator.translate(user_input,src=src ,dest=dest)
    
    return results.text