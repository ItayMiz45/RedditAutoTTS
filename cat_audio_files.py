from pydub import AudioSegment
import os

STATIC_SOUND_PATH = r"C:\Users\itay\PycharmProjects\PythonProjects\reddit_auto_tts\audio\splitter\static_sound_effect.mp3"
TITLE_MP3_PATH = "audio/title/title.mp3"
COMMENTS_PATH = "audio/comments"
FULL_MP3_PATH = "audio/full_audio.mp3"


def get_len_of_all_mp3():
    comments = []

    for r, d, f in os.walk(COMMENTS_PATH):
        for file in f:
            audio = AudioSegment.from_mp3(r + '/' + file)
            comments.append(len(audio)/1000)

    title = AudioSegment.from_mp3(TITLE_MP3_PATH)
    splitter = AudioSegment.from_mp3(STATIC_SOUND_PATH)

    return len(title)/1000, len(splitter)/1000, comments


def create_and_save_mp3():
    #AudioSegment.ffmpeg = r"C:\Users\itay\ffmpeg-20190824-1cfba7f-win64-static\ffmpeg-20190824-1cfba7f-win64-static\bin\ffmpeg.exe"

    static_audio = AudioSegment.from_mp3(STATIC_SOUND_PATH)

    new_audio = AudioSegment.from_mp3(TITLE_MP3_PATH) + static_audio

    comments = []

    for r, d, f in os.walk(COMMENTS_PATH):
        for file in f:
            comments.append(os.path.join(r, file))

    for comment in comments:
        new_audio += AudioSegment.from_mp3(comment) + static_audio

    new_audio.export(FULL_MP3_PATH, format="mp3")


def main():
    create_and_save_mp3()


if __name__ == '__main__':
    main()
