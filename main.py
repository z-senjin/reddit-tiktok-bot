from helpers.subreddit import get_subreddits
from helpers.speech import convert_text_to_speech
from helpers.screenshot import download_reddit_screenshots
from helpers.video import generate_background, generate_final_video




reddit_content = get_subreddits()
length, number_of_comments = convert_text_to_speech(reddit_content)
download_reddit_screenshots(reddit_content, number_of_comments)
generate_background(length)
final_video = generate_final_video(number_of_comments)
