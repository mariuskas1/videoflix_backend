import subprocess
import os


def convert_video(input_path, output_path, resolution):
    command = [
        'ffmpeg', '-i', input_path, '-vf', f"scale=-2:{resolution}",
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'aac', '-b:a', '128k', output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def convert_120p(input_path):
    output_path = input_path.replace('.mp4', '_120p.mp4')
    convert_video(input_path, output_path, 120)


def convert_360p(input_path):
    output_path = input_path.replace('.mp4', '_360p.mp4')
    convert_video(input_path, output_path, 360)


def convert_720p(input_path):
    output_path = input_path.replace('.mp4', '_720p.mp4')
    convert_video(input_path, output_path, 720)


def convert_1080p(input_path):
    output_path = input_path.replace('.mp4', '_1080p.mp4')
    convert_video(input_path, output_path, 1080)