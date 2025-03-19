#coding=utf-8
import os
from openai import OpenAI
with open ('grok_3_key.txt','r',encoding='utf-8') as f :
    grok_3_key = f.read()

client = OpenAI(
    api_key=grok_3_key,
    base_url="https://api.x.ai/v1/chat/completions",
)

completion = client.chat.completions.create(
    model="grok-beta",
    messages=[
        {
            "role": "system",
            "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
        },
        {
            "role": "user",
            "content": "What is the meaning of life, the universe, and everything?"
        },
    ],
)

print(completion.choices[0].message.content)







