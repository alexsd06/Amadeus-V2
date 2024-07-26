lang = 'Japanese'
tag = 'mio/amadeus'
vocoder_tag = 'none'

from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none
import sounddevice as sd
import numpy as np

#Can't include header Python.h
#sudo apt install python3-dev

text2speech = Text2Speech.from_pretrained(
    model_tag=str_or_none(tag),
    vocoder_tag=str_or_none(vocoder_tag),
    device="cuda",   #if your runtime has cuda cores
    threshold=0.5,
    minlenratio=0.0,
    maxlenratio=10.0,
    use_att_constraint=False,
    backward_window=1,
    forward_window=3,
    speed_control_alpha=0.9,
    #noise_scale=0.333,
    #noise_scale_dur=0.333,
)
import torch


def tts(x):
    with torch.no_grad():
        output = text2speech(x)
        wav = output["wav"]
        if torch.is_tensor(wav):
            wav = wav.cpu().numpy().astype(np.float32)
            return wav


def play_audio(wav, sample_rate=22050):
    sd.play(wav, sample_rate)
    # sd.wait()