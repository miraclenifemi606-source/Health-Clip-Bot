from moviepy.editor import VideoFileClip

def create_clip(video_path, start, end, output_path):
    video = VideoFileClip(video_path).subclip(start, end)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
