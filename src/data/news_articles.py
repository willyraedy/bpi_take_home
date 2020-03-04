import requests
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
    sources = get_source_list()
    articles = []
    for cand_name in cand_names:
        new_articles = fetch_articles_for_candidate(cand_name, sources)
        articles += [format_article(a) for a in new_articles]
    return articles

def fetch_full_text(url):
  diff_test_resp = requests.get(f'https://api.diffbot.com/v3/article?url={url}&token={DIFF_BOT_API_KEY}')
  print(diff_test_resp.status_code)
  diff_bot_results = diff_test_resp.json()
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
