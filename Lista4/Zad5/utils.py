import os
import json
from datetime import datetime


HISTORY_FILE = 'history.json'
DEFAULT_ENCODING = 'utf-8'

def get_output_dir():
    return os.environ.get('CONVERTED_DIR', 'converted/')

def log_conversion(file_path, output_path, output_format, program_used, error):
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_file": file_path,
        "output_file": output_path,
        "output_format": output_format,
        "program_used": program_used,
    }
    if error:
        log_data["error"] = error

    log_file = os.path.join(get_output_dir(), HISTORY_FILE)

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding=DEFAULT_ENCODING) as file:
            history = json.load(file)
    else:
        history = []

    history.append(log_data)

    with open(log_file, 'w', encoding=DEFAULT_ENCODING) as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

def generate_file_name(file_path, output_format):
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{timestamp}-{os.path.basename(file_path).split('.')[0]}.{output_format}"

def get_output_path(file_path, output_format):
    new_file_name = generate_file_name(file_path, output_format)
    output_dir = get_output_dir()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return os.path.join(output_dir, new_file_name)

def is_video_or_audio(file_path):
    video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.webm']
    audio_formats = ['.mp3', '.wav', '.flac', '.aac']

    _, ext = os.path.splitext(file_path)
    return ext.lower() in video_formats + audio_formats


def is_image(file_path):
    image_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in image_formats
