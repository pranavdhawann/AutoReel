import os
import torch
import numpy as np
import soundfile as sf
from praw import Reddit
from moviepy.editor import AudioFileClip, VideoFileClip
from transformers import pipeline
from datasets import load_dataset
import whisper
import subprocess

# Initialize Reddit
reddit = Reddit(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET', user_agent='YOUR_USER_AGENT')

# Set paths (replace with appropriate paths)
BG_path = "path/to/background/video.mp4"
Audio_path = "path/to/generated/audio.wav"
Intermediate_video_path = "path/to/intermediate/video.mp4"
Output_path = "path/to/final_output_video.mp4"
SRT_path = "path/to/generated_subtitles.srt"

# Define subreddit to fetch posts from
subreddit = 'YOUR_SUBREDDIT'

# Set an appropriate chunk length for text-to-speech synthesis
max_chunk_length = 200

# Load speaker embeddings for the synthesizer
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

# Initialize text-to-speech synthesizer
synthesizer = pipeline("text-to-speech", "microsoft/speecht5_tts")

# Fetch hot posts from Reddit
hot_posts = list(reddit.subreddit(subreddit).hot(limit=2))

def split_text(text, max_length):
    """
    Split text into chunks of specified maximum length.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Process each post
for post in hot_posts[1:]:
    # Convert post title and content to speech
    text = post.selftext  # You can also concatenate title and content if needed
    text_chunks = split_text(text, max_chunk_length)
    audio_segments = []
    
    # Synthesize speech for each chunk
    for chunk in text_chunks:
        speech = synthesizer(chunk, forward_params={"speaker_embeddings": speaker_embedding})
        audio_segments.append(speech["audio"])

    # Concatenate all audio segments
    final_audio = np.concatenate(audio_segments, axis=0)
    sf.write(Audio_path, final_audio, samplerate=speech["sampling_rate"])

# Determine the duration of the generated audio
audioclip = AudioFileClip(Audio_path)
audio_duration = audioclip.duration

# Load the background video and trim it to the audio duration
videoclip = VideoFileClip(BG_path).subclip(0, audio_duration)

# Combine audio and video
videoclip = videoclip.set_audio(audioclip)
videoclip.write_videofile(Intermediate_video_path)

# Transcribe the audio using Whisper
model = whisper.load_model("base")
result = model.transcribe(Audio_path)

def generate_srt(transcription):
    """
    Generate SRT file content from the transcription.
    """
    srt = []
    for i, segment in enumerate(transcription['segments']):
        start = segment['start']
        end = segment['end']
        text = segment['text']
        start_time = format_timestamp(start)
        end_time = format_timestamp(end)
        srt.append(f"{i+1}\n{start_time} --> {end_time}\n{text}\n")
    return "\n".join(srt)

def format_timestamp(seconds):
    """
    Format seconds into SRT timestamp format.
    """
    hrs, secs = divmod(seconds, 3600)
    mins, secs = divmod(secs, 60)
    millis = (secs % 1) * 1000
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{int(millis):03}"

# Create SRT subtitles file
srt_content = generate_srt(result)
with open(SRT_path, "w") as f:
    f.write(srt_content)

# Overlay subtitles on the video using ffmpeg
subprocess.run(["ffmpeg", "-i", Intermediate_video_path, "-vf", f"subtitles={SRT_path}", Output_path], shell=True)

# Clean up temporary files
os.remove(Audio_path)
os.remove(Intermediate_video_path)
os.remove(SRT_path)