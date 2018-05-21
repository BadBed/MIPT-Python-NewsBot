from s_database import TableTopic, TableArticle, TableTag
from collections import defaultdict
import re


def all_last_articles():
    """
    Возвращает все статьи
    :return: статьи, упорядоченные по времени добавления
    """
    return (TableArticle.select().
            order_by(TableArticle.last_update.desc()))


def all_last_topics():
    """
    Возвращает все темы
    :return: темы, упорядоченные по времени обновления
    """
    return (TableTopic.select().
            order_by(TableTopic.last_update.desc()))


def last_articles(count):
    """
    Возвращает несколько последних статей
    :param count: необходимое количество статей
    :return: несколько последних статей
    """
    return all_last_articles().limit(count)


def last_topics(count):
    """
    Возвращает несколько последних тем
    :param count: необходимое количество тем
    :return: несколько последних тем
    """
    return all_last_topics().limit(count)


def all_articles_by_topic(topic_title):
    """
    Возвращает все статьи в теме
    :param topic_title: заголовок темы
    :return: все статьи в теме, упорядоченные по времени добавления
    """
    return (TableArticle.select().
            join(TableTopic).
            where(TableTopic.title == topic_title).
            order_by(TableArticle.last_update.desc()))


def articles_by_topic(topic_title, count):
    """
    Возвращает несколько последних статей в теме
    :param topic_title: заголовок темы
    :param count: необходимое количество статей
    :return: несколько последних статьей в теме
    """
    return all_articles_by_topic(topic_title).limit(count)


def tags_by_topic(topic_title):
    """
    Возвращает тэги темы
    :param topic_title: заголовок темы
    :return: все тэги темы
    """
    return (TableTag.select().
            join(TableArticle).
            join(TableTopic).
            where(TableTopic.title == topic_title))


def find_topic(topic_title):
    """
    Поиск темы по названию
    :param topic_title: заголовок темы
    :return: тема
    """
    return (TableTopic.select().
            where(TableTopic.title == topic_title).
            get())


def find_article(art_title):
    """
    Поиск статьи по названию
    :param art_title: заголовок статьи
    :return: статья
    """
    return (TableArticle.select().
            where(TableArticle.title == art_title).
            get())


def is_article_in_database(art_title):
    """
    Возвращает, есть ли статья в базе
    :return: True, если статья есть в базе данных, False иначе
    """
    return all_last_articles().where(TableArticle.title 
            == art_title).count() != 0


def is_topic_in_database(topic_title):
    """
    Возвращает, есть ли топик в базе
    :return: True, если топик есть в базе данных, False иначе
    """
    return all_last_topics().where(TableTopic.title
            == topic_title).count() != 0


def best_tags(topic_title, count):
    """
    Популярные тэги
    :param topic_title: заголовок темы
    :param count: необходимое количество тэгов
    :return: несколько самых популярных тэгов темы
    """
    tags_dict = defaultdict(int)
    for i in tags_by_topic(topic_title):
        tags_dict[i.tag] += 1

    result = [(x, tags_dict[x]) for x in tags_dict]
    result.sort(key=(lambda c: -c[1]))
    return [i[0] for i in result][:count]


def get_words(text):
    """
    Все слова какого-либо текста
    :param text: текст
    :return: список всех его слов
    """
    return list(map(lambda s: s.lower(), re.findall(r"\w+", text)))


def word_len_freq(text):
    """
    Частота длин слов
    :param text: текст
    :return: словарь частот длин слов в этом тексте
    """
    words = get_words(text)
    word_dict = defaultdict(int)
    for word in words:
        word_dict[len(word)] += 1

    return word_dict


def word_freq(text):
    """
    Частота слов
    :param text: текст
    :return: словарь частот слов в этом тексте
    """
    words = get_words(text)
    word_dict = defaultdict(int)
    for word in words:
        if len(word) > 2:
            word_dict[word] += 1

    return word_dict


def word_count(text):
    """
    Количество слов
    :param text: текст
    :return: количество слов в нём
    """
    return len(get_words(text))


def docs_count_in_topic(topic_title):
    """
    Количество статьей в теме
    :param topic_title: заголовок темы
    :return: количество статей в ней
    """
    topic = find_topic(topic_title)
    return len(topic.articles)


def words_count_in_topic(topic_title):
    """
    Количество слов в теме
    :param topic_title: заголовок темы
    :return: количество слов в ней
    """
    articles = all_articles_by_topic(topic_title)
    result = 0
    for article in articles:
        result += word_count(article.text)
    return result


def most_popular_words(topic_title, count):
    """
    Самые популярные слова в теме (список)
    :param topic_title: заголовок темы
    :param count: необходимое количество слов
    :return: список самых популярных слов
    """
    freq_dict = word_freq(find_article(topic_title).text)
    result = [(u, freq_dict[u]) for u in freq_dict]
    result.sort(key=lambda x: -x[1])
    return result[:count]


def dicts_sum(*dicts):
    """
    Слияние словарей
    :param dicts: список словарей, которые необходимо слить
    :return: результат их слияния
    """
    result = defaultdict(int)
    for cur_dict in dicts:
        for i in cur_dict:
            result[i] += cur_dict[i]
    return result


def word_freq_in_topic(topic_title):
    """
    Частота слов в теме
    :param topic_title: заголовок темы
    :return: словарь частот слов в теме
    """
    articles = all_articles_by_topic(topic_title)
    small_freqs = [word_freq(article.text) for article in articles]
    return dicts_sum(*small_freqs)


def word_len_freq_in_topic(topic_title):
    """
    Частота длин слов в теме
    :param topic_title: заголовок темы
    :return: словарь частот длин слов в теме
    """
    articles = all_articles_by_topic(topic_title)
    small_freqs = [word_len_freq(article.text) for article in articles]
    return dicts_sum(*small_freqs)


def most_popular_words_in_topic(topic_title, count):
    """
    Самые популярные слова в теме (словарь с частотами)
    :param topic_title: заголовок темы
    :param count: необходимое число слов
    :return: словарь популярных слов с частотами
    """
    freq_dict = word_freq_in_topic(find_topic(topic_title).title)
    result = [(u, freq_dict[u]) for u in freq_dict]
    result.sort(key=lambda x: -x[1])
    return result[:count]
