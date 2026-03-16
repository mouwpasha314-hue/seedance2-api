"""Lightweight Python client for the Seedance 2.0 API (seed2.io)."""

import time
import requests

DEFAULT_BASE_URL = "https://api.seed2.io"
DEFAULT_POLL_INTERVAL = 3
DEFAULT_TIMEOUT = 600


class SeedanceError(Exception):
    def __init__(self, message, code=None, data=None):
        super().__init__(message)
        self.code = code
        self.data = data


class Seedance:
    """
    Seedance 2.0 API client.

    Usage::

        from seedance import Seedance

        client = Seedance(api_key="sk-s2-xxxx")
        result = client.generate(prompt="A cat playing piano in a jazz bar")
        print(result["video_url"])
    """

    def __init__(self, api_key, base_url=None, timeout=DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def create_task(self, prompt, model="seedance_2.0_fast", duration=5,
                    ratio="16:9", image_files=None, video_files=None,
                    audio_files=None, **kwargs):
        """Submit a video generation task. Returns the raw API response data."""
        payload = {"prompt": prompt, "model": model, "duration": duration, "ratio": ratio}
        if image_files:
            payload["image_files"] = image_files
        if video_files:
            payload["video_files"] = video_files
        if audio_files:
            payload["audio_files"] = audio_files
        payload.update(kwargs)

        resp = self._session.post(f"{self.base_url}/v1/video/generate", json=payload)
        body = resp.json()
        if body.get("code") != 0:
            raise SeedanceError(body.get("message", "Unknown error"), body.get("code"), body)
        return body["data"]

    def get_task(self, task_id):
        """Query a task by ID. Returns the task data dict."""
        resp = self._session.get(f"{self.base_url}/v1/tasks/{task_id}")
        body = resp.json()
        if body.get("code") != 0:
            raise SeedanceError(body.get("message", "Unknown error"), body.get("code"), body)
        return body["data"]

    def wait_for_task(self, task_id, poll_interval=DEFAULT_POLL_INTERVAL, timeout=None):
        """Poll until the task reaches a terminal state (completed / failed)."""
        timeout = timeout or self.timeout
        start = time.time()
        while True:
            task = self.get_task(task_id)
            if task["status"] == "completed":
                return task
            if task["status"] == "failed":
                err = (task.get("result") or {}).get("error", "Task failed")
                raise SeedanceError(err, data=task)
            if time.time() - start > timeout:
                raise SeedanceError(f"Timeout after {timeout}s, status: {task['status']}")
            time.sleep(poll_interval)

    def generate(self, prompt, model="seedance_2.0_fast", duration=5,
                 ratio="16:9", image_files=None, video_files=None,
                 audio_files=None, poll_interval=DEFAULT_POLL_INTERVAL,
                 timeout=None, **kwargs):
        """
        All-in-one: create a task, wait for completion, and return the result.

        Returns a dict with ``video_url``, ``duration``, etc.
        """
        data = self.create_task(
            prompt=prompt, model=model, duration=duration, ratio=ratio,
            image_files=image_files, video_files=video_files,
            audio_files=audio_files, **kwargs,
        )
        task = self.wait_for_task(data["task_id"], poll_interval, timeout)
        return task.get("result", task)
