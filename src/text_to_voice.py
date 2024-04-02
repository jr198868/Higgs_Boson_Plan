import os
import math
import shutil
import re
import subprocess
from moviepy.editor import *
from gtts import gTTS
from pydub import AudioSegment
import edge_tts

def text_to_voice():
    try:
        shutil.rmtree('./texttovoice')
        #os.mkdir('./tts')
    except:
        pass

    voice = []
    content = open('../content.txt').read()

    contents = re.split(r'[。！？？, ，]', content)

    for content in contents:
        content = content.replace('"', "'").strip()
        if not len(content):
            continue
        # filename = gtts(content)
        filename = _edge_tts(content)
        voice.append(filename)
    return voice

def gtts(content):
    filename = '../tts/%s.mp3' % content
    # 转语音
    g_tts = gTTS(content, lang='zh-CN')
    g_tts.save(filename)

    # 调整语速 为 1.0 倍速
    sound = AudioSegment.from_mp3(filename)
    duration = int(sound.duration_seconds)
    update_speed_filename = '../tts/%s_duration_%f.mp3' % (content, math.ceil(duration * 0.85))
    cmd = "ffmpeg -y -i %s -filter_complex \"atempo=tempo=%s\" %s" % (filename, '1.0', update_speed_filename)
    res = subprocess.call(cmd, shell=True)
    if res == 0:
        os.remove(filename)
    return update_speed_filename


def _edge_tts(content):

    filename = '../tts/%s.mp3' % content
    cmd = 'edge-tts --voice zh-CN-YunxiNeural --text "' + content + '" --write-media %s' % filename
    res = subprocess.call(cmd, shell=True)

    sound = AudioSegment.from_mp3(filename)
    duration = int(sound.duration_seconds)
    update_name = '../tts/%s_duration_%f.mp3' % (content, duration)
    os.rename(filename, update_name)
    return update_name
    pass


def get_all_files(path):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files