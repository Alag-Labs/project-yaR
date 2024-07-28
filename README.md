# yaR: AI-Powered Pendant for the Visually Impaired

yaR is an open-source AI wearable device designed to assist visually impaired individuals in navigating the world with greater confidence and independence.

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Server Setup](#server-setup)
  - [Raspberry Pi Client Setup](#raspberry-pi-client-setup)
- [License](#license)

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

### Server Setup

1. Create a virtual environment and install the required Python packages:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - `OPENAI_API_KEY`: OpenAI API key
   - `ANTHROPIC_API_KEY`: Anthropic API key

3. Firebase Credentials Setup:
   - Create a new Firebase project in the [Firebase Console](https://console.firebase.google.com/)
   - Generate a new private key:
     - Go to Project Settings > Service Accounts
     - Click "Generate new private key"
   - Rename the downloaded JSON file to `yar-v2.json`
   - Move `yar-v2.json` to the `video_processing` folder

   **Important:** Keep `yar-v2.json` secure and never expose it publicly.

4. Configure Django:
   - Add the server's IP address/domain to `ALLOWED_HOSTS` in `Server/server/settings.py`

5. Run the Django server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

### Raspberry Pi Client Setup

1. Set up the Raspberry Pi hardware (Hardware Guide coming soon)

2. Install required Python packages:
   ```
   pip3 install -r requirements.txt
   ```

3. Set up environment variables:
   - `VIDEO_PROCESSING_URL`: URL/IP address of the server
   - `API_TOKEN`: API token for the server (e.g., "1234")

4. Run the client:
   ```
   python main.py
   ```

## License

This project is licensed under the [MIT License](LICENSE).
