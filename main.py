import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'http://rss.cnn.com/rss/cnn_topstories.rss'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

stories = soup.find_all('item')

stories_data = []

for story in stories:
    story_data = {}
    story_data['title'] = story.title.get_text()
    story_data['url'] = story.guid.get_text()
    dirty_desciption = story.description.get_text()
    description = dirty_desciption.split('<')[0]
    story_data['description'] = description
    story_data['date_collected'] = datetime.today().strftime('%Y-%m-%d')
    stories_data.append(story_data)


print(stories_data)