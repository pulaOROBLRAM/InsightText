import json
import subprocess
import sys
import re
from collections import Counter

# --- Auto-install missing dependencies ---
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


# --- Now you can safely import optional packages ---
# import nltk
# import textblob

import nltk
import textblob

# --- Input ---
text = input("Paste your text:\n")

# --- Preprocessing ---
words = re.findall(r'\b\w+\b', text.lower())
stopwords = {"the","a","an","and","or","of","to","in","with","is","it","where","by","for"}
words = [w for w in words if w not in stopwords]

# --- Frequency Analysis ---
freq = Counter(words)

# --- Chunk the text into ~20-word segments ---
segments = re.findall(r'(?:\S+\s+){1,20}', text)

# Score segments by sum of word frequencies
segment_scores = {seg: sum(freq.get(w.lower(),0) for w in re.findall(r'\b\w+\b', seg)) for seg in segments}

# Pick top 2 segments as summary
top_segments = sorted(segment_scores, key=segment_scores.get, reverse=True)[:2]
summary = " ".join(s.strip() for s in top_segments)

# --- Sentiment Analysis ---
positive_words = {"good","happy","great","love","excellent","awesome"}
negative_words = {"bad","sad","terrible","hate","awful","poor"}
pos_score = sum(1 for w in words if w in positive_words)
neg_score = sum(1 for w in words if w in negative_words)
if pos_score > neg_score:
    sentiment = "Positive 😊"
elif neg_score > pos_score:
    sentiment = "Negative 😟"
else:
    sentiment = "Neutral 😐"

# --- Top Keywords ---
top_keywords = [word for word, count in freq.most_common(5)]

# --- Display ---
print("\n📄 Summary:")
for seg in top_segments:
    print("- " + seg.strip())
print("\n💖 Sentiment:", sentiment)
print("\n🏷 Top Keywords:", ", ".join(top_keywords))
