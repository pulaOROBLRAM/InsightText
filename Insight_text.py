import json
import subprocess
import sys
import re
from collections import Counter

try:
    with open("requirements.json") as f:
        deps = json.load(f).get("dependencies", [])
        for pkg in deps:
            try:
                __import__(pkg)  # Try importing the package
            except ImportError:
                print(f"Installing missing package: {pkg} ...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
except FileNotFoundError:
    print("requirements.json not found. Skipping auto-install.")

from transformers import pipeline
import re
from collections import Counter

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

sentiment_analyzer = pipeline("sentiment-analysis")

text = input("Paste your text:\n")

try:
    summary_result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    ai_summary = summary_result[0]['summary_text']
except Exception as e:
    ai_summary = "⚠️ Summary failed: " + str(e)

try:
    sentiment = sentiment_analyzer(text)[0]
    sentiment_label = sentiment['label']
    sentiment_score = sentiment['score']
except Exception as e:
    sentiment_label = "Unknown"
    sentiment_score = 0

words = re.findall(r'\b\w+\b', text.lower())
stopwords = {"the","a","an","and","or","of","to","in","with","is","it","where","by","for"}
words = [w for w in words if w not in stopwords]
freq = Counter(words)
top_keywords = [w for w,_ in freq.most_common(5)]

print("\n📄 AI Summary:")
print(ai_summary)

print("\n💖 Sentiment:", sentiment_label, f"(score: {sentiment_score:.2f})")

print("\n🏷 Top Keywords:", ", ".join(top_keywords))

