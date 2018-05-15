import s_parser
import os
import dateparser
import s_statistic
from s_database import TableTag, TableArticle, TableTopic


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
    topics = s_parser.parse_topics_list()
    for t in topics:
        articles = s_parser.parse_topic(t['url'])
        if articles[0]['time'] < time:
            break

        print('TOPIC:', t['title'])
        try:
            topic = s_statistic.find_topic(t['title'])
        except:
            topic = TableTopic.create(title=t['title'],
                                    url=t['url'],
                                    description=t['description'],
                                    last_update=articles[0]['time'])

        for a in articles:
            if (a['time'] < time):
                break

            art = s_parser.parse_article(a['url'])
            print('article:', a['title'])
            article = TableArticle.create(topic=topic,
                                          title=a['title'],
                                          url=a['url'],
                                          text=art['text'],
                                          last_update=a['time'])

            for tag in art['tags']:
                TableTag.create(article=article, tag=tag)
