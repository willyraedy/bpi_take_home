import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.environ['NEWS_API_KEY']
DIFF_BOT_API_KEY = os.environ['DIFF_BOT_KEY']

def fetch_articles_for_candidate(cand_name, sources):
    url = 'http://newsapi.org/v2/everything?' +\
            f'q={cand_name}' +\
            f'&apiKey={NEWS_API_KEY}' +\
            '&language=en' +\
            f'&sources={",".join(sources)}' +\
            '&sortBy=relevancy' +\
            '&pageSize=100'
    res = requests.get(url)
    articles = res.json()['articles']
    return [{**a, 'query': cand_name } for a in articles]

def format_article(raw_article):
    return {**raw_article, 'source': raw_article['source']['id']}

def get_source_list():
    source_url = f'http://newsapi.org/v2/sources?apiKey={NEWS_API_KEY}&category=general&country=us'
    res_sources = requests.get(source_url)
    return [x['id'] for x in res_sources.json()['sources']]

def fetch_for_candidates(cand_names):
    """
    Fetch articles from News API for given list of candidates. New API is limited
    to articles within one month of current day and only 100 results per
    request. Queries each candidate's name and retrieves up to 100 articles
    for each candidate.

    Args:
        cand_names (list): List of candidate names

    Returns:
        List of article objects.
    """
    sources = get_source_list()
    articles = []
    for cand_name in cand_names:
        new_articles = fetch_articles_for_candidate(cand_name, sources)
        articles += [format_article(a) for a in new_articles]
    return articles

def fetch_full_text(url):
    """
    Fetch full text of an article using DiffBot

    Args:
        url (str): URL of the article

    Returns:
        Full text record including the url, the full text, and any DiffBot tags
    """
    diff_resp = requests.get(f'https://api.diffbot.com/v3/article?url={url}&token={DIFF_BOT_API_KEY}')
    diff_bot_results = diff_resp.json()
    objects = diff_bot_results.get('objects')
    if objects and objects[0]:
        return {
        'url': url,
        'text': objects[0].get('text'),
        'tags': objects[0].get('tags')
        }
    return {
        'url': url,
        'text': '',
        'tags': []
        }

def fetch_articles_for_date(query, date, sources):
    url = 'http://newsapi.org/v2/everything?' +\
          f'q={query}' +\
          f'&apiKey={NEWS_API_KEY}' +\
          '&language=en' +\
          f'&sources={",".join(sources)}' +\
          '&sortBy=populatiry' +\
          '&pageSize=100' +\
          f'&from={date}&to={date}'
    res = requests.get(url)
    articles = res.json()['articles']
    return [{**a, 'query': query } for a in articles]

def fetch_for_range(query, start_date, end_date):
    """
    Fetch articles from News API for given date range. New API is limited
    to articles within one month of current day and only 100 results per
    request. Makes a daily request retreiving up to 100 articles for each day
    in range.

    Args:
        query (str): Query string to search for news articles
        start_date (str): Starting date of range
        end_date (str): End date of range

    Returns:
        List of article objects.
    """
    sources = get_source_list()
    articles = []
    end = pd.to_datetime(end_date)
    curr_date = pd.to_datetime(start_date)
    while curr_date < end:
        date_query = curr_date.strftime("%m/%d/%Y")
        new_articles = fetch_articles_for_date(query, date_query, sources)
        articles += [format_article(a) for a in new_articles]
        curr_date = curr_date + timedelta(days=1)
    return articles
