from utils.console import print_error, print_header, print_step, print_substep
from pathlib import Path
from gtts import gTTS
from mutagen.mp3 import MP3
from rich.progress import track

def convert_text_to_speech(reddit_content):
    print_header('Converting text to speech...')
    video_length = 0

    Path("assets/audio").mkdir(parents=True, exist_ok=True)

    print_step("Generating audio files...")
    title_tts = gTTS(text=reddit_content['post_title'], lang='en')
    title_tts.save("assets/audio/title.mp3")

    video_length += MP3(f"assets/audio/title.mp3").info.length

    try:
        Path("assets/audio/posttext.mp3").unlink()
    except OSError as e:
        print_error(str(e))
        pass

    # if reddit_content['post_text'] != "":
    #     posttext_tts = gTTS(text=reddit_content['post_text'], lang='en')
    #     posttext_tts.save("assets/audio/posttext.mp3")
    #     video_length += MP3(f"assets/audio/posttext.mp3").info.length
    count = 0
    for i, comment in track(enumerate(reddit_content['post_comments']), 'Saving comment..'):
        count += 1
        if video_length > 50:
            break
        comment_tts = gTTS(text=comment['comment_text'], lang='en')
        comment_tts.save(f"assets/audio/comment{i}.mp3")
        video_length += MP3(f"assets/audio/comment{i}.mp3").info.length
    
    print_substep("Saved MP3 to [ assets/audio/ ]  successfully!")
    print_substep(f"Video length: {video_length} seconds")

    return video_length, count

