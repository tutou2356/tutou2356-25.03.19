from openai import OpenAI
#coding=utf-8
import os


def chat_g(question):
    with open ('guiji_key.txt','r',encoding='utf-8') as f :
        guiji_key = f.read()
    client = OpenAI(api_key=guiji_key, base_url="https://api.siliconflow.cn/v1")
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-V2.5',
        messages=[
            {'role': 'user',
            'content': question}
        ],
        stream=True
    )

#     result_text=''
#     for chunk in response:
#         result_text = chunk.choices[0].delta.content
#         print(result_text,end='')
#
#
#
# chat_g('python是什么')

    result_text = ""
    for chunk in response:
        # 如果你想调试，可以打印，但要拼接字符串才能最终return
        piece = chunk.choices[0].delta.content
        result_text += piece  # 关键：持续拼接
    return result_text

