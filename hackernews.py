import requests
from bs4 import BeautifulSoup
import schedule
import time
import openai
import os

# Initialize OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_hackernews():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    top_stories = soup.select(".titleline > a")

    article_contents = []
    for story in top_stories[:5]:
        article_url = story["href"]
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        article_content = article_soup.get_text()
        article_contents.append(article_content)

    return article_contents

def summarize_text(text):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Please summarize the following text: {text}",
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def split_text(text, max_tokens):
    tokens = text.split()
    return [" ".join(tokens[i:i+max_tokens]) for i in range(0, len(tokens), max_tokens)]

def main():
    hackernews_articles = get_hackernews()
    summaries = []
    for article in hackernews_articles:
        article_chunks = split_text(article, max_tokens=2000)
        chunk_summaries = [summarize_text(chunk) for chunk in article_chunks]
        combined_summary = " ".join(chunk_summaries)
        summaries.append(combined_summary)

    logging.info(f"Summaries: {summaries}")

if __name__ == "__main__":
    main()
