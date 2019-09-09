import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='CPZ4C94UUmsr2Q',
                     client_secret='SSe0KyC-R87TmOMxCwc-Xn5xuhM',
                     user_agent='Zero315'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments

counter = 0

#  We pass the lists as parameters to not delete previously created lists while iterating through comment
def process_comments(comments, negative_comments_list, neutral_comments_list, positive_comments_list):

    for comment in comments:
        global counter
        if len(comment.replies) > 0:  # Only iterate through replies if there are any
            process_comments(comment.replies, negative_comments_list, neutral_comments_list, positive_comments_list)

        if counter < 8:
            print("Counter: %d\t Comment: %s\n\n%s\n\n" % (counter, comment, comment.body))
            counter += 1

        # Get the sentiment value of the current comment to compare them and add them to the proper list
        neg, neu, pos = (get_text_negative_proba(comment.body),
                         get_text_neutral_proba(comment.body),
                         get_text_positive_proba(comment.body))

        if neg < neu and pos < neu:
            # print("this comments are neutral: %s with value %f" % (comment, neu))
            neutral_comments_list.append(comment)
            # print(neutral_comments_list)
        elif pos < neg and neu < neg:
            # print("this comments are negative: %s with value %f" % (comment, neg))
            negative_comments_list.append(comment)
            # print(negative_comments_list)
        elif neu < pos and neg < pos:
            # print("this comments are positive: %s with value %f" % (comment, pos))
            positive_comments_list.append(comment)
            # print(positive_comments_list)

def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')

    neg, neu, pos = ([], [], [])

    process_comments(comments, neg, neu, pos)

    print("These are Neutral")
    for i in neu:
        print("Comment %s has a Neu value: %s" % (i, get_text_neutral_proba(i.body)))

    print("These are Negative")
    for i in neg:
        print("Comment %s has a Neg value: %s" % (i, get_text_negative_proba(i.body)))

    print("These are Positive")
    for i in pos:
        print("Comment %s has a Pos value: %s" % (i, get_text_positive_proba(i.body)))

main()
