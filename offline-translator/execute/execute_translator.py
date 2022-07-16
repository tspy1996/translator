import subprocess
import opencc

translator_path ='./translator_argo'

def exe(input_text, src, dest):
    input_text = input_text.replace("'", " ")
    ret = subprocess.run([translator_path, input_text, src, dest],
                shell=False, stdout=subprocess.PIPE) # input as list, set shell=False
    result = ret.stdout.decode('utf8')

    converter = opencc.OpenCC('s2t')
    translatedText = converter.convert(result)

    return translatedText

# exe("solve the problem", 'en', 'zh')