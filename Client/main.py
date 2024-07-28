import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from libcamera import controls
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from request_handler import upload_video_and_handle_response
from yaRException import yaRException
from Logger import Logger
from audio_utils import play_audio, record_audio


####################### RPI GPIO SETUP #######################
# Using BCM numbering, not the physical pin number
GPIO.setmode(GPIO.BCM)
button_pin = 2
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
###############################################################


###################### Buffer Variables ######################
video_path = 'video.h264'
audio_path = 'recording3.wav'
##############################################################


###################### Camera Setup ##########################
picam2 = Picamera2()
picam2.start(show_preview=False)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
##############################################################


def main():
    """
    The main function that runs the game loop. This function is responsible for handling the game loop and the button press event. 
    """
    
    # Initialise the Logger. Read the Logger class in Logger.py for more information.
    Logger(log_to_file=True).info("Starting yaR....")

    # Variables
    is_recording = False
    audio_process = None  # Declare audio_process variable

    try:
        while True:
            if not GPIO.input(button_pin):
                if not is_recording:
                    Logger().info("Button pressed. Starting camera and audio recording...")

                    audio_process = record_audio()
                    encoder = H264Encoder()
                    output = FileOutput(video_path)
                    picam2.start_recording(encoder, output)
                    is_recording = True
                    time.sleep(1)
                else:
                    Logger().info("Button pressed. Stopping recording and camera...")

                    picam2.stop_recording()
                    audio_process.terminate()
                    audio_process.wait()
                    
                    if audio_process.returncode is not None:
                        Logger().info("Audio recording stopped successfully.")
                    else:
                        Logger().error("There was an issue stopping the audio recording.")
                        # # Continue with the loop. Can be changed to raise an exception if required.
                        # raise yaRException(yaRErrorCodes.AUDIO_RECORDING_FAILED)
                    
                    try:
                        mp3_path = upload_video_and_handle_response(video_path, audio_path)
                    except yaRException as e:
                        # Exception handling for the upload_video_and_handle_response function. Already logged in the function.
                        pass
                    
                    if mp3_path:
                        play_audio(mp3_path)
                    
                    is_recording = False
                    time.sleep(1)  # Debounce delay to avoid multiple button presses
            else:
                time.sleep(0.01)
    except KeyboardInterrupt:
        Logger().info("Stopping gracefully... Press Ctrl+C again to force stop.")

        if is_recording:
            picam2.stop_recording()
            picam2.close()
            audio_process.terminate()
            audio_process.wait()
        GPIO.cleanup()

        Logger().info("Cleanup complete. Exiting yaR.")


if __name__ == "__main__":
    main()