# app.py
import streamlit as st
import newspaper
from newspaper import Article
from transformers import pipeline
from langdetect import detect
from datetime import datetime
import torch

# Force models to CPU
device = torch.device("cpu")

# Load Hugging Face translation and summarization models
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", framework="pt", device=-1)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt", device=-1)

# Scrape from major news websites
def scrape_news_from_sites(query, max_articles_per_site=5):
    news_sites = [
        "https://www.bbc.com/news",
        "https://www.reuters.com/news/world",
        "https://www.aljazeera.com/news/",
        "https://www.channelnewsasia.com/world",
        "https://www.nhk.or.jp/nhkworld/en/news/"
    ]
    
    matching_articles = []
    
    for site_url in news_sites:
        try:
            paper = newspaper.build(site_url, memoize_articles=False)
            count = 0
            for content in paper.articles:
                if count >= max_articles_per_site:
                    break
                content.download()
                content.parse()
                if query.lower() in content.text.lower():
                    matching_articles.append(content.text)
                    count += 1
        except Exception as e:
            print(f"Error scraping {site_url}: {e}")
    
    return matching_articles

# Language detection
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Translation
def translate_text(text, detected_language):
    if detected_language.lower() in ["en", "english"]:
        return text
    try:
        translation = translator(text)[0]['translation_text']
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return text

# Summarization
def summarize_text(text, max_length=120, min_length=30):
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Summarization error: {e}")
        return text

# Streamlit UI
st.set_page_config(page_title="🌍 Global News Summarizer", layout="wide")
st.title("🌍 Global News Summarizer")

query = st.text_input("Enter any keyword (in any language):", "")

if st.button("Search and Summarize"):
    if query.strip() == "":
        st.warning("Please enter a keyword to search.")
    else:
        with st.spinner('Scraping and processing news...'):
            articles = scrape_news_from_sites(query)

            if not articles:
                st.error("No articles found. Try a different keyword.")
            else:
                st.success(f"Found {len(articles)} articles! Translating and summarizing...")

                for idx, article_text in enumerate(articles, 1):
                    detected_lang = detect_language(article_text)
                    translated_text = translate_text(article_text, detected_lang)
                    summary = summarize_text(translated_text)

                    st.subheader(f"Summary {idx}")
                    st.write(summary)

        st.success("✅ Done!")
