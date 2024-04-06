import os
import openai
import asyncio
from src.translator import translate
from src.config import gpt_key
from src.config import setting_TTS_lang

#sys_content = ("Note that if you cannot answer the question which is about "
#                   "something you do not know such as time-sensitive information(e.g. "
#                   "today's weather/stock, .etc), you can only reply \"IDK\" in your response without other characters."
#                   "Do not say something like As an AI language model..., I'm sorry... and etc.")
sys_content = ("")
class ChatGPT:
    def __init__(self):
        if setting_TTS_lang == "en":
            sys_content = ("Answer in english")
        elif setting_TTS_lang == "es":
            sys_content = ("Answer in spanish")
        elif setting_TTS_lang == "ca":
            sys_content = ("Answer in catalan")
            
        openai.api_key = gpt_key
        self.messages = [
            {"role": "system", "content": sys_content},
        ]

    async def gpt(self, prompt, lang):
        #translate the prompt into English first for better accuracy
        #if lang != "en-US":
        #    prompt = translate(prompt, "en")

        prompt += "\n"
        self.messages.append({"role": "user", "content": prompt})
        #run the synchronous openai.ChatCompletion.create() in a separate thread
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        self.messages.append({"role":"assistant", "content": response['choices'][0]['message']["content"]})
        return response
