import whisper

model = whisper.load_model("base")

def transcribe_audio(filepath):
    try:
        result = model.transcribe(filepath)
        return result["text"]
    except Exception as e:
        return f"[Transcription Error] {e}"
