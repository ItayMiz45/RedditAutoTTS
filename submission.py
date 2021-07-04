import praw
import datetime
from datetime import datetime
from gtts import gTTS

AUDIO_PATH = "audio"
TITLE_PATH = AUDIO_PATH + '/' + "title"
COMMENTS_PATH = AUDIO_PATH + '/' + "comments"

SUBREDDIT = "AskReddit"
REDDIT_SITE = "www.reddit.com"

ONE_MIN_NUM_CHARS = 650

reddit = praw.Reddit(client_id="", client_secret="")


def get_valid_submissions(subreddit):
    subreddit = reddit.subreddit(subreddit)

    submissions_last24 = []
    for submission in subreddit.hot(limit=100):
        # Used same utc standard for post time, and reference time that's checked when run.

        utc_post_time = submission.created
        submission_date = datetime.utcfromtimestamp(utc_post_time)

        current_time = datetime.utcnow()

        # How long ago it was posted.
        submission_delta = str(current_time - submission_date)

        """
        title = submission.title
        link = 'www.reddit.com' + submission.permalink
        score = submission.score
        """

        if 'day' not in submission_delta:
            submissions_last24.append(submission)

    return submissions_last24


def get_best_submission(valid_submissions):
    return max(valid_submissions, key=lambda item: item.score)


def get_num_of_comments(comments):
    i = 1
    string = ""

    print("function: Number of comments")

    while True:
        string = [c for c in string if c.isalpha()]
        string += comments[i].body

        if len(string) >= ONE_MIN_NUM_CHARS * 10:
            print("Number of letters:", len(string))
            print("Number of comments:", i)
            return i

        i += 1


def get_top_comments(submission):
    all_comments = []

    for comment in submission.comments:
        if type(comment) == praw.models.reddit.comment.Comment:
            all_comments.append(comment)

    all_comments.sort(key=lambda comment: comment.score, reverse=True)

    return all_comments[:get_num_of_comments(all_comments)]


def save_title_and_comments(title: str, comments: list):
    print("In save_title_and_comments")
    gTTS(title, "en").save(TITLE_PATH + '/' + "title.mp3")
    print("Saved title")

    for i, comment in enumerate(comments, start=1):
        gTTS(comment.body, "en").save(COMMENTS_PATH + '/' + f"comment{str(i).zfill(3)}.mp3")
        print("Saved comment", i)


def main():
    valid_submissions = get_valid_submissions(SUBREDDIT)
    best_submission = get_best_submission(valid_submissions)
    comments = get_top_comments(best_submission)

    save_title_and_comments(best_submission.title, comments)


if __name__ == '__main__':
    main()
