"""Image-to-Video: animate a still image into a video."""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from seedance import Seedance

API_KEY = os.environ.get("SEEDANCE_API_KEY", "YOUR_API_KEY")
client = Seedance(api_key=API_KEY)

result = client.generate(
    prompt="The girl in @image_file_1 smiles and turns around slowly, hair flowing in the wind",
    model="seedance_2.0_fast",
    duration=5,
    ratio="16:9",
    image_files=["https://example.com/girl-portrait.jpg"],  # Replace with your image URL
)

print(f"Video URL: {result['video_url']}")
