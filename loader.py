import parser
import os
import dateparser
import statistic
from my_database import TableTag, TableArticle, TableTopic


def load_new(default_time):
    try:
        file = open('last_update_db', 'r')
        time = dateparser.parse(file.read())
        file.close()
    except FileNotFoundError:
        time = default_time

    load(time)

    file = open('last_update_db', 'w')
    file.write(str(dateparser.parse('today')))
    file.close()


def load(time):
    topics = parser.parse_topics_list()
    for t in topics:
        articles = parser.parse_topic(t['url'])
        if articles[0]['time'] < time:
            break

        print('TOPIC:', t['title'])
        try:
            topic = statistic.find_topic(t['title'])
        except:
            topic = TableTopic.create(title=t['title'],
                                    url=t['url'],
                                    description=t['description'],
                                    last_update=articles[0]['time'])

        for a in articles:
            if (a['time'] < time):
                break

            art = parser.parse_article(a['url'])
            print('article:', a['title'])
            article = TableArticle.create(topic=topic,
                                          title=a['title'],
                                          url=a['url'],
                                          text=art['text'],
                                          last_update=a['time'])

            for tag in art['tags']:
                TableTag.create(article=article, tag=tag)
