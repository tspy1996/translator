"""collect terms into one file for latter translate
中華民國外交部.csv 2557字
create terms_dict.pickle
"""
import re
import pandas
import itertools
import pickle
def count_ngram(row):
  n = len(row.split(' '))
  return n

def clean1(df):
  '''let one zh word pair with only one en word'''
  df_new = pandas.DataFrame(columns=['英文(English)', '中文(Chinese)'])
  for _, row in df.iterrows():
    zh_list = []
    en_list = []
    if ";" in row['英文(English)']:
      e = row['英文(English)'].split(";")
      e = [i.strip() for i in e ]
      en_list.extend(e)
    if "/" in row['英文(English)']:
      e = row['英文(English)'].split("/")
      e = [i.strip() for i in e ]
      en_list.extend(e)
    # if "、" in row['中文(Chinese)']:
    #   z = row['中文(Chinese)'].split("、")
    #   z = [i.strip() for i in z ]
    #   zh_list.extend(z)
    # reformat row
    tmp_row = []
    if len(zh_list)!=0 and len(en_list)!=0:
      tmp_row = list(itertools.product(en_list, zh_list))
      for pair in list(itertools.product(en_list, zh_list)):
        tmp_row = {'英文(English)': [pair[0]], '中文(Chinese)':[pair[1]]}
        s = pandas.DataFrame.from_dict(tmp_row)
        df_new = pandas.concat([df_new, s], ignore_index=True)
    elif len(zh_list)==0 and len(en_list)!=0:
      for eword in en_list:
        tmp_row = {'英文(English)': [eword], '中文(Chinese)':[row['中文(Chinese)']]}
        s = pandas.DataFrame.from_dict(tmp_row)
        df_new = pandas.concat([df_new, s], ignore_index=True)
    elif len(zh_list)!=0 and len(en_list)==0:
      for zword in zh_list:
        tmp_row = {'英文(English)': [row['英文(English)']], '中文(Chinese)': [zword]}
        s = pandas.DataFrame.from_dict(tmp_row)
        df_new = pandas.concat([df_new, s], ignore_index=True)
    else:
      tmp_row = {'英文(English)': [row['英文(English)']], '中文(Chinese)':[row['中文(Chinese)']]}
      s = pandas.DataFrame.from_dict(tmp_row)
      df_new = pandas.concat([df_new, s], ignore_index=True)
  return df_new

def clean2(df):
  '''
  remove "（）"in chinese
  English to lowercase
  '''
  df['中文(Chinese)'] = df['中文(Chinese)'].apply(lambda row: re.sub(r'\([^)]*\)', '', row))
  df['英文(English)'] = df['英文(English)'].apply(lambda row: row.lower())
  return df
    
def termfile_2_dict():
  '''
  turn 中華民國外交部.csv 
  into dictionary = {num of eng word: {en: zh}} for latter useage.
  '''
  df = pandas.read_csv('中華民國外交部_mod.csv')
  # sperate ";" "、"and "/"
  df = clean1(df)
  df = clean2(df)
  # count n-gram
  df['words'] = df['英文(English)'].apply(lambda row: count_ngram(row))
  # mask = df['words'] <5
  # print(df[mask])
  word_dict = {}
  for _, row in df.iterrows():
    try:
      tmp_dict = word_dict[row['words']]
      tmp_dict[row['英文(English)']] = row['中文(Chinese)']

    except KeyError:
      word_dict[row['words']] = {}
      tmp_dict = word_dict[row['words']]
      tmp_dict[row['英文(English)']] = row['中文(Chinese)']
    word_dict[row['words']] = tmp_dict

  return word_dict


terms_dict = termfile_2_dict()
with open('terms_dict.pickle', 'wb') as handle:
    pickle.dump(terms_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

