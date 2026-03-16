"""Image + Audio: combine a portrait with audio for lip-sync animation."""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from seedance import Seedance

API_KEY = os.environ.get("SEEDANCE_API_KEY", "YOUR_API_KEY")
client = Seedance(api_key=API_KEY)

result = client.generate(
    prompt="The person in @image_file_1 is speaking naturally with expressive gestures",
    model="seedance_2.0",
    duration=8,
    ratio="9:16",
    image_files=["https://example.com/portrait.jpg"],      # Replace with your image URL
    audio_files=["https://example.com/voiceover.mp3"],      # Replace with your audio URL
)

print(f"Video URL: {result['video_url']}")
