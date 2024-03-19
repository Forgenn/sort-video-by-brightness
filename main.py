import argparse
import cv2
import numpy as np
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

def get_frame_brightness(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate the average brightness of the frame
    brightness = np.mean(gray_frame)
    return brightness

def sort_by_brightness(video_path):
    video = VideoFileClip(video_path)
    frames_brightness = []
    for frame_time in np.arange(0, video.duration, 1.0 / video.fps):
        frame = video.get_frame(frame_time)
        frame_brightness = get_frame_brightness(frame)
        frames_brightness.append((frame, frame_brightness, frame_time))

    # Sort frames based on brightness
    frames_brightness.sort(key=lambda x: x[1])

    new_clips = []
    for i, (_, _, frame_time) in enumerate(frames_brightness):
        if i != len(frames_brightness) - 2:
            clip = video.subclip(frame_time, frame_time + 1.0 / video.fps).set_start(i * 1.0 / video.fps)
            new_clips.append(clip)
            print(f"Processed clip {i+1}/{len(frames_brightness)}")

    final_clip = concatenate_videoclips(new_clips)
    output_path = video_path.split('.')[0] + "_brightness_sorted.mp4"
    final_clip.write_videofile(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort video frames by brightness")
    parser.add_argument("video_path", type=str, help="Path to input video file")
    args = parser.parse_args()
    sort_by_brightness(args.video_path)
