# FFmpeg Video Renderer API

A FastAPI service that combines audio and image files into MP4 videos using FFmpeg.

## Features

- 🎵 Converts MP3 audio + JPG image → MP4 video
- ⚡ Fast processing with FFmpeg
- 🐳 Docker containerized
- 🚀 Ready for Render deployment
- 🔒 Health check endpoint

## API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "ok",
  "service": "ffmpeg-video-renderer"
}
```

### `POST /render`
Render video from audio and image

**Parameters:**
- `audio` (file): MP3 audio file
- `image` (file): JPG/PNG image file

**Response:** MP4 video file

## Local Development

### Prerequisites
- Python 3.11+
- FFmpeg installed

### Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Test
```bash
curl -X POST http://localhost:8000/render \
  -F "audio=@test.mp3" \
  -F "image=@cover.jpg" \
  -o output.mp4
```

## Docker

### Build
```bash
docker build -t ffmpeg-api .
```

### Run
```bash
docker run -p 8080:8080 ffmpeg-api
```

## Deploy to Render

1. Push this repo to GitHub
2. Connect to Render
3. Render will auto-deploy using `render.yaml`

## Environment Variables

- `PORT` (default: 8080) - Server port

## Tech Stack

- **FastAPI** - Modern Python web framework
- **FFmpeg** - Video processing
- **Docker** - Containerization
- **Render** - Cloud hosting