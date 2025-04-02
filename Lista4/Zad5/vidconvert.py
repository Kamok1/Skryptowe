import os
import subprocess
import sys
import argparse
import utils
import logging

FFMPEG_COMMAND = 'ffmpeg'
MAGICK_COMMAND = 'magick'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_file(file_path, output_format, command, extra_args=None):
    output_path = utils.get_output_path(file_path, output_format)
    result = run_command([command] + (extra_args or []) + [file_path, output_path])
    utils.log_conversion(file_path, output_path, output_format, command, result)

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return str(e)

def convert_files(directory_path, video_format, photo_format):
    files = os.listdir(directory_path)
    has_videos = any(utils.is_video_or_audio(f) for f in files)
    has_images = any(utils.is_image(f) for f in files)

    if has_images and not photo_format:
        logger.error("Brak parametru -pf dla konwersji obrazów!")
        return

    if has_videos and not video_format:
        logger.error("Brak parametru -vf dla konwersji wideo!")
        return

    for file in files:
        file_path = os.path.join(directory_path, file)

        if not os.path.isfile(file_path):
            continue
        if not os.access(file_path, os.R_OK):
            logger.warning(f"Brak dostępu do pliku {file_path}.")
            continue

        if utils.is_video_or_audio(file_path) and video_format:
            convert_file(file_path, video_format, FFMPEG_COMMAND, extra_args=['-i'])
        elif utils.is_image(file_path) and photo_format:
            convert_file(file_path, photo_format, MAGICK_COMMAND)
        else:
            logger.warning(f"Plik {file} nie ma obsługiwanego formatu.")

def parse_args():
    parser = argparse.ArgumentParser(description="Skrypt do konwersji plików wideo/audio oraz obrazów")
    parser.add_argument("directory", help="Ścieżka do katalogu z plikami do konwersji")
    parser.add_argument("-vf", "--video_format", help="Format wyjściowy (np. 'mp4', 'webm')", required=False)
    parser.add_argument("-pf", "--photo_format", help="Format wyjściowy (np. 'jpg', 'png')", required=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if not os.path.isdir(args.directory):
        logger.error(f"Podana ścieżka {args.directory} nie jest katalogiem.")
        sys.exit(1)

    convert_files(args.directory, args.video_format, args.photo_format)
