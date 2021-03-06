import requests
import dateparser
from bs4 import BeautifulSoup


def parse_topics_list():
    """
    Парсит список тем
    :return: список распарсенный тем
    """
    data = BeautifulSoup(requests.get('https://www.rbc.ru/story/').text, 'lxml')
    topic_list = data.find_all('div', {'class': 'item item_story js-story-item'})
    result = []

    for topic in topic_list:
        url = topic.find('a', {'class': 'item__link no-injects'})['href'].strip()
        title = topic.find('span', {'class': 'item__title'}).text.strip()
        description = topic.find('span', {'class': 'item__text'}).text.strip()
        result.append({'url': url, 'title': title, 'description': description})

    return result


def parse_topic(address):
    """
    Парсит статьи в теме
    :param address: адрес темы
    :return: список распарсенных статей
    """
    data = BeautifulSoup(requests.get(address).text, 'lxml')
    article_list = data.find_all('div',
                                 {'class': 'item item_story-single js-story-item'})
    result = []

    for article in article_list:
        url = article.find('a', {'class': 'item__link no-injects js-yandex-counter'})['href'].strip()
        title = article.find('span', {'class': 'item__title'}).text.strip()
        time_str = article.find('span', {'class': 'item__info'}).text.strip()
        time = dateparser.parse(time_str)
        result.append({'url': url, 'title': title, 'time': time})

    return result


def parse_article(address):
    """
    Парсит текст статьи и тэги статьи
    :param address: адрес статьи
    :return: текст статьи и список её тэгов
    """
    data = BeautifulSoup(requests.get(address).text, 'lxml')
    result = {'text': '', 'tags': []}

    paragraphs = data.find_all('p')
    for p in paragraphs:
        result['text'] += p.text.strip() + "\n"

    tags_lives_here = data.find('div', {'class': 'article__tags'})
    if tags_lives_here is not None:
        tags = tags_lives_here.find_all('a', {'class': 'article__tags__link'})
        for tag in tags:
            result['tags'].append(tag.text.strip())

    return result
