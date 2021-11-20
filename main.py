import requests
from bs4 import BeautifulSoup
from datetime import datetime

cnn_url = 'http://rss.cnn.com/rss/cnn_topstories.rss'
# kos_url = 'http://feeds.dailykosmedia.com/dailykosofficial'
guardian_url = 'https://www.theguardian.com/us/rss' #needs additional cleaning in get_descriptions
huffpo_url = 'https://chaski.huffpost.com/us/auto'
breitbart_url = 'https://feeds.feedburner.com/breitbart'
fox_url = 'http://feeds.foxnews.com/foxnews/latest'
federalist_url = 'https://thefederalist.com/feed/'
npr_url ='https://feeds.npr.org/1002/rss.xml'
rt_url = 'https://www.rt.com/rss/usa/'
cbc_url = 'https://www.cbc.ca/cmlink/rss-topstories'

def parse_article(url, website):
    website_content = {
        'cnn': {'tag': 'section', 'id': 'body-text' },
        'guardian': {'tag': 'div', 'id': 'maincontent'},
        'huffpo': {'tag': 'section', 'id': 'entry-body'},
        'breitbart': {'tag': 'div', 'class': 'entry-content'},
        'fox': {'tag': 'div', 'class':'article-body'},
        'federalist': {'tag': 'div', 'class': 'entry-content'},
        'npr': {'tag': 'div', 'id': 'storytext'},
        'rt': {'tag': 'div', 'class': 'article'},
        'cbc': {'tag': 'div', 'class': 'storyWrapper'}
    }
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    if 'id' in website_content[website]:
        article = soup.find(website_content[website]['tag'], id=website_content[website]['id'])
    else:
        article = soup.find(website_content[website]['tag'], class_=website_content[website]['class'])
    return article.get_text()

def parse_rss_feed(url):
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
        story_data['title'] = story.title.get_text(strip=True)
        story_data['url'] = story.guid.get_text(strip=True)
        story_data['date_collected'] = datetime.today().strftime('%Y-%m-%d')
        stories_data.append(story_data)
    
    return stories_data



# npr_data = parse_stories(npr_url)
# cnn_data = parse_stories(cnn_url)
# huffpo_data = parse_stories(huffpo_url)
# # kos_data = parse_stories(kos_url)
# breitbart_data = parse_stories(breitbart_url)
# fox_data = parse_stories(fox_url)
# federalist_data = parse_stories(federalist_url)
# guardian_data = parse_stories(guardian_url)
# rt_data = parse_stories(rt_url)
# cbc_data = parse_stories(cbc_url)

# url = 'https://www.cnn.com/2021/11/20/us/atlanta-airport-scare/index.html'
# print(parse_article(url, 'cnn'))

# url = 'https://www.huffpost.com/entry/charlottesville-survivors-activists-work-goes-on_n_6198024ee4b07fe2010ba3d7'
# print(parse_article(url, 'huffpo'))

# url = 'https://www.breitbart.com/asia/2021/11/20/lebron-on-enes-kanters-china-criticism-trying-use-my-name-create-opportunity-himself'
# print(parse_article(url, 'breitbart'))

# url = 'https://www.foxnews.com/sports/mississippi-state-will-rogers-dak-prescott-records'
# print(parse_article(url, 'fox'))

# url = 'https://thefederalist.com/2021/11/20/amid-criticisms-a-sex-crimes-registry-is-overly-harsh-colorado-rebrands-the-term-sex-offender/'
# print(parse_article(url, 'federalist'))

# url = 'https://www.npr.org/2021/11/20/1057661558/atlantas-airport-had-an-active-shooter-scare-as-millions-prepare-for-holiday-tra'
# print(parse_article(url, 'npr'))

# url = 'https://www.rt.com/usa/540856-kamala-harris-kyle-rittenhouse-verdict/'
# print(parse_article(url, 'rt'))

# url = 'https://www.cbc.ca/news/canada/british-columbia/b-c-bodies-recovered-mudslide-lillooet-1.6256924?cmp=rss'
# print(parse_article(url, 'cbc'))
