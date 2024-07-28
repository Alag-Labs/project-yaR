import os

def save_video_file(video_file, board_token, directory="uploads"):
    """
    Save an uploaded video file to a specified directory.

    Args:
        video_file (UploadedFile): The uploaded video file object.
        board_token (str): A unique identifier for the board, used in the filename.
        directory (str): The directory to save the file. Defaults to "uploads".

    Returns:
        str: The path to the saved video file.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Generate the file path
    video_file_path = os.path.join(directory, f"video-{board_token}.mp4")
    
    # Save the file
    with open(video_file_path, "wb") as f:
        for chunk in video_file.chunks():
            f.write(chunk)
    
    return video_file_path

def save_audio_file(uploaded_audio, board_token, directory="audio"):
    """
    Save an uploaded audio file to a specified directory.

    Args:
        uploaded_audio (UploadedFile): The uploaded audio file object.
        board_token (str): A unique identifier for the board, used in the filename.
        directory (str): The directory to save the file. Defaults to "audio".

    Returns:
        str: The path to the saved audio file.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Generate the file path
    audio_file_path = os.path.join(directory, f"audio-{board_token}.wav")
    
    # Save the file
    with open(audio_file_path, "wb") as wf:
        for chunk in uploaded_audio.chunks():
            wf.write(chunk)
    
    return audio_file_path