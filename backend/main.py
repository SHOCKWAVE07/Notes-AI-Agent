from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper 
from backend.agent import interpret
import os
import tempfile

app = FastAPI()
model = whisper.load_model("base")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/voice-command")
async def voice_cmd(file: UploadFile):
    ext = os.path.splitext(file.filename)[1] or ".wav"
    tp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    tp.write(await file.read())
    tp.flush()
    txt = model.transcribe(tp.name)["text"]
    return interpret(txt)

@app.post("/text-command")
async def text_cmd(msg: str):
    return interpret(msg)

@app.get("/notes")
def get_all():
    from notes_manager import read_notes
    return read_notes()
