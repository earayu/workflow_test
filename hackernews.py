import requests
from bs4 import BeautifulSoup
import schedule
import time
import openai
import os
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_hackernews():
    logging.info("Fetching Hacker News articles...")
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    top_stories = soup.select(".titleline > a")

    article_titles = [story.text for story in top_stories[:5]]
    return article_titles

def summarize_text(text):
    logging.info("Summarizing article content...")
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Please summarize the following text: {text}",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def translate_to_chinese(text):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Translate the following English text to Chinese: {text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def process_article(title):
    summary = summarize_text(title)
    chinese_summary = translate_to_chinese(summary)
    return chinese_summary

def main():
    hackernews_titles = get_hackernews()

    with ThreadPoolExecutor() as executor:
        chinese_summaries = list(executor.map(process_article, hackernews_titles))

    logging.info(f"Chinese summaries: {chinese_summaries}")

if __name__ == "__main__":
    main()
