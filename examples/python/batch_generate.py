"""Batch generation: submit multiple tasks and collect results."""

import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from seedance import Seedance

API_KEY = os.environ.get("SEEDANCE_API_KEY", "YOUR_API_KEY")
client = Seedance(api_key=API_KEY)

prompts = [
    "A golden retriever running through a sunflower field, slow motion, golden hour",
    "Ocean waves crashing on rocky cliffs, aerial drone shot, dramatic sky",
    "A steaming cup of coffee on a rainy windowsill, cozy atmosphere, macro lens",
]

task_ids = []
for prompt in prompts:
    data = client.create_task(prompt=prompt, model="seedance_2.0_fast", duration=5)
    task_ids.append(data["task_id"])
    print(f"Submitted task {data['task_id']}: {prompt[:50]}...")

print(f"\n{len(task_ids)} tasks submitted. Waiting for results...\n")

results = {}
while task_ids:
    remaining = []
    for tid in task_ids:
        task = client.get_task(tid)
        if task["status"] == "completed":
            results[tid] = task["result"]
            print(f"Task {tid} completed: {task['result']['video_url']}")
        elif task["status"] == "failed":
            print(f"Task {tid} failed: {(task.get('result') or {}).get('error', 'Unknown')}")
        else:
            remaining.append(tid)
    task_ids = remaining
    if task_ids:
        time.sleep(5)

print(f"\nDone. {len(results)}/{len(prompts)} videos generated.")
