import os
import re

def count_chinese_english_words(text):
    """
    >>>count_chinese_english_words('测试 a piece of test')
    6
    """
    # Count Chinese characters
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    num_chinese_words = len(chinese_chars)
    
    # Count English words
    english_words = re.findall(r'\b[a-zA-Z]+\b', text)
    num_english_words = len(english_words)
    
    return num_chinese_words+num_english_words

def sentences_to_paragraph(sentence_list, max_par_len=650):
    paragraphs = []
    current_paragraph = ''
    
    for sentence in sentence_list:
        if count_chinese_english_words(current_paragraph) <= max_par_len:
            current_paragraph += (sentence + '. ')
        else:
            paragraphs.append(current_paragraph)
            current_paragraph = sentence
            
    if count_chinese_english_words(current_paragraph) <= max_par_len:
        paragraphs.append(current_paragraph)
        
    return paragraphs

def get_latest_file(directory, file_extension):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(file_extension)]
    # 获取最近修改的文件
    if files:
        latest_file = max(files, key=os.path.getmtime)
        print(f"最近的 {file_extension} 文件是: {latest_file}")
    else:
        print(f"目录中没有扩展名为 {file_extension} 的文件")
    
    return latest_file

