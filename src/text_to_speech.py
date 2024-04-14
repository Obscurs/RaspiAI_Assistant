from gtts import gTTS
from src.config import setting_TTS_method
from src.config import setting_TTS_piper_EN_model
from src.config import setting_TTS_piper_ES_model
from src.config import setting_TTS_piper_CA_model
import os
import subprocess

BASE_MODEL_PATH  = "models/"

def googleTTS(text, language, filename):
    print("text_to_speech: gTTS")
    tts = gTTS(text, lang=language)
    print("text_to_speech: save")
    tts.save(filename)
    print("text_to_speech: open")
    subprocess.Popen(["cvlc", "--play-and-exit", "--no-repeat", filename])
    
def piperTTS(text, language):
    model_suffix = {
        "ca": setting_TTS_piper_CA_model,
        "en": setting_TTS_piper_EN_model,
        "es": setting_TTS_piper_ES_model
    }.get(language, "")
    
    model_file = f"{BASE_MODEL_PATH}{model_suffix}.onnx"

    text = text.replace("'", "\'")

    # Prepare the command
    command = [
        './env/bin/piper', 
        '--model', model_file, 
        '--output-raw'
    ]

    # Run the TTS engine and capture output
    piper_process = subprocess.Popen(
        command, stdout=subprocess.PIPE, 
        input=text, text=True
    )
    audio_data = piper_process.communicate()[0]

     # Play the audio
    play_command = ['aplay', '-r', '22050', '-f', 'S16_LE', '-t', 'raw', '-']
    play_process = subprocess.Popen(
        play_command, stdin=subprocess.PIPE
    )
    play_process.communicate(input=audio_data)

    piper_process.wait()
    play_process.wait()

def text_to_speech(text, language, filename="output.wav"):
    if setting_TTS_method == "gTTS":
        googleTTS(text, language, filename)
    elif setting_TTS_method == "piper":
        piperTTS(text, language)
