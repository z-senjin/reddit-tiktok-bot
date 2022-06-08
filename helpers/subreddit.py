from config import config
import os
from utils.console import print_error, print_header, print_step, print_substep
import praw
import random
from dotenv import load_dotenv

load_dotenv()

def get_subreddits():
    print_header('Getting reddit posts...')
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD')
        )

    genre =  config['genres'][random.randint(0, len(config['genres']))]
    print_step('Searching subreddit: ' + genre)

    posts = reddit.subreddit(genre).hot(limit=config['max_posts_per_genre'])

    submission = list(posts)[random.randrange(0, config['max_posts_per_genre'])]
    
    print_substep('Post score: ' + str(submission.score))
    print_substep(f"Submission title: {submission.title}");

    content = {}

    try:
        print_step('Getting comments...')

        content['post_title'] = submission.title
        content['post_url'] = submission.url
        content['post_score'] = submission.score
        content['post_text'] = submission.selftext
        content['post_id'] = submission.id
        content['post_comments'] = []

        for comment in submission.comments:
            comment_length = len(comment.body.split())
            if(type(comment) is praw.models.MoreComments):
                break
            if not comment.stickied and comment_length < config['max_comment_word_length']:
                content['post_comments'].append({
                    "comment_id": comment.id,
                    "comment_url": comment.permalink,
                    "comment_text": comment.body,
                })
                
    except Exception as e:
        print_error(str(e))
    
    print_substep("Successfully retrieved comments for post!")
    print_substep("Title: " + content['post_title'])
    print_substep('Post score: ' + str(content['post_score']))
    print_substep('Number of comments: ' + str(len(content['post_comments'])))

    return content


