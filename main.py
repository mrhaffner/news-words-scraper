import requests
from bs4 import BeautifulSoup
from datetime import datetime

cnn_url = 'http://rss.cnn.com/rss/cnn_topstories.rss'
# kos_url = 'http://feeds.dailykosmedia.com/dailykosofficial'
guardian_url = 'https://www.theguardian.com/us/rss'
huffpo_url = 'https://chaski.huffpost.com/us/auto'
breitbart_url = 'https://feeds.feedburner.com/breitbart'
fox_url = 'http://feeds.foxnews.com/foxnews/latest'
federalist_url = 'https://thefederalist.com/feed/'

def get_description(story):
    dirty_desciption = story.description.get_text()

    if dirty_desciption[:3] == '<p>':
        return dirty_desciption
    else:
        return dirty_desciption.split('<')[0]

def parse_stories(url):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    stories = soup.find_all('item')

    stories_data = []

    for story in stories:
        story_data = {}
        story_data['title'] = story.title.get_text()
        story_data['url'] = story.guid.get_text()
        story_data['description'] = get_description(story)
        story_data['date_collected'] = datetime.today().strftime('%Y-%m-%d')
        stories_data.append(story_data)
    
    return stories_data




# cnn_data = parse_stories(cnn_url)
# huffpo_data = parse_stories(huffpo_url)
# # kos_data = parse_stories(kos_url)
# breitbart_data = parse_stories(breitbart_url)
# fox_data = parse_stories(fox_url)
# federalist_data = parse_stories(federalist_url)
# guardian_data = parse_stories(guardian_url)