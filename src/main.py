import os
from text_to_voice import text_to_voice
from create_movie import create_movie, combine

if __name__ == "__main__":
    # Generate voice files from text
    voice = text_to_voice()

    # Remove any .DS_Store files in the pictures folder
    for root, dirs, files in os.walk('../pictures'):
        for file in files:
            if file == '.DS_Store':
                os.remove(os.path.join(root, file))

    # Create the movie using the generated voice files
    image_clips, bg_music, voice_clips = create_movie(voice)

    combine(image_clips, bg_music, voice_clips)
