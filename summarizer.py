# summarizer.py
from transformers import pipeline

# Force to use PyTorch by setting framework="pt"
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    framework="pt"  # Force PyTorch only
)

def summarize_text(text, max_length=120, min_length=30):
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error summarizing: {e}")
        return text


print("Summarizing today's translated content...")