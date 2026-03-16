"""Text-to-Video: generate a video from a text prompt."""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from seedance import Seedance

API_KEY = os.environ.get("SEEDANCE_API_KEY", "YOUR_API_KEY")
client = Seedance(api_key=API_KEY)

result = client.generate(
    prompt="A cat playing piano in a jazz bar, cinematic lighting, warm tones",
    model="seedance_2.0_fast",
    duration=5,
    ratio="16:9",
)

print(f"Video URL: {result['video_url']}")
print(f"Duration:  {result.get('duration', 'N/A')}s")
