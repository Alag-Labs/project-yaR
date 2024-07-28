import os
import requests
from dotenv import load_dotenv
from Logger import Logger
from yaRException import yaRException, yaRErrorCodes
from pathlib import Path

load_dotenv()

def upload_video_and_handle_response(video_path, audio_path):
    url = os.getenv("VIDEO_PROCESSING_URL")
    token = os.getenv("API_TOKEN")

    if not url:
        Logger().logger.error("API URL or token not found in environment variables.")
        raise yaRException(yaRErrorCodes.VIDEO_UPLOAD_URL_NOT_FOUND)

    if not token:
        Logger().logger.error("API token not found in environment variables.")
        raise yaRException(yaRErrorCodes.VIDEO_UPLOAD_TOKEN_NOT_FOUND)
    
    headers = {"X-Token": token}
    video_file_name = Path(video_path).name
    audio_file_name = Path(audio_path).name

    if not Path(video_path).is_file():
        Logger().logger.error(f"The video file {video_path} does not exist.")
        raise yaRException(yaRErrorCodes.VIDEO_FILE_NOT_FOUND_WHILE_UPLOAD)
    
    if not Path(audio_path).is_file():
        Logger().logger.error(f"The audio file {audio_path} does not exist.")
        raise yaRException(yaRErrorCodes.AUDIO_FILE_NOT_FOUND_WHILE_UPLOAD)
    
    with open(video_path, "rb") as video_file, open(audio_path, "rb") as audio_file:
        files = {
            "video": (video_file_name, video_file, "video/mp4"),
            "audio": (audio_file_name, audio_file, "audio/wav")
        }
        response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        mp3_path = video_path.rsplit(".", 1)[0] + ".mp3"
        with open(mp3_path, "wb") as mp3_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  
                    mp3_file.write(chunk)
        Logger().logger.info(f"MP3 saved to {mp3_path}")
        return mp3_path
    else:
        Logger().logger.error(f"Error: {response.status_code} - {response.text}")
        raise yaRException(yaRErrorCodes.VIDEO_PROCESSING_FAILED)


if __name__ == "__main__":
    Logger(log_to_file=True).info("Starting yaR....")
    try:
        upload_video_and_handle_response("video.mp4", "audio.wav")
    except yaRException as e:
        Logger().logger.error(e)