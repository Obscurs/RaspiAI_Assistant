from gtts import gTTS
from src.config import setting_TTS_method
from src.config import setting_TTS_piper_EN_model
from src.config import setting_TTS_piper_ES_model
from src.config import setting_TTS_piper_CA_model
import os
import subprocess

def googleTTS(text, language, filename):
    print("text_to_speech: gTTS")
    tts = gTTS(text, lang=language)
    print("text_to_speech: save")
    tts.save(filename)
    print("text_to_speech: open")
    subprocess.Popen(["cvlc", "--play-and-exit", "--no-repeat", filename])
    
def piperTTS(text, language):
    model_file = "models/"
    text = text.replace("'", "\'")
    if language == "ca":
        model_file = model_file + setting_TTS_piper_CA_model
    elif language == "en":
        model_file = model_file + setting_TTS_piper_EN_model
    elif language == "es":
        model_file = model_file + setting_TTS_piper_ES_model
    
    model_file = model_file + ".onnx"
    command = f"""
    echo '{text}' | \
    ./env/bin/piper --model {model_file} --output-raw | \
    aplay -r 22050 -f S16_LE -t raw -
    """
    subprocess.run(command, shell=True, text=True, check=True)

def text_to_speech(text, language, filename="output.wav"):
    if setting_TTS_method == "gTTS":
        googleTTS(text, language, filename)
    elif setting_TTS_method == "piper":
        piperTTS(text, language)
