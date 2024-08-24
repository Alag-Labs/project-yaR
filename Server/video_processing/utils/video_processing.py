import os
import cv2
from imutils import paths
from moviepy.editor import VideoFileClip


def extract_audio(video_file_path):
    """
    Extract audio from a video file.

    Args:
        video_file_path (str): Path to the input video file.

    Returns:
        str: Path to the extracted audio file (MP3).
    """
    mp3_file = video_file_path.rsplit(".", 1)[0] + ".mp3"

    # Load the video clip
    video_clip = VideoFileClip(video_file_path)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    # Write the audio to a separate file
    audio_clip.write_audiofile(mp3_file)

    # Close the video and audio clips
    audio_clip.close()
    video_clip.close()

    return mp3_file


def variance_of_laplacian(image):
    """
    Compute the Laplacian variance of an image.

    This function is used to measure the focus/blurriness of an image.
    Higher variance indicates a less blurry image.

    Args:
        image (numpy.ndarray): Grayscale image.

    Returns:
        float: Variance of the Laplacian.
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()


def find_least_blurry_frame(directory):
    """
    Find the least blurry image in a directory of images.

    Args:
        directory (str): Path to the directory containing images.

    Returns:
        str: Path to the least blurry image.

    Raises:
        Exception: If no frames are found in the directory.
    """
    highest_focus_measure = 0
    least_blurry_image_path = None

    for image_path in paths.list_images(directory):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        if fm > highest_focus_measure:
            highest_focus_measure = fm
            least_blurry_image_path = image_path

    if least_blurry_image_path is None:
        raise Exception("No frames found in the directory")

    return least_blurry_image_path


def extract_and_find_least_blurry_frame(video_file_path, directory="frames"):
    """
    Extract frames from a video file and find the least blurry frame.

    This function processes the video, saves frames to a directory,
    finds the least blurry frame, and cleans up other frames.

    Args:
        video_file_path (str): Path to the video file.
        directory (str): Directory to save extracted frames. Defaults to "frames".

    Returns:
        str: Path to the least blurry frame.

    Raises:
        Exception: If there's an error opening the video file or no frames are found.
    """
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        raise Exception("Error opening video file")

    if not os.path.exists(directory):
        os.makedirs(directory)

    highest_focus_measure = 0
    least_blurry_frame_path = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)

        if fm > highest_focus_measure:
            highest_focus_measure = fm
            least_blurry_frame_path = os.path.join(
                directory, f"frame-{frame_count}.jpg"
            )
            cv2.imwrite(least_blurry_frame_path, frame)

        frame_count += 1

    cap.release()

    if least_blurry_frame_path is None:
        raise Exception("No frames found in the video")

    # Clean up other frames
    for file in os.listdir(directory):
        if file != os.path.basename(least_blurry_frame_path):
            os.remove(os.path.join(directory, file))

    return least_blurry_frame_path
