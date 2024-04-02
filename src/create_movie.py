from pydub import AudioSegment
from moviepy.editor import *
from grab_files import *
from revise_images import *

def create_movie(voice=None):
    # 计算所有语音的长度，得出需要视频的长度
    if voice is None:
        voice = []
    duration_clips, text_clips = [], []
    for item in voice:
        filename = str(item.split('/')[-1])
        tmp = filename.split('_')
        text_clips.append(tmp[0])
        duration_clips.append(float(tmp[-1].replace('.mp3', '')))

    duration = sum(duration_clips)

    # 背景音乐
    bg_music = AudioFileClip("../bgm/HappyUkulele.mp3").set_duration(duration).volumex(0.3)

    # 解说 + 字幕
    voice_clips, txt_clips = [], []

    for idx, item in enumerate(text_clips):
        start = sum(duration_clips[:idx])
        end = start + duration_clips[idx]
        voice_clips.append(
             AudioFileClip(voice[idx]).set_start(start).volumex(0.8))
        
        txt_clip = TextClip(text_clips[idx], fontsize=40, color='white')
        #txt_clip = txt_clip.set_pos('bottom').set_duration(duration_clips[idx]).crossfadein(1).crossfadeout(1)
        txt_clip = txt_clip.set_start(start).set_end(end)
        txt_clips.append(txt_clip)
        

    picture_path = '../pictures'
    # 定义每张图片的剪辑，并添加淡入淡出效果
    images = grab_files(picture_path)

    # 将图片格式化
    for image in images:
        # 将图片变成 16:9  高度787.5 ，宽度1400
        revise_images(image)

    image_num = len(images)
    image_duration = duration / image_num
    image_clips = []

    # 镜头焦点效果
    def resize_func(t):
        return 1 + 0.005 * t

    # screensize = (640, 360)
    for image_path in grab_files('../pictures'):
        image_clip = ImageClip(image_path).set_duration(image_duration).resize(resize_func).set_position(
            ('center', 'center')).set_fps(25)
        image_clip = image_clip.crossfadein(1).crossfadeout(1)
        image_clips.append(image_clip)

        # image_clips.append(ImageClip('path_to_image.jpg').resize(resize_func).set_position(('center', 'center')).set_duration(image_duration).set_fps(25))
    return [image_clips, txt_clips, bg_music, voice_clips]


def combine(image_clips, txt_clips, bg_music, voice_clips):
    # 将所有图片剪辑合并为一个剪辑
    
    image_clip = concatenate_videoclips(image_clips)

    # 将图像、字幕和音频剪辑合并为一个剪辑，并添加淡入淡出效果
    #video_clip = CompositeVideoClip([image_clip])
    txt_clips = [CompositeVideoClip([clip]) for clip in txt_clips]  # Ensuring txt_clips is a list of CompositeVideoClip objects
    video_clip = CompositeVideoClip([image_clip] + txt_clips)
    audio_clip = CompositeAudioClip([bg_music] + voice_clips)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip = video_clip.crossfadein(1).crossfadeout(1)

    # 导出视频剪辑
    video_clip.write_videofile("../output.mp4", fps=24)




