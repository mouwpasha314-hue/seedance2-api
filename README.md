# Seedance 2.0 API

[中文文档](README.zh.md)

Generate AI videos from text, images, audio, and video references — powered by [ByteDance Seedance 2.0](https://seed2.io).

## Features

- **Text to Video** — describe a scene, get a video
- **Image to Video** — animate any still image
- **Video Reference** — transfer motion/choreography from a reference video
- **Audio Sync** — synchronize video to music or voiceover
- **Image + Audio** — lip-sync a portrait with speech audio
- **4–15 seconds** output duration, up to 1080p
- Two model tiers: `seedance_2.0_fast` (budget) and `seedance_2.0` (premium)

## Quick Start

### 1. Get Your API Key

Sign up at [seed2.io](https://seed2.io) and copy your API key from the [Account](https://seed2.io/account) page. New users get **10,000 free credits** (≈ $1).

### 2. Generate a Video

**cURL:**

```bash
curl -X POST https://api.seed2.io/v1/video/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat playing piano in a jazz bar, cinematic lighting",
    "model": "seedance_2.0_fast",
    "duration": 5,
    "ratio": "16:9"
  }'
```

**Python (with SDK):**

```python
from seedance import Seedance

client = Seedance(api_key="sk-s2-xxxx")
result = client.generate(
    prompt="A cat playing piano in a jazz bar, cinematic lighting",
    model="seedance_2.0_fast",
    duration=5,
)
print(result["video_url"])
```

**Node.js:**

```javascript
const res = await fetch("https://api.seed2.io/v1/video/generate", {
  method: "POST",
  headers: {
    Authorization: "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    prompt: "A cat playing piano in a jazz bar, cinematic lighting",
    model: "seedance_2.0_fast",
    duration: 5,
    ratio: "16:9",
  }),
});
const { data } = await res.json();
console.log("Task ID:", data.task_id);
```

### 3. Poll for Result

```bash
curl https://api.seed2.io/v1/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Response when completed:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": 123,
    "status": "completed",
    "result": {
      "video_url": "https://cdn.seed2.io/videos/xxx.mp4",
      "duration": 5
    },
    "points_cost": 2900
  }
}
```

## API Reference

### Authentication

All requests require an API key in the `Authorization` header:

```
Authorization: Bearer sk-s2-xxxxxxxxxxxx
```

### Create Video Task

```
POST /v1/video/generate
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text description. Use `@image_file_1` to reference uploaded images. |
| `model` | string | No | `seedance_2.0_fast` (default) or `seedance_2.0` |
| `duration` | int | No | 4–15 seconds. Default: 5 |
| `ratio` | string | No | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`. Default: `16:9` |
| `image_files` | string[] | No | Image URLs (max 9). Reference in prompt as `@image_file_1`, `@image_file_2`, etc. |
| `video_files` | string[] | No | Reference video URLs (max 3, total ≤ 15s) |
| `audio_files` | string[] | No | Audio URLs (max 3) |

**Response:**

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "task_id": 456,
    "status": "pending",
    "points_cost": 2900,
    "balance": 7100
  }
}
```

### Query Task

```
GET /v1/tasks/:task_id
```

**Status values:** `pending` → `processing` → `completed` / `failed`

If a task fails, credits are automatically refunded.

## Usage Modes

### Text to Video

The simplest mode — just provide a prompt.

```python
result = client.generate(prompt="Sunrise over Mount Fuji, timelapse, 4K")
```

### Image to Video

Animate a still image. Reference images in the prompt with `@image_file_N`.

```python
result = client.generate(
    prompt="The woman in @image_file_1 walks through a garden, petals falling",
    image_files=["https://example.com/woman.jpg"],
)
```

### Video Reference

Use a reference video to transfer motion, style, or choreography.

```python
result = client.generate(
    prompt="A cartoon character performing the same dance",
    model="seedance_2.0",
    duration=10,
    video_files=["https://example.com/dance.mp4"],
)
```

### Audio Sync

Synchronize the generated video with background music or sound effects.

```python
result = client.generate(
    prompt="A DJ mixing at a nightclub, energetic crowd",
    duration=10,
    audio_files=["https://example.com/edm-track.mp3"],
)
```

### Image + Audio (Lip-sync)

Combine a portrait with speech audio for realistic lip-sync.

```python
result = client.generate(
    prompt="The person in @image_file_1 is giving a TED talk with confident gestures",
    model="seedance_2.0",
    duration=8,
    ratio="9:16",
    image_files=["https://example.com/speaker.jpg"],
    audio_files=["https://example.com/speech.mp3"],
)
```

## Pricing

| Model | Without Video/Audio | With Video/Audio |
|-------|:-------------------:|:----------------:|
| `seedance_2.0_fast` | 580 credits/sec | 1,160 credits/sec |
| `seedance_2.0` | 1,160 credits/sec | 2,320 credits/sec |

- **1 USD = 10,000 credits**
- New users: **10,000 free credits**
- Recharge at [seed2.io/recharge](https://seed2.io/recharge)

**Example cost:** A 5-second text-to-video with `seedance_2.0_fast` costs 2,900 credits ($0.29).

## Examples

Check the [`examples/`](examples/) directory for ready-to-run scripts:

| File | Language | Description |
|------|----------|-------------|
| [`examples/python/text_to_video.py`](examples/python/text_to_video.py) | Python | Text to Video |
| [`examples/python/image_to_video.py`](examples/python/image_to_video.py) | Python | Image to Video |
| [`examples/python/video_reference.py`](examples/python/video_reference.py) | Python | Video Reference |
| [`examples/python/image_audio_lipsync.py`](examples/python/image_audio_lipsync.py) | Python | Image + Audio Lip-sync |
| [`examples/python/batch_generate.py`](examples/python/batch_generate.py) | Python | Batch Generation |
| [`examples/javascript/text_to_video.mjs`](examples/javascript/text_to_video.mjs) | Node.js | Text to Video |
| [`examples/javascript/image_to_video.mjs`](examples/javascript/image_to_video.mjs) | Node.js | Image to Video |
| [`examples/curl/examples.sh`](examples/curl/examples.sh) | cURL | All modes |

Run any Python example:

```bash
export SEEDANCE_API_KEY="sk-s2-xxxx"
python examples/python/text_to_video.py
```

## Python SDK

This repo includes a lightweight Python client in [`seedance/`](seedance/):

```python
from seedance import Seedance

client = Seedance(api_key="sk-s2-xxxx")

# One-liner: create → poll → return result
result = client.generate(prompt="A cat playing piano")
print(result["video_url"])

# Or manage tasks manually
data = client.create_task(prompt="A cat playing piano")
task = client.wait_for_task(data["task_id"])
print(task["result"]["video_url"])
```

**Requirements:** Python 3.7+ with `requests` installed (`pip install requests`).

## Links

- **Web App:** [seed2.io](https://seed2.io)
- **API Docs:** [seed2.io/api-docs](https://seed2.io/api-docs)
- **Video Gallery:** [seed2.io/plaza](https://seed2.io/plaza)

## License

[MIT](LICENSE)
