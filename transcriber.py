from moviepy import VideoFileClip
import whisper
import os

def extract_audio(video_path='video.mp4', audio_path='audio.wav'):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path='audio.wav'):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']

def process_video_to_text(video_path='video.mp4'):
    audio_path = extract_audio(video_path)
    transcript = transcribe_audio(audio_path)
    os.remove(audio_path)  # optional: cleanup
    return transcript
