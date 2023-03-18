import requests
from bs4 import BeautifulSoup
import schedule
import time
import openai
import os
import logging

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

    article_contents = []
    for story in top_stories[:5]:
        article_url = story["href"]
        logging.info(f"Fetching article content from {article_url}")
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        article_content = article_soup.get_text()
        article_contents.append(article_content)

    return article_contents

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
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def split_text(text, max_tokens):
    tokens = text.split()
    return [" ".join(tokens[i:i+max_tokens]) for i in range(0, len(tokens), max_tokens)]

def process_article(article):
    logging.info("Processing article...")
    article_chunks = split_text(article, max_tokens=1000)
    chunk_summaries = [summarize_text(chunk) for chunk in article_chunks]
    combined_summary = " ".join(translate_to_chinese(chunk_summaries))
    return combined_summary

def main():
    hackernews_articles = get_hackernews()
    summaries = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_article, article) for article in hackernews_articles]
        for future in concurrent.futures.as_completed(futures):
            summaries.append(future.result())

    logging.info(f"Summaries: {summaries}")

if __name__ == "__main__":
    main()
