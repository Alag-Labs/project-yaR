import pygame
import subprocess

def play_audio(audio_path):
    """
    Play audio using the pygame library. This function is used to play the response audio after the video and audio files are processed. 

    Also used to play auditory feedback when the button is pressed.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def record_audio(audio_path):
    """
    Record audio using the built in arecord command. Starting a new process to record audio to prevent blocking the main thread.
    """
    command = ["arecord", "-D", "dmic_sv", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "wav", "-V", "mono", "-v", audio_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process
