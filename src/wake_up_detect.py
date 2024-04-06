import pvporcupine
import asyncio
import pyaudio
import struct
import sys
import os
import signal
from src.speech_to_text import recognize_speech
from src.text_to_speech import text_to_speech
from src.translator import translate
from src.config import porcupine_access_key
from src.config import setting_Wakeup_model
from src.config import setting_TTS_lang
from src.gpt import ChatGPT
#from src.bing import Bing
from src.nlp import is_time_sensitive

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

async def wake_up_detect():
    #capture SIGINT signal, e.g. ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    #create chatGPT and Bing object
    chat_gpt = ChatGPT()
    #bing = Bing()
    #define the hotword model
    # keyword_path = "models/alexa_windows.ppn" #test case with "alexa" in Windows platform
    #keyword_path = "models/Hey-Ras-Pi_en_raspberry-pi_v2_1_0.ppn"
    keyword_path = "models/" + setting_Wakeup_model + ".ppn"

    #initialize the Porcupine engine
    porcupine = None
    try:
        porcupine = pvporcupine.create(access_key=porcupine_access_key, keyword_paths=[keyword_path])
        print("Portcupine inited")
        print(porcupine.sample_rate)
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        listening = True
        while not interrupt_callback():
            if listening:
                listening = False
                print("Listening for 'Hey Ras Pi'...")
            
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                listening = True
                #play wake up sound
                
                print("Hey Ras Pi detected! Recognizing speech...")
                query, lang = recognize_speech()

                #if lang == "en-US":
                #text_to_speech("Let me think about it. Please wait for a while","en","seaching.wav")
                #else:
                #    text_to_speech("請給點時間我想一想","zh","seaching.wav")

                try:
                   
                    # gpt_result, bing_result = await asyncio.gather(gpt(query, lang), bing(query))
                    #if is_time_sensitive(query):
                    #    bing_result = await asyncio.wait_for(bing.bing(query), timeout=45)
                    #    response = bing_result["item"]["messages"][1]["text"]
                    #    print("BING: ",bing_result)
                    #else:
                    # Call gpt() and bing() concurrently
                    #gpt_result, bing_result = await asyncio.wait_for(
                    #    asyncio.gather(chat_gpt.gpt(query, lang), bing.bing(query)),
                    #    timeout=45
                    #)
                    if lang == "en-US" or lang == "es-ES" or lang == "en-ES":
                        print("Got it! Please wait for a while")
                        #text_to_speech("Got it! Please wait for a while","en")
                        os.system(f"aplay searching.wav")
                        gpt_result = await asyncio.wait_for(asyncio.gather(chat_gpt.gpt(query, lang)), timeout=45)
                    #print(gpt_result)
                        gpt_result = gpt_result[0]['choices'][0]['message']["content"]
                        #gpt_result, bing_result = gpt_result['choices'][0]['message']["content"], bing_result["item"]["messages"][1]["text"]
                    else:
                        print("Error parsing")
                        os.system(f"aplay finish.wav")
                        gpt_result = ''
                        
                    print("GPT: ", gpt_result)
                        #print("BING: ",bing_result)
                    #response = bing_result if "IDK" in gpt_result or "Sorry" in gpt_result or "sorry" in gpt_result  or "s an AI language model" in gpt_result else gpt_result
                    response = gpt_result
                except asyncio.TimeoutError:
                    #text_to_speech("Sorry I could not process your request, try again","en")
                    os.system(f"aplay finish.wav")
                    print("Request timed out. Retrying...")
                    continue
                
                #translate to the voice input language
                #if lang != "en-US" and response != bing_result:
                #    response = translate(response,"zh-TW")

                #text to speech
                #if lang == "en-US":
                print("Output response:")
                if gpt_result != '':
                    text_to_speech(response, setting_TTS_lang)
                    os.system(f"aplay finish.wav")
                #else:
                #    text_to_speech(response, "zh")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


