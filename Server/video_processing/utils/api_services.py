import os
import requests
import anthropic
import base64
import json

# Load API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

def convert_speech_to_text(audio_file_path, model="whisper-1"):
    """
    Convert speech in an audio file to text using OpenAI's Whisper model.

    Args:
        audio_file_path (str): Path to the audio file.
        model (str): The model to use for speech recognition. Default is "whisper-1".

    Returns:
        str: The transcribed text.

    Raises:
        Exception: If the API request fails.
    """
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
    }
    files = {
        "file": ("openai.mp3", open(audio_file_path, "rb"), "audio/mpeg"),
        "model": (None, model),
    }
    response = requests.post(
        "https://api.openai.com/v1/audio/translations", headers=headers, files=files
    )
    if response.status_code == 200:
        response_data = response.json()
        transcript = response_data["text"]
        return transcript
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def convert_text_to_speech(input_text, board_token, model="tts-1", voice="alloy", directory="response"):
    """
    Convert text to speech using OpenAI's Text-to-Speech model.

    Args:
        input_text (str): The text to convert to speech.
        board_token (str): A unique identifier for the board.
        model (str): The TTS model to use. Default is "tts-1".
        voice (str): The voice to use. Default is "alloy".
        directory (str): The directory to save the audio file. Default is "response".

    Yields:
        bytes: Chunks of the audio file.

    Raises:
        Exception: If the API request fails.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = os.path.join(directory, f"response-{board_token}.mp3")
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "input": input_text, "voice": voice, "language": "en"}
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers=headers,
        json=payload,
        stream=True,
    )
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def image_to_text(image_path, prompt, model="claude-3-haiku-20240307", max_tokens=250):
    """
    Convert an image to descriptive text using Anthropic's Claude model.

    Args:
        image_path (str): Path to the image file.
        prompt (str): The user's prompt or question about the image.
        model (str): The Claude model to use. Default is "claude-3-haiku-20240307".
        max_tokens (int): Maximum number of tokens in the response. Default is 250.

    Returns:
        str: The generated text description of the image.

    Raises:
        Exception: If the API request fails.
    """
    client = anthropic.Client(api_key=anthropic_api_key)
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system="The user is visually impaired and is seeking assistance to gain environmental awareness through this query. Using the details provided in the image and the user's prompt, generate a response that is helpful, relevant, and respectful of privacy. Maintain the language and tone of the user's prompt, and ensure the response is assistive in nature. The cost of not providing a useful response could be significant, so prioritize accuracy and utility. Be concise when required, and provide additional context when necessary. RESPOND ONLY IN ENGLISH",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    message = message.json()
    message = json.loads(message)
    text_response = message["content"][0]["text"]
    return text_response