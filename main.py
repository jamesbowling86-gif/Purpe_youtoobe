from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()

@app.post("/render")
async def render(audio: UploadFile = File(...), image: UploadFile = File(...)):
    base = f"/tmp/{uuid.uuid4()}"
    audio_path = base + "_audio.mp3"
    image_path = base + "_image.jpg"
    output_path = base + "_out.mp4"

    with open(audio_path, "wb") as a:
        a.write(await audio.read())
    with open(image_path, "wb") as i:
        i.write(await image.read())

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-pix_fmt", "yuv420p", output_path
    ]
    subprocess.run(cmd, check=True)

    return FileResponse(output_path, media_type="video/mp4", filename="output.mp4")
