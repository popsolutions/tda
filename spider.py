import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pymongo

class Tweet:
    def __init__(self, username, text, date):
        self.username = username
        self.text = text
        self.date = date


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_scraper']
collection = db['tweets']

base_url = 'https://nitter.net/search?f=tweets&q='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}


def get_next_page(soup):
    next_path = soup.find_all('div', class_='show-more')[-1].find('a').get("href")
    next_url = urljoin(base_url, next_path)
    print(next_url)
    return next_url


def get_page_tweets(soup):
    tweets = soup.find_all(class_='timeline-item')
    parsed_tweets = []
    for tweet in tweets:
        try:
            tweet_content = tweet.find(class_='tweet-content').get_text()
            username = tweet.find(class_='username').get_text()
            tweet_date = tweet.find('span', class_='tweet-date').find('a').get("title")
            parsed_tweet = {
                'username': username,
                'date': tweet_date,
                'text': tweet_content
            }
            collection.insert_one(parsed_tweet)
            parsed_tweets.append(parsed_tweet)
        except:
            pass
    return parsed_tweets


def scrape_pages(search_text, num_pages=1):
    parsed_tweets = []
    url = base_url + search_text
    print(url)
    current_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(current_page.text, 'html.parser')
    parsed_tweets.extend(get_page_tweets(soup))

    for i in range(1, num_pages):
        next_url = get_next_page(soup)
        current_page = requests.get(next_url, headers=headers)
        soup = BeautifulSoup(current_page.text, 'html.parser')
        parsed_tweets.extend(get_page_tweets(soup))

    return parsed_tweets


# Example:
# scrape_pages('OSE_Uruguay', 10)
