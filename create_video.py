from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import moviepy.editor as mpe

ONE_LINE_LEN = 91
FRAMES_FOLDER = "images/frames"
TITLE_PATH = "images/title/title.png"
FINAL_VIDEO_PATH = "final_video/full_video.mp4"

SPLITTER_PATH = "images/splitter/static_splitter.png"
FRAMERATE = 20


def add_newline_after_words(text: str, num: int):
    if len(text) <= num:
        return text

    all_str = ""
    dist_from_newline = 0
    i = 0

    while i < len(text):
        if dist_from_newline <= num:
            all_str += text[i]
            i += 1
            dist_from_newline += 1

        else:
            all_str = all_str[::-1]
            all_str = list(all_str)

            for j in range(len(all_str)):
                if all_str[j] == ' ':
                    all_str[j] = '\n'
                    dist_from_newline = j
                    break

            all_str = ''.join(all_str)
            all_str = all_str[::-1]

    return all_str


def create_img_with_text(text, file_path):
    text = add_newline_after_words(text, ONE_LINE_LEN)

    img = Image.new("RGB", (1280, 720), (35, 39, 42))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", 26)

    draw.text((50, 50), text, font=font)

    img.save(file_path)


def create_images_from_text_list(text_list: list):
    for i, text in enumerate(text_list, 1):
        create_img_with_text(text, FRAMES_FOLDER + '/' + f"frame{str(i).zfill(3)}.png")


def add_frames_to_video(out_vid, frames_folder, all_times):
    # all_times: (title_len, splitter_len, [frames_len, ...])

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(out_vid, fourcc, FRAMERATE, (1280, 720))

    frames = []

    # get all frames

    for r, d, f in os.walk(frames_folder):
        for file in f:
            path = r + '/' + file
            frames.append(cv2.imread(path))

    splitter_frame = cv2.imread(SPLITTER_PATH)

    # add title frames
    for j in range(int(FRAMERATE * all_times[0])):
        title = cv2.imread(TITLE_PATH)
        out.write(title)

    # add splitter frames
    for j in range(int(FRAMERATE * all_times[1])):
        out.write(splitter_frame)

    for i, frame in enumerate(frames, start=0):
        print(FRAMERATE * all_times[2][i])

        for j in range(int(FRAMERATE * all_times[2][i])):
            out.write(frame)

        # add splitter frames
        for j in range(int(FRAMERATE * all_times[1])):
            out.write(splitter_frame)

    out.release()


def add_audio_to_video(audio_path, video_path):
    video = mpe.VideoFileClip(video_path)
    audio = mpe.AudioFileClip(audio_path)
    final = video.set_audio(audio)
    final.write_videofile(FINAL_VIDEO_PATH)


def main():
    add_audio_to_video("audio/full_audio.mp3", "images/only_video.mp4")


if __name__ == '__main__':
    main()
