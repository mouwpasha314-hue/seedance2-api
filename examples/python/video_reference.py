"""Video Reference: use a reference video to guide motion and choreography."""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from seedance import Seedance

API_KEY = os.environ.get("SEEDANCE_API_KEY", "YOUR_API_KEY")
client = Seedance(api_key=API_KEY)

result = client.generate(
    prompt="A robot dancing in a futuristic city, neon lights, cyberpunk style",
    model="seedance_2.0",
    duration=10,
    ratio="16:9",
    video_files=["https://example.com/dance-reference.mp4"],  # Replace with your video URL
)

print(f"Video URL: {result['video_url']}")
