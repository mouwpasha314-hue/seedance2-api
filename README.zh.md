# Seedance 2.0 API

[English](README.md)

基于 [字节跳动 Seedance 2.0](https://seed2.io) 的 AI 视频生成 API —— 支持文字、图片、音频和视频参考生成视频。

## 功能特性

- **文生视频** — 描述一个场景，生成视频
- **图生视频** — 将静态图片变成动态视频
- **视频参考** — 从参考视频中迁移动作和编排
- **音频同步** — 让视频与背景音乐或配音同步
- **图片 + 音频** — 让肖像照片根据语音进行口型同步
- 输出时长 **4–15 秒**，最高 1080p
- 两个模型档位：`seedance_2.0_fast`（快速版）和 `seedance_2.0`（高质量版）

## 快速开始

### 1. 获取 API Key

在 [seed2.io](https://seed2.io) 注册账号，从 [账户页](https://seed2.io/account) 复制你的 API Key。新用户赠送 **10,000 积分**（约 $1）。

### 2. 生成视频

**cURL：**

```bash
curl -X POST https://api.seed2.io/v1/video/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只猫在爵士酒吧弹钢琴，电影感光线",
    "model": "seedance_2.0_fast",
    "duration": 5,
    "ratio": "16:9"
  }'
```

**Python（使用 SDK）：**

```python
from seedance import Seedance

client = Seedance(api_key="sk-s2-xxxx")
result = client.generate(
    prompt="一只猫在爵士酒吧弹钢琴，电影感光线",
    model="seedance_2.0_fast",
    duration=5,
)
print(result["video_url"])
```

**Node.js：**

```javascript
const res = await fetch("https://api.seed2.io/v1/video/generate", {
  method: "POST",
  headers: {
    Authorization: "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    prompt: "一只猫在爵士酒吧弹钢琴，电影感光线",
    model: "seedance_2.0_fast",
    duration: 5,
    ratio: "16:9",
  }),
});
const { data } = await res.json();
console.log("任务 ID:", data.task_id);
```

### 3. 轮询获取结果

```bash
curl https://api.seed2.io/v1/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

完成时的响应：

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

## API 参考

### 认证

所有请求需要在 `Authorization` 头中携带 API Key：

```
Authorization: Bearer sk-s2-xxxxxxxxxxxx
```

### 创建视频任务

```
POST /v1/video/generate
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | 是 | 文字描述。使用 `@image_file_1` 引用上传的图片。 |
| `model` | string | 否 | `seedance_2.0_fast`（默认）或 `seedance_2.0` |
| `duration` | int | 否 | 4–15 秒，默认 5 |
| `ratio` | string | 否 | `16:9`、`9:16`、`1:1`、`4:3`、`3:4`、`21:9`，默认 `16:9` |
| `image_files` | string[] | 否 | 图片 URL 列表（最多 9 个），在 prompt 中用 `@image_file_1`、`@image_file_2` 引用 |
| `video_files` | string[] | 否 | 参考视频 URL（最多 3 个，总时长 ≤ 15 秒） |
| `audio_files` | string[] | 否 | 音频 URL（最多 3 个） |

**响应：**

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

### 查询任务

```
GET /v1/tasks/:task_id
```

**状态流转：** `pending` → `processing` → `completed` / `failed`

任务失败时，积分会自动退还。

## 使用模式

### 文生视频

最简单的模式 —— 只需提供文字描述。

```python
result = client.generate(prompt="富士山日出，延时摄影，4K")
```

### 图生视频

将静态图片变成动态视频。在 prompt 中使用 `@image_file_N` 引用图片。

```python
result = client.generate(
    prompt="@image_file_1 中的女人走过花园，花瓣飘落",
    image_files=["https://example.com/woman.jpg"],
)
```

### 视频参考

使用参考视频来迁移动作、风格或编排。

```python
result = client.generate(
    prompt="一个卡通角色表演同样的舞蹈",
    model="seedance_2.0",
    duration=10,
    video_files=["https://example.com/dance.mp4"],
)
```

### 音频同步

让生成的视频与背景音乐或音效同步。

```python
result = client.generate(
    prompt="一个 DJ 在夜店打碟，热情的人群",
    duration=10,
    audio_files=["https://example.com/edm-track.mp3"],
)
```

### 图片 + 音频（口型同步）

将肖像图片与语音音频结合，实现逼真的口型同步。

```python
result = client.generate(
    prompt="@image_file_1 中的人正在自信地进行 TED 演讲",
    model="seedance_2.0",
    duration=8,
    ratio="9:16",
    image_files=["https://example.com/speaker.jpg"],
    audio_files=["https://example.com/speech.mp3"],
)
```

## 定价

| 模型 | 不含视频/音频 | 含视频/音频 |
|------|:----------:|:---------:|
| `seedance_2.0_fast` | 580 积分/秒 | 1,160 积分/秒 |
| `seedance_2.0` | 1,160 积分/秒 | 2,320 积分/秒 |

- **1 美元 = 10,000 积分**
- 新用户赠送 **10,000 积分**
- 充值入口：[seed2.io/recharge](https://seed2.io/recharge)

**费用示例：** 使用 `seedance_2.0_fast` 生成 5 秒文生视频，花费 2,900 积分（$0.29）。

## 示例代码

查看 [`examples/`](examples/) 目录获取可直接运行的脚本：

| 文件 | 语言 | 说明 |
|------|------|------|
| [`examples/python/text_to_video.py`](examples/python/text_to_video.py) | Python | 文生视频 |
| [`examples/python/image_to_video.py`](examples/python/image_to_video.py) | Python | 图生视频 |
| [`examples/python/video_reference.py`](examples/python/video_reference.py) | Python | 视频参考 |
| [`examples/python/image_audio_lipsync.py`](examples/python/image_audio_lipsync.py) | Python | 图片+音频口型同步 |
| [`examples/python/batch_generate.py`](examples/python/batch_generate.py) | Python | 批量生成 |
| [`examples/javascript/text_to_video.mjs`](examples/javascript/text_to_video.mjs) | Node.js | 文生视频 |
| [`examples/javascript/image_to_video.mjs`](examples/javascript/image_to_video.mjs) | Node.js | 图生视频 |
| [`examples/curl/examples.sh`](examples/curl/examples.sh) | cURL | 全部模式 |

运行 Python 示例：

```bash
export SEEDANCE_API_KEY="sk-s2-xxxx"
python examples/python/text_to_video.py
```

## Python SDK

本仓库在 [`seedance/`](seedance/) 目录中包含一个轻量级 Python 客户端：

```python
from seedance import Seedance

client = Seedance(api_key="sk-s2-xxxx")

# 一行代码：创建 → 轮询 → 返回结果
result = client.generate(prompt="一只猫在弹钢琴")
print(result["video_url"])

# 或者手动管理任务
data = client.create_task(prompt="一只猫在弹钢琴")
task = client.wait_for_task(data["task_id"])
print(task["result"]["video_url"])
```

**依赖：** Python 3.7+，需要安装 `requests`（`pip install requests`）。

## 相关链接

- **Web 应用：** [seed2.io](https://seed2.io)
- **API 文档：** [seed2.io/api-docs](https://seed2.io/api-docs)
- **视频广场：** [seed2.io/plaza](https://seed2.io/plaza)

## 许可证

[MIT](LICENSE)
