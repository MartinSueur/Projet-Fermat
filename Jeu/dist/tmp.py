from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os

liste = []
for i in range(0,11):
    for j in range(0,11):
        if i+j>=7 and max(i,j) <= 8 and i!=j:
            liste.append((i,j))

for i,j in liste:
    # Get the desired video title
    title = f"videos/{i}_{j}.mp4"

    # Open the video and audio
    video_clip = VideoFileClip(title)
    audio_clip = AudioFileClip("1-minute-of-silence.mp3")

    # Concatenate the video clip with the audio clip
    final_clip = video_clip.set_audio(audio_clip)

    # Export the final video with audio
    final_clip.write_videofile(f"videos-with-audio/{i}_{j}.mp4")