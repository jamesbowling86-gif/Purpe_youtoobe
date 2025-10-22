from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "ffmpeg-video-renderer"}

@app.post("/render")
async def render(audio: UploadFile = File(...), image: UploadFile = File(...)):
    """Render video from audio and image files"""
    base = f"/tmp/{uuid.uuid4()}"
    audio_path = base + "_audio.mp3"
    image_path = base + "_image.jpg"
    output_path = base + "_out.mp4"

    # Write uploaded files to disk
    with open(audio_path, "wb") as a:
        a.write(await audio.read())
    with open(image_path, "wb") as i:
        i.write(await image.read())

    # Run ffmpeg to create video
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-pix_fmt", "yuv420p", output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # Clean up files on error
        for path in [audio_path, image_path, output_path]:
            if os.path.exists(path):
                os.remove(path)
        raise Exception(f"FFmpeg failed: {e.stderr}")
    
    # Clean up input files (output will be cleaned by FastAPI after response)
    os.remove(audio_path)
    os.remove(image_path)

    return FileResponse(
        output_path, 
        media_type="video/mp4", 
        filename="output.mp4",
        headers={"X-Content-Type-Options": "nosniff"}
    )