import base64
from PIL import Image
import io
import subprocess
import os
from TTS.api import TTS
import torch
import shutil


def sadtalker(text, img):
    pil_image = Image.open(img)

    # handle image
    file_path = "image.jpg"
    pil_image.save(file_path, format='JPEG')

    # handle audio
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Using {device} for TTS")

    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # Text to speech to a file
    tts.tts_to_file(text=text, speaker_wav="voice/source_girl.mp3", language="zh-cn", file_path="voice/voice_girl.wav")


    # clear directory
    target_directory = 'outputs'
    if os.path.exists(target_directory) and os.path.isdir(target_directory):
        if os.listdir(target_directory):
            clear_directory(target_directory)
    
    remove_all_folders(target_directory)
                                                                    
                                                                                                

    command = f"python inference.py --driven_audio voice/voice_girl.wav \
                    --source_image image.jpg \
                    --result_dir outputs \
                    --still \
                    --preprocess full \
                    --enhancer gfpgan "

    print("Process Start, Please Wait...")
    subprocess.run(command, shell=True, capture_output=True, text=True)

    return "[INFO] Process complete"


def clear_directory(folder_path):
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
                print(f"Error deleting file: {file_path} - {e}")


def remove_all_folders(directory):
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Folder '{item_path}' has been deleted successfully.")
    except OSError as e:
        print(f"Error: {e.strerror}")