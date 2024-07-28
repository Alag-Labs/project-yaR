# yaR: AI-Powered Pendant for the Visually Impaired

yaR is an open-source AI wearable device designed to assist visually impaired individuals in navigating the world with greater confidence and independence.

## Project Overview

yaR started as a hackathon project and has evolved into a sophisticated AI-powered pendant. It uses a Raspberry Pi to capture visual input and process it to provide audio feedback to the user.

### Key Features

- Visual input processing using AI
- Audio feedback for users
- Lightweight and wearable design
- Open-source for community contributions

## Repository Structure

The repository is organized into two main folders:

1. `Client`: Contains the Python code for the Raspberry Pi
2. `Server`: Contains the Django Python code for the server

### Client Files

- `main.py`: The main script for the Raspberry Pi
- `audio_utils.py`: Utilities for audio processing
- `request_handler.py`: Handles requests to the server
- `Logger.py`: Logging utilities
- `yaRException.py`: Custom exception handling
- `requirements.txt`: Required Python packages for the client

### Server Files

- `manage.py`: Django management script
- `video_processing/`: Django app for video processing
  - `views.py`: Contains the view functions
  - `urls.py`: URL configurations
  - `utils/`: Utility functions for various tasks
- `server/`: Django project settings
- `requirements.txt`: Required Python packages for the server

## Getting Started

### Server

- Create a virtual environment and install the required Python packages using `pip install -r requirements.txt`.
- The following environment variables are required:
    - `OPENAI_API_KEY` - OpenAI API key
    - `ANTHROPIC_API_KEY` - Anthropic API key
- <Enter instructions on firebase credentials>
- Take note of the server's IP address/ domain and add it to the `ALLOWED_HOSTS` list in the [settings file](./Server/server/settings.py).
- Run the Django server using `python manage.py runserver 0.0.0.0:8000`.
- The server is now ready to receive requests from the Raspberry Pi client.


### Raspberry Client 

- Set up the Raspberry Pi with the required hardware as per the instructions in the `Hardware Guide` (coming soon). 
- Install the required Python packages on the Raspberry Pi using `pip3 install -r requirements.txt`.
- The following environment variables are required:
    - `VIDEO_PROCESSING_URL` - URL/ IP address of the above server
    - `API_TOKEN` - API token for the server. This token is synonymous to an identity token associated with each raspberry pi board. Currently, whenever the server receives a new token, it will create a new `board` in the firestore database. This is written in the [firebase utils file](./Server/video_processing/utils/firebase_utils.py). It should be changed to a more secure method in the future. For now, use a random string such as `1234`.
- Run the `main.py` script to start the client.

