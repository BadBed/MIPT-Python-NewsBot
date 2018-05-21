import s_parser
import dateparser
import s_statistic
from s_database import TableTag, TableArticle, TableTopic

TODAY = str(dateparser.parse('today'))


def load_new(default_time):
    """
    Загрузка новых статей в формирующуюся базу данных
    :param default_time: ограничение на время публикации для статей
    """
    try:
        db_file = open('last_update_db', 'r')
        time = dateparser.parse(db_file.read())
        db_file.close()
    except FileNotFoundError:
        time = dateparser.parse(default_time)

    load(time)

    db_file = open('last_update_db', 'w')
    db_file.write(TODAY)
    db_file.close()


def load(time):
    """
    Подгрузка новостей к сформированной базе данных
    :param time: ограничение на время публикации для статей
    """
    topics = s_parser.parse_topics_list()
    for topic in topics:
        articles = s_parser.parse_topic(topic['url'])
        if articles[0]['time'] < time:
            break

        print('TOPIC:', topic['title'])
        if not s_statistic.is_topic_in_database(topic['title']):
            topic = TableTopic.create(title=topic['title'],
                                      url=topic['url'],
                                      description=topic['description'],
                                      last_update=articles[0]['time'])

        for article in articles:
            if article['time'] < time:
                break

            print('article:', article['title'])
            if not s_statistic.is_article_in_database(article['title']):
                article_text = s_parser.parse_article(article['url'])
                article = TableArticle.create(topic=topic,
                                              title=article['title'],
                                              url=article['url'],
                                              text=article_text['text'],
                                              last_update=article['time'])

                for tag in article_text['tags']:
                    TableTag.create(article=article, tag=tag)
