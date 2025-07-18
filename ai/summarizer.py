from transformers import pipeline

# Load summarizer (you can cache this)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    if len(text) < 50:
        return "Text too short to summarize."
    try:
        summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"[Summarization Error] {e}"
