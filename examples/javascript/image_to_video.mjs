/**
 * Image-to-Video: animate a still image into a video using Node.js.
 *
 * Usage:
 *   SEEDANCE_API_KEY=sk-s2-xxx node image_to_video.mjs
 */

const API_KEY = process.env.SEEDANCE_API_KEY || "YOUR_API_KEY";
const BASE_URL = "https://api.seed2.io";

async function createTask(payload) {
  const res = await fetch(`${BASE_URL}/v1/video/generate`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const body = await res.json();
  if (body.code !== 0) throw new Error(body.message);
  return body.data;
}

async function getTask(taskId) {
  const res = await fetch(`${BASE_URL}/v1/tasks/${taskId}`, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });
  const body = await res.json();
  if (body.code !== 0) throw new Error(body.message);
  return body.data;
}

async function waitForTask(taskId, interval = 3000, timeout = 600000) {
  const start = Date.now();
  while (true) {
    const task = await getTask(taskId);
    if (task.status === "completed") return task;
    if (task.status === "failed") {
      throw new Error(task.result?.error || "Task failed");
    }
    if (Date.now() - start > timeout) {
      throw new Error(`Timeout after ${timeout / 1000}s`);
    }
    await new Promise((r) => setTimeout(r, interval));
  }
}

// --- Main ---
const data = await createTask({
  prompt: "The girl in @image_file_1 smiles and turns around slowly, hair flowing in the wind",
  model: "seedance_2.0_fast",
  duration: 5,
  ratio: "16:9",
  image_files: ["https://example.com/girl-portrait.jpg"], // Replace with your image URL
});

console.log(`Task ${data.task_id} created. Waiting...`);

const task = await waitForTask(data.task_id);
console.log(`Video URL: ${task.result.video_url}`);
