from reddit_auto_tts import submission, cat_audio_files, create_video
import os

TITLE_IMG_PATH = "images/title/title.png"
ONLY_VIDEO_PATH = "images/only_video.mp4"

# TODO
# Check for comments that are too long to view


def delete_files():
    for root, d, files in os.walk("."):
        for f in files:
            if not(f.endswith(".py") or f.endswith(".pyc") or f.endswith(".exe") or ("splitter" in f) or ("static" in f) or ("ff" in f)):
                os.remove(os.path.join(root, f))


def main():
    delete_files()

    # get best submission of the day
    valid_submissions = submission.get_valid_submissions(submission.SUBREDDIT)
    best_submission = submission.get_best_submission(valid_submissions)

    # get top comments of best submission
    comments = submission.get_top_comments(best_submission)

    print("Got comments")

    # save title and comments as mp3 file
    submission.save_title_and_comments(best_submission.title, comments)
    print("Saved as mp3")

    # concatenate the audio files
    cat_audio_files.create_and_save_mp3()
    print("Created full mp3")

    # create images for video
    create_video.create_images_from_text_list([comment.body for comment in comments]) # list of the body of comments
    create_video.create_img_with_text(best_submission.title, TITLE_IMG_PATH)
    print("Created images for video")

    times = cat_audio_files.get_len_of_all_mp3()
    create_video.add_frames_to_video(ONLY_VIDEO_PATH, create_video.FRAMES_FOLDER, times)

    create_video.add_audio_to_video(cat_audio_files.FULL_MP3_PATH, ONLY_VIDEO_PATH)

    print("\nDONE")


if __name__ == '__main__':
    main()
