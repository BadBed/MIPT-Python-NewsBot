from my_database import TableTopic, TableArticle, TableTag


def last_articles(count):
    return list(TableArticle.select().
                order_by(TableArticle.last_update.desc()).
                limit(count))


def last_topics(count):
    return list(TableTopic.select().
                join(TableArticle).
                order_by(TableArticle.last_update.desc()).
                limit(count))


def articles_in_topic(topic_title, count=5):
    return list(TableArticle.select().
                join(TableTopic).
                where(TableTopic.title == topic_title).
                order_by(TableArticle.last_update.desc()).
                limit(count))
