Voice Assistant
A Python-based voice assistant that responds to voice commands prefixed with "hey vishesh". It can open applications, browse websites, play music on Spotify, fetch weather updates, take notes, read notes, set timers, and more. The assistant uses speech recognition and text-to-speech for interaction, with modular design and error handling for robustness.
Features

Voice Activation: Responds to commands starting with "hey vishesh".
Application Launch: Opens applications like Chrome or Android Studio.
Website Navigation: Opens websites like YouTube, Google, or Spotify.
Spotify Integration: Plays songs or searches on Spotify.
Weather Updates: Fetches real-time weather using the OpenWeatherMap API.
Note-Taking: Saves and reads notes with timestamps.
Timer Functionality: Sets timers with voice alerts.
Logging: Tracks actions and errors in assistant.log.
Extensible: Mock AI processing for future integration with APIs like xAI's (https://x.ai/api).

Prerequisites

Python 3.8+
Libraries: speechrecognition, pyttsx3, requests
OpenWeatherMap API key for weather functionality
A microphone for voice input
Windows system (for application paths; modify for other OS)

Installation

Clone the Repository (or download the script):git clone <repository-url>
cd <repository-directory>


Install Dependencies:pip install speechrecognition pyttsx3 requests


Set Up OpenWeatherMap API Key:
Sign up at OpenWeatherMap to get an API key.
Set the key as an environment variable:export OPENWEATHER_API_KEY='your-api-key'  # Linux/Mac
set OPENWEATHER_API_KEY=your-api-key       # Windows




Configure Application Paths:
Edit APP_COMMANDS in voice_assistant.py to match your system's application paths (e.g., for Chrome, Android Studio).



Usage

Run the script:python voice_assistant.py


The assistant will say: "Hello Vishesh. Say 'hey vishesh' followed by your command."
Speak commands clearly, starting with "hey vishesh". Examples:
"hey vishesh open chrome"
"hey vishesh play believer on spotify"
"hey vishesh check weather in delhi"
"hey vishesh take a note buy groceries"
"hey vishesh read notes"
"hey vishesh set timer for 10 seconds"
"hey vishesh exit"



Example Interaction
[Assistant]: Hello Vishesh. Say 'hey vishesh' followed by your command.
Listening...
[Heard]: hey vishesh open chrome
[Assistant]: Opening chrome
[Heard]: hey vishesh check weather in delhi
[Assistant]: In Delhi, it's 28 degrees Celsius with clear sky.
[Heard]: hey vishesh take a note buy groceries
[Assistant]: Note saved: buy groceries
[Heard]: hey vishesh exit
[Assistant]: Goodbye.

Configuration

Wake Word: Change WAKE_WORD in the script (default: "hey vishesh").
Applications: Update APP_COMMANDS with paths to your applications.
Websites: Modify SITE_KEYWORDS to add or change website mappings.
Microphone: Adjust device_index in the listen function if your microphone isn't detected (default: 1).

Notes

Paths in APP_COMMANDS are set for Windows; update for macOS/Linux as needed.
Notes are saved in assistant_notes.txt in the script's directory.
Logs are written to assistant.log for debugging.
The process_command_with_ai function uses a mock AI; replace with a real API (e.g., xAI's API) for advanced command processing.

Troubleshooting

Microphone Issues: Ensure your microphone is connected and set as the default input device. Try different device_index values.
Application Not Opening: Verify paths in APP_COMMANDS are correct.
Weather Errors: Ensure OPENWEATHER_API_KEY is set and valid.
Speech Recognition Fails: Check internet connection (required for Google Speech API) or adjust energy_threshold in the listen function.

MIT License - feel free to modify and distribute.
Contributing
Submit issues or pull requests to the repository for bug fixes or new features.
