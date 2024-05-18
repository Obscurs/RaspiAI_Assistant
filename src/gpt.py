import os
from openai import OpenAI
#import openai
import pyaudio
import pygame
import asyncio
from datetime import date
import time
#from src.translator import translate
from src.config import gpt_key
from src.config import setting_TTS_lang
from src.config import setting_Audio_Volume

#sys_content = ("Note that if you cannot answer the question which is about "
#                   "something you do not know such as time-sensitive information(e.g. "
#                   "today's weather/stock, .etc), you can only reply \"IDK\" in your response without other characters."
#                   "Do not say something like As an AI language model..., I'm sorry... and etc.")
sys_content = ("")
os.environ['OPENAI_API_KEY'] = gpt_key

pygame.mixer.init()
today = str(date.today())
class ChatGPT:
    def __init__(self):
        if setting_TTS_lang == "en":
            sys_content = ("Answer in english")
        elif setting_TTS_lang == "es":
            sys_content = ("Answer in spanish")
        elif setting_TTS_lang == "ca":
            sys_content = ("Answer in catalan")
            
        #openai.api_key = gpt_key
        self.client = OpenAI()
            
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
        #response = await openai.ChatCompletion.acreate(
        #    model="gpt-3.5-turbo",
        #    messages=self.messages
        #)

        response = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages= self.messages
        )
        self.messages.append({"role":"assistant", "content": response.choices[0].message.content})
        return response
        
    def tts(self, text, language):
        os.system(f"amixer set Master {setting_Audio_Volume/1.3}%")
        response = self.client.audio.speech.create(
            model="tts-1",
            # alloy: man; nova: woman
            voice="nova",
            input= text )

        fname = 'output.mp3'

        mp3file =open(fname, 'w+') 

        #if os.path.exists(fname):
        #    os.remove(fname)    
                      
        response.stream_to_file(fname)

        showtext = True  

        try:        
            pygame.mixer.music.load(mp3file)
            pygame.mixer.music.play()
        
            while pygame.mixer.music.get_busy():
                #  
                if showtext:
                    print("AI: " + text)
                    showtext = False 
                time.sleep(0.25)
            
            pygame.mixer.music.stop()    
            mp3file.close()
        
        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            mp3file.close()
            #print("\nAudio playback stopped.")
