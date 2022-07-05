import argostranslate.package, argostranslate.translate
import sys

def argoTranslator(user_input, src='en', dest='zh'):

    input_map = {'auto':'en', 'zh-TW':'zh','zh':'zh', 'en':'en','ja':'ja'}
    from_code = input_map[src]
    to_code = input_map[dest]

    # Error Control
    available_pairs = [('en', 'zh'), ('zh', 'en'),('en', 'ja'),('ja', 'en')]
    pair = (from_code, to_code)
    if pair in available_pairs:
        # Download and install Argos Translate package
        available_packages = argostranslate.package.get_available_packages()
        available_package = list(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )[0]
        download_path = available_package.download()
        argostranslate.package.install_from_path(download_path)

        # # Translate
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(
            lambda x: x.code == from_code,
            installed_languages))[0]
        to_lang = list(filter(
            lambda x: x.code == to_code,
            installed_languages))[0]
        translation = from_lang.get_translation(to_lang)

        if from_code=='en':
            user_input = user_input.lower()
            
        translatedText = translation.translate(user_input)
    else:
        translatedText = "目前尚不能翻譯此組合"
        
    return translatedText

print(argoTranslator(sys.argv[1], sys.argv[2], sys.argv[3]))
# print(argoTranslator("solution", 'en', 'zh'))
# if __name__=="__main__":

# 	print(argoTranslator("solution", 'en', 'zh'))