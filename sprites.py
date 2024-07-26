# emotions = ["sleep", "interest", "sad", "very default", "wink", "serious", "disappoint", "tired", "fun", "angry",
#             "embarrassed", "very not interest", "default", "very embarrassed", "calm", "very serious", "surprise",
#             "not interest", "closed sleep", "back"]

emotions = ["sleep", "interest", "sadness", "very default", "wink", "serious", "disappoint", "tired", "joy", "anger",
            "love", "very not interest", "default", "very embarrassed", "calm", "very serious", "surprise",
            "not interest", "closed sleep", "fear"]

def get_sprite_code (distance="medium", emotion="default"):
    assert distance in ["large", "medium", "small"]
    assert emotion in emotions
    index = emotions.index(emotion)
    D = "D_40000"
    E = "E_40000"
    F = "F_00000"
    D_dat = ["a", "b", "c", "1", "2", "3", "4", "5", "6", "7", "8", ""]
    E_dat = ["1", "2", "3", "4", "5", "6", "7", "0"]
    pref = "CRS_J" + {"large": "L", "medium": "M", "small": "S"}[distance]

    if index == 19:
        return pref + "F_00000" + E_dat[7]
    elif index >= 12:
        return pref + "E_40000" + E_dat[index - 12]
    else:
        return pref + "D_40000" + D_dat[index]




"""
start_letter = 'J'
height_code = {
    'short': 'L',
    'medium': 'M',
    'tall': 'S'
}
body_orientation = {
    'frontal': 'D',
    'sideways_left': 'E',
    'backward': 'F'
}
expressions = {
    'frontal': {
        'eyes_closed': '40000a0',
        'serious': '40000b0',
        'sad': '40000c0',
        'default': '4000010',
        'blink_smiling': '4000020',
        'anger': '4000030',
        'annoyed': '4000040',
        'little_sad': '4000050',
        'smiling_eyes_closed': '4000060',
        'determination': '4000070',
        'blushing': '4000080',
        'no_eye_contact': '4000090'
    },
    'sideways': {
        'default': '4000010',
        'blushing': '4000020',
        'smiling': '4000030',
        'determination': '4000040',
        'curious': '4000050',
        'no_eye_contact': '4000060',
        'eyes_closed': '4000070'
    },
    'backward': '00000001'

}
mouth_position = {
    'closed': '0',
    'medium': '1',
    'opened': '2'
}

tokens_frontal = [f"[frontal/{emotion}]" for emotion in expressions['frontal']]
tokens_sideways = [f"[sideways/{emotion}]" for emotion in expressions['sideways']]

tokens = []
tokens.extend(tokens_frontal)
tokens.extend(tokens_sideways)

print(f'Tokens for front facing: {list(expressions["frontal"].keys())}')
print(f'Tokens for facing sideways: {list(expressions["sideways"].keys())}')

print(tokens)
"""