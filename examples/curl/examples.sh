#!/bin/bash
# Seedance 2.0 API - cURL Examples
# Replace YOUR_API_KEY with your actual API key from https://seed2.io/account

API_KEY="${SEEDANCE_API_KEY:-YOUR_API_KEY}"
BASE="https://api.seed2.io"

# ============================================================
# 1. Text to Video
# ============================================================
echo "=== Text to Video ==="
curl -s -X POST "$BASE/v1/video/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat playing piano in a jazz bar, cinematic lighting",
    "model": "seedance_2.0_fast",
    "duration": 5,
    "ratio": "16:9"
  }'

echo -e "\n"

# ============================================================
# 2. Image to Video
# ============================================================
echo "=== Image to Video ==="
curl -s -X POST "$BASE/v1/video/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The girl in @image_file_1 smiles and turns around slowly, hair flowing in the wind",
    "model": "seedance_2.0_fast",
    "duration": 5,
    "ratio": "16:9",
    "image_files": ["https://example.com/girl-portrait.jpg"]
  }'

echo -e "\n"

# ============================================================
# 3. Video Reference
# ============================================================
echo "=== Video Reference ==="
curl -s -X POST "$BASE/v1/video/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A robot dancing in a futuristic city, neon lights, cyberpunk style",
    "model": "seedance_2.0",
    "duration": 10,
    "ratio": "16:9",
    "video_files": ["https://example.com/dance-reference.mp4"]
  }'

echo -e "\n"

# ============================================================
# 4. Image + Audio (Lip-sync)
# ============================================================
echo "=== Image + Audio ==="
curl -s -X POST "$BASE/v1/video/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The person in @image_file_1 is speaking naturally with expressive gestures",
    "model": "seedance_2.0",
    "duration": 8,
    "ratio": "9:16",
    "image_files": ["https://example.com/portrait.jpg"],
    "audio_files": ["https://example.com/voiceover.mp3"]
  }'

echo -e "\n"

# ============================================================
# 5. Query Task Status
# ============================================================
echo "=== Query Task ==="
# Replace 123 with your actual task_id from the create response
curl -s "$BASE/v1/tasks/123" \
  -H "Authorization: Bearer $API_KEY"

echo -e "\n"
