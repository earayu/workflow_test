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
    titles = soup.select(".titleline > a")
    return [title.text for title in titles]


def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following text: {text}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def translate_to_chinese(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please translate the following text to Chinese: {text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def main():
    hackernews_titles = get_hackernews()
    summaries = [summarize_text(title) for title in hackernews_titles]
    chinese_summaries = [translate_to_chinese(summary) for summary in summaries]
    print(chinese_summaries)
    # Do something with the chinese_summaries, e.g., save to a file or send an email


main()

# schedule.every().day.at("00:00").do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(60)