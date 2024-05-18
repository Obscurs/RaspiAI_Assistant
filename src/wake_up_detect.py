import pvporcupine
import asyncio
import pyaudio
import struct
import sys
import os
import signal
from src.speech_to_text import recognize_speech
from src.text_to_speech import text_to_speech
#from src.translator import translate
from src.config import setting_Audio_Volume
from src.config import porcupine_access_key
from src.config import setting_Wakeup_model
from src.config import setting_TTS_lang
from src.gpt import ChatGPT
from src.nlp import is_time_sensitive

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted
        
async def wake_up_detect():
    signal.signal(signal.SIGINT, signal_handler)

    chat_gpt = ChatGPT()
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
        print("Listening for 'Hey Ras Pi'...")
        while not interrupt_callback():
            if listening:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    audio_stream.stop_stream()
                    listening = False
                    
                    print("Hey Ras Pi detected! Recognizing speech...")
                    query, lang = recognize_speech()

                    try:
                        if lang == "en-US" or lang == "es-ES" or lang == "en-ES":
                            print("Got it! Please wait for a while")
                            os.system(f"amixer set Master {setting_Audio_Volume/1.5}%")
                            os.system(f"aplay searching.wav")
                            gpt_result = await asyncio.wait_for(asyncio.gather(chat_gpt.gpt(query, lang)), timeout=45)
                            gpt_result = gpt_result[0].choices[0].message.content
                        else:
                            print("Error parsing")
                            os.system(f"aplay finish.wav")
                            gpt_result = ''
                            
                        print("GPT: ", gpt_result)
                        response = gpt_result
                    except asyncio.TimeoutError:
                        os.system(f"aplay finish.wav")
                        print("Request timed out. Retrying...")
                        continue
                    
                    print("Output response:")
                    if gpt_result != '':
                        text_to_speech(response, setting_TTS_lang, chat_gpt)
                        os.system(f"aplay finish.wav")
                        
                    audio_stream.start_stream()
                    print("Finished writing going to listen again")
                    listening = True

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
