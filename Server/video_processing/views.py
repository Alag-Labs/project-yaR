import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .config.firebase_config import firestore
from .utils import (
    save_audio_file,
    save_video_file,
    convert_speech_to_text,
    upload_image_to_storage,
    image_to_text,
    convert_text_to_speech,
    add_query_to_board,
    get_time,
    extract_and_find_least_blurry_frame,
    extract_audio,
)
from .utils.Logger import Logger


@csrf_exempt
def upload_video(request):
    """
    Main view function to handle video upload, processing, and response generation.

    This function orchestrates the entire process of receiving video and audio files,
    processing them, generating a response, and initiating background tasks.
    """
    logger = Logger(log_to_file=True)

    # Validate request method
    if request.method != "POST":
        logger.warning("Invalid request method")
        return HttpResponse({"error": "Invalid request method"}, status=405)

    # Check for board token in headers
    board_token = request.headers.get("X-Token")
    if not board_token:
        logger.error("Token is required")
        return HttpResponse({"message": "Token is required"}, status=400)

    # Validate presence of both video and audio files
    video_file = request.FILES.get("video")
    if not video_file:
        logger.error("Video and audio are required")
        return HttpResponse({"message": "Video and audio are required"}, status=400)

    start_time = time.time()
    logger.info(f"Received video and audio files - Timer started at {start_time}")

    try:
        # Save incoming files
        video_file_path = save_files(video_file, board_token, logger, start_time)

        # Process files to extract information
        least_blurry_frame, transcript, vision_response, audio_file_path = (
            process_files(video_file_path, logger)
        )

        # Convert the vision response to speech
        audio_stream = convert_text_to_speech(vision_response, board_token)

        # Prepare the streaming response
        response = StreamingHttpResponse(audio_stream, content_type="audio/mpeg")

        # Start a background thread for saving image and query
        threading.Thread(
            target=save_image_and_query,
            args=(
                least_blurry_frame,
                board_token,
                transcript,
                vision_response,
                video_file_path,
                audio_file_path,
                logger,
            ),
        ).start()

        return response
    except Exception as e:
        logger.error(f"Error in upload_video: {e}")
        return HttpResponse({"message": "An error occurred"}, status=500)


def save_files(video_file, board_token, logger, start_time):
    """
    Save the uploaded video and audio files.

    Args:
        video_file (File): The uploaded video file.
        board_token (str): The board token for identification.
        logger (Logger): The logger instance for logging events.
        start_time (float): The start time of the overall process.

    Returns:
        tuple: Path of the saved video file
    """
    video_file_path = save_video_file(video_file, board_token)
    logger.info(f"Video file saved, Time taken: {get_time(start_time)}")

    return video_file_path


def process_files(video_file_path, logger):
    """
    Process the video file concurrently.

    This function extracts the least blurry frame from the video,
    extracts audio, converts speech to text, and generates a vision response.

    Args:
        video_file_path (str): Path to the saved video file.
        logger (Logger): The logger instance for logging events.

    Returns:
        tuple: The least blurry frame, transcript, and vision response.
    """
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Extract least blurry frame from video
        future_frame = executor.submit(
            extract_and_find_least_blurry_frame, video_file_path
        )
        # Extract audio from video
        future_audio = executor.submit(extract_audio, video_file_path)
        logger.info(f"Extracted audio, Time taken: {get_time(time.time())}")

        least_blurry_frame = future_frame.result()
        logger.info(f"Least blurry frame found, Time taken: {get_time(time.time())}")

        audio_file_path = future_audio.result()
        logger.info(f"Audio extracted, Time taken: {get_time(time.time())}")

        # Convert speech to text
        transcript = convert_speech_to_text(audio_file_path)
        logger.info(f"Transcript made, Time taken: {get_time(time.time())}")

        # Generate vision response based on the frame and transcript
        vision_response = executor.submit(
            image_to_text, least_blurry_frame, transcript
        ).result()
        logger.info(f"Vision response generated, Time taken: {get_time(time.time())}")

    return least_blurry_frame, transcript, vision_response, audio_file_path


def save_image_and_query(
    least_blurry_frame,
    board_token,
    transcript,
    vision_response,
    video_file_path,
    audio_file_path,
    logger,
):
    """
    Save the processed image and query to storage and database.

    This function runs as a background task to upload the image,
    save the query, and clean up temporary files.

    Args:
        least_blurry_frame (str): Path to the least blurry frame image.
        board_token (str): The board token for identification.
        transcript (str): The generated transcript from audio.
        vision_response (str): The generated vision response.
        video_file_path (str): Path to the temporary video file.
        audio_file_path (str): Path to the temporary audio file.
        logger (Logger): The logger instance for logging events.
    """
    try:
        # Upload the least blurry frame to storage
        image_url = upload_image_to_storage(least_blurry_frame, board_token)
        logger.info(f"Image uploaded, Time taken: {get_time(time.time())}")

        # Save the query to the board
        add_query_to_board(
            board_token,
            {
                "prompt": transcript,
                "response": vision_response,
                "created_at": firestore.SERVER_TIMESTAMP,
                "image_url": image_url,
            },
        )
        logger.info(f"Query saved, Time taken: {get_time(time.time())}")

        # Clean up temporary files
        for file_path in [video_file_path, audio_file_path, least_blurry_frame]:
            os.remove(file_path)
        logger.info("Temporary files removed")
    except Exception as e:
        logger.error(f"Error in saving image and query: {e}")
