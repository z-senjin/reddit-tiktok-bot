#youtube video: https://www.youtube.com/watch?v=OhBo1A8atuA
from random import randrange, choice
from tkinter import W
from utils.console import print_step, print_header, print_substep, print_error
from pathlib import Path
from yt_dlp import YoutubeDL
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeAudioClip,
    CompositeVideoClip
)
import os

def get_video_length(video_length, clip_length):
    random_time = randrange(180, int(clip_length) - int(video_length))
    return random_time, random_time + video_length

def download_background():

    if not Path("assets/video/background.mp4").is_file():
        print_step("Downloading background video..")

        youtube_dl_option = {
            "outtmpl": "assets/video/background.mp4",
            "merge_output_format": "mp4",
        }

        with YoutubeDL(youtube_dl_option) as ydl:
            ydl.download("https://www.youtube.com/watch?v=OhBo1A8atuA")

        print_substep("Finished downloading background!")


def generate_background(video_length):
    print_header("Generating background video...")

    download_background()

    background_video = VideoFileClip("assets/video/background.mp4")

    start_time, end_time = get_video_length(video_length, background_video.duration)

    print_step("Extracting clip from background video..")
    
    ffmpeg_extract_subclip(
        "assets/video/background.mp4",
        start_time,
        end_time,
        targetname="assets/video/background_clip.mp4",
    )

    print_substep("Finished generating background!")


def generate_final_video(number_of_comments):
    W,H = 1080, 1920
    print_header("Generating final video...")

    opacity = os.getenv("OPACITY")

    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(height=W)

    background_clip = (VideoFileClip("assets/video/background_clip.mp4").without_audio().resize(height=H)
    .crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    )

    print_step('Appending clips together..')

    audio_clips = []
    for i in range(0, number_of_comments):
        audio_clips.append(AudioFileClip(f"assets/audio/comment{i}.mp3"))
    audio_clips.insert(0, AudioFileClip("assets/audio/title.mp3"))

    # try:
    #     audio_clips.append(AudioFileClip("assets/audio/posttext.mp3"))
    # except Exception as e:
    #     OSError()
    #     print_error(str(e))

    compiled_audio_clips = concatenate_audioclips(audio_clips)
    compiled_audio_composite = CompositeAudioClip([compiled_audio_clips])

    image_clips = []
    for i in range(0, number_of_comments):
        image_clips.append(ImageClip(f"assets/screenshots/comment{i}.png")
        .set_duration(audio_clips[i + 1].duration)
        .set_position("center")
        .resize(width=W - 100)
        .set_opacity(float(opacity))
        )

    # if os.path.exists(f"assets/audio/posttext.mp3") and os.path.exists(f"assets/screenshots/posttext.png"):
    #     image_clips.insert(0, ImageClip(f"assets/screenshots/posttext.png")
    #     .set_duration(audio_clips[0].duration + audio_clips[1].duration)
    #     .set_position("center")
    #     .resize(width=W - 100)
    #     .set_opacity(float(opacity)))
    # else:
    image_clips.insert(0, ImageClip(f"assets/screenshots/title.png").set_duration(audio_clips[0].duration)
    .set_position("center")
    .resize(width=W - 100)
    .set_opacity(float(opacity)))

    compiled_image_clips = concatenate_videoclips(image_clips).set_position(("center", "center"))

    compiled_image_clips.audio = compiled_audio_composite

    final_video = CompositeVideoClip([background_clip, compiled_image_clips])
    random_string = "".join(choice("abcdefghijklmnopqrstuvwxyz") for i in range(10))
    filename = "final/" + str(random_string) + ".mp4"
    final_video.write_videofile(filename, fps=30, audio_codec="aac", audio_bitrate="192k")
