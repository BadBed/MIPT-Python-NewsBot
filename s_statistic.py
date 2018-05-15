from s_database import TableTopic, TableArticle, TableTag
from collections import defaultdict
import re


def all_last_articles():
    return (TableArticle.select().
            order_by(TableArticle.last_update.desc()))


def all_last_topics():
    return (TableTopic.select().
            order_by(TableTopic.last_update.desc()))


def last_articles(count):
    return all_last_articles().limit(count)


def last_topics(count):
    return all_last_topics().limit(count)


def all_articles_by_topic(topic_title):
    return (TableArticle.select().
            join(TableTopic).
            where(TableTopic.title == topic_title).
            order_by(TableArticle.last_update.desc()))


def articles_by_topic(topic_title, count):
    return all_articles_by_topic(topic_title).limit(count)


def tags_by_topic(topic_title):
    return (TableTag.select().
            join(TableArticle).
            join(TableTopic).
            where(TableTopic.title == topic_title))


def find_topic(topic_title):
    return (TableTopic.select().
            where(TableTopic.title == topic_title).
            get())


def find_article(art_title):
    return (TableArticle.select().
            where(TableArticle.title == art_title).
            get())


def best_tags(topic_title, count):
    dict = defaultdict(int)
    for i in tags_by_topic(topic_title):
        dict[i.tag] += 1
    #Сортируем по
    result = [(x, dict[x]) for x in dict]
    result.sort(key=(lambda c: -c[1]))
    return [i[0] for i in result][:count]


def get_words(text):
    return list(map(lambda s: s.lower(), re.findall(r"\w+", text)))


def word_len_freq(text):
    words = get_words(text)
    dict = defaultdict(int)
    for word in words:
        dict[len(word)] += 1

    return dict


def word_freq(text):
    words = get_words(text)
    dict = defaultdict(int)
    for word in words:
        dict[word] += 1

    return dict


def word_count(text):
    return len(get_words(text))


def docs_count_in_topic(topic_title):
    topic = find_topic(topic_title)
    return len(topic.articles)


def words_count_in_topic(topic_title):
    arts = all_articles_by_topic(topic_title)
    result = 0
    for art in arts:
        result += word_count(art.text)
    return result


def most_popular_words(topic_title, count):
    dct = word_freq(find_article(topic_title).text)
    res = [(u, dct[u]) for u in dct]
    res.sort(key = lambda x: -x[1])
    return res[:count]


def dicts_sum(*dicts):
    result = defaultdict(int)
    for d in dicts:
        for i in d:
            result[i] += d[i]
    return result

def word_freq_in_topic(topic_title):
    arts = all_articles_by_topic(topic_title)
    small_freqs = [word_freq(i.text) for i in arts]
    return dicts_sum(*small_freqs)


def word_len_freq_in_topic(topic_title):
    arts = all_articles_by_topic(topic_title)
    small_freqs = [word_len_freq(i.text) for i in arts]
    return dicts_sum(*small_freqs)


def most_popular_words_in_topic(topic_title, count):
    dct = word_freq_in_topic(find_topic(topic_title).title)
    res = [(u, dct[u]) for u in dct]
    res.sort(key = lambda x: -x[1])
    return res[:count]
