import requests
import json
import os
# from openai import OpenAI
import re
import mistune
from bs4 import BeautifulSoup

def remove_specific_first_line(text):
    lines = text.split("\n")
    
    # 确保文本非空，并检查第一行是否满足所有条件
    if lines and lines[0].endswith("：") and ("书面化" in lines[0] or "转写" in lines[0]):
        lines = lines[1:]  # 删除第一行

    # 检查最后一行是否包含“注：”且包含“口语”或“书面”
    if lines and "注：" in lines[-1] and ("口语" in lines[-1] or "书面" in lines[-1] or "转写" in lines[-1] or "改写" in lines[-1]):
        lines = lines[:-1]  # 删除最后一行
    
    return "\n".join(lines)

def extract_markdown(text):
    match = re.search(r'---\n(.*?)\n---', text, re.DOTALL)
    text = match.group(1) if match else re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = remove_specific_first_line(text)
    return text

def markdown_to_text(md_content):
    markdown = mistune.create_markdown()
    html = markdown(md_content)
    soup = BeautifulSoup(html, 'html.parser')
    result = re.sub(r'\n+', '\n', soup.get_text(), flags=re.MULTILINE)
    return result

# def ollama(prompt, system, model="deepseek-r1:14b", pure_text=False):
def ollama(prompt, system, model="hf.co/bartowski/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K_L", pure_text=False):
    url = "http://192.168.1.116:11434/api/generate"
    # 构建请求数据
    data = {
        "model": model,
        "prompt": prompt,
        "system": system,
    }
    # 发送POST请求
    response = requests.post(url, json=data)
    # 检查响应
    with requests.post(url, json=data, stream=True) as response:
    # 检查响应状态码
        if response.status_code == 200:
            # 流式读取响应内容并逐行打印
            result = ''
            for line in response.iter_lines():
                if line:  # 忽略空行
                    try:
                        # 解析每一行的JSON数据
                        json_data = json.loads(line.decode('utf-8'))
                        print(json_data['response'], end='')  # 打印每个JSON对象
                        result += json_data['response']
                    except json.JSONDecodeError as e:
                        print(f"解析错误: {e}")
        else:
            print("Error:", response.status_code, response.text)

    # result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)
    result = extract_markdown(result)
    if pure_text:
        result = markdown_to_text(result)
    return result

def openai(prompt, system, model="qwen-max"):
    system_prompt = system
    user_prompt = str(prompt)

    client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)
    completion = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0.2,
    )
    print(completion.choices[0].message.content, flush=True)
    return completion.choices[0].message.content


