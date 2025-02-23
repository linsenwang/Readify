import os
import re
from functools import partial
from utils.models import ollama
from utils.phrase import sentences_to_paragraph, get_latest_file




directory = 'ori'
file_extension = '.txt'  # 你想要的文件扩展名

latest_file = get_latest_file(directory, file_extension)



#pattern = latest_file.split('.')[0].split('/')[-1]
pattern = re.sub(r'\..+-文稿-转写结果', '', os.path.splitext(latest_file)[0].split('/')[-1])
pattern



def search(pattern):
    """
    >>>search('gt-01')
    ['ori/gt-01-1.m4a-文稿-转写结果.txt', 'ori/gt-01-2.m4a-文稿-转写结果.txt']
    """
    result = []
    for filename in os.listdir('ori'):
        if re.search(pattern, filename):
            result.append('ori/'+filename)
    return result

'''with open(search('gt-01')[1]) as f:
    sentence_list = re.split(r'[。|\n]', f.read().replace('\xa0', ''))
    for i in sentence_list:
        if count_chinese_english_words(i)[1] > 6:
            print(i)'''

def get_sentence_list(pattern):
    sentence_list = []
    for i in search(pattern):
        item_list = []
        with open(i) as f:
            item_list = re.split(r'[。|\n|.]', re.sub(r'\xa0|right\?|Right\?|  ', ' ', f.read()))
            #item_list = re.split(r'[\n]', re.sub(r'\xa0|right\?|Right\?|  ', ' ', f.read()))
        item_list = [item for item in item_list if item != '']
        sentence_list = sentence_list + item_list
    return sentence_list

sentence_list = get_sentence_list(pattern)
sentence_list



paragraph = sentences_to_paragraph(sentence_list)
for p in paragraph:
    print(p[-50:])



paragraph[1]


system = "请使用中文将下面这段语音转写结果转换成更加书面的语言。减少语气词，增加合适的句号和分段。尽可能保持内容完整。一定要使用中文。不要输出其它内容。"
get_result = partial(ollama, system=system)

try:
    with open('log/' + pattern + '.txt', 'r+') as f:
        last = int(re.findall(r'PARA(.+)\n', f.read())[-1])
except:
        last = -1

for i in range(last + 1, len(paragraph)):
    try:
        text = get_result(paragraph[i])
    except:
        text = str(i)+'ERROR'

    with open('pro/' + pattern + '.txt', 'a') as f:
            f.write(text +'\n')
            # print(text)

    with open('log/' + pattern + '.txt', 'a') as f:
        f.write('PARA'+str(i)+'\n')
        for index, i in enumerate(text.split('\n')):
            f.write(str(index) + ': ' + i[:15] + '\n')






