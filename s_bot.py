from telebot import TeleBot
import s_statistic
import s_graphics
import re
import dateparser
import s_loader


bot = TeleBot('560308205:AAF2VvyafzjeL0Oe3CFzHm4nV5bbMDRh9Og')
HELP = '''/help - показать все, что может бот. \n
/new_docs <N> - показать N самых свежих новостей. \n
/new_topics <N> - показать N самых свежих тем. \n
/topic <topic_name> - показать описание темы и заголовки 5 самых
свежих новостей в этой теме. \n
/doc <doc_title> - показать текст документа с заданным заголовком. \n
/tags <topic_name> - показать 5 самых популярных тегов по этой теме. \n
/describe_doc <doc_title> - вывести статистику по документу. \n
/describe_topic <topic_name> - вывести статистику по теме. \n'''
STANDARD_NUMBER = 5
STANDARD_WORD_NUMBER = 15
STANDARD_DATE = "14.05.2018"
MIN_WORD_LEN_FOR_FREQ = 1


def com_start(message):
    """
    Начало работы бота
    :param message: сообщение пользователя
    :return: посылает сообщение о начале работы
    """
    bot.send_message(message.chat.id, "К работе готов.")


def com_help(message):
    """
    Справка
    :param message: сообщение пользователя
    :return: посылает сообщение-справку
    """
    bot.send_message(message.chat.id, HELP)


def com_new_docs(message):
    """
    Новые статьи
    :param message: сообщение пользователя
    :return: посылает несколько новых статей
    """
    try:
        number = int(message.text.split()[1])
    except TypeError:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None
    except IndexError:
        number = STANDARD_NUMBER

    for article in s_statistic.last_articles(number):
        bot.send_message(message.chat.id, str(article.title) +
                         '\n' + str(article.url))


def com_new_topics(message):
    """
    Обновлённые темы
    :param message: сообщение пользователя
    :return: посылает несколько обновлённых тем
    """
    try:
        number = int(message.text.split()[1])
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Некорректная команда")
        return None
    except IndexError:
        number = STANDARD_NUMBER

    for topic in s_statistic.last_topics(number):
        bot.send_message(message.chat.id, topic.title + '\n' + topic.url)


def com_topic(message):
    """
    Описание темы
    :param message: сообщение пользователя
    :return: посылает описание темы и несколько её последних статей
    """
    try:
        topic_title = re.sub("/topic ", "", message.text, 1)
        topic = s_statistic.find_topic(topic_title)
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    bot.send_message(message.chat.id, topic.title + '\n' + topic.description)

    for article in s_statistic.articles_by_topic(topic_title,
                                                 STANDARD_NUMBER):
        bot.send_message(message.chat.id, article.title + '\n' + article.url)


def com_doc(message):
    """
    Текст статьи
    :param message: сообщение пользователя
    :return: посылает текст статьи
    """
    try:
        art_title = re.sub("/doc ", "", message.text, 1)
        article = s_statistic.find_article(art_title)
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    bot.send_message(message.chat.id, article.title + '\n' + article.text)


def com_tags(message):
    """
    Популярные в теме тэги
    :param message: сообщение пользователя
    :return: посылает 5 самых популярных тэгов темы
    """
    try:
        topic = re.sub("/tags ", "", message.text, 1)
        for tag in s_statistic.best_tags(topic, STANDARD_NUMBER):
            bot.send_message(message.chat.id, tag)
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Некорректная команда")
        return None


def com_describe_doc(message):
    """
    Статистика статьи
    :param message: сообщение пользователя
    :return: посылает график частот длин слов и
        15 самых популярных значимых слов в статье
    """
    try:
        title = re.sub("/describe_doc ", "", message.text, 1)
        s_statistic.find_article(title)
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    s_graphics.plot_words_len_freq(
        s_statistic.word_len_freq(s_statistic.find_article(title).text),
        "plot.png")
    plot_file = open("plot.png", "rb")
    bot.send_photo(message.chat.id, plot_file)
    plot_file.close()

    bot_message = "Самые популярные слова:\n"
    for word in s_statistic.most_popular_words(title,
                                               STANDARD_WORD_NUMBER,
                                               MIN_WORD_LEN_FOR_FREQ):
        bot_message += word[0] + ' - ' + str(word[1]) + ' раз\n'
    bot.send_message(message.chat.id, bot_message)


def com_describe_topic(message):
    """
    Статистика темы
    :param message: сообщение пользователя
    :return: посылает количество слов и статей в теме,
        среднюю длину статьи в теме,
        график частот длин слов и
        15 самых популярных значимых слов в теме
    """
    try:
        title = re.sub("/describe_topic ", "", message.text, 1)
        s_statistic.find_topic(title)
    except Exception as err:
        print(err)
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    bot.send_message(message.chat.id, "Количество слов в теме: " +
                     str(s_statistic.words_count_in_topic(title)))

    bot.send_message(message.chat.id, "Количесвто статей в теме: " +
                     str(s_statistic.docs_count_in_topic(title)))

    bot.send_message(message.chat.id, "Средняя длина статьи " +
                     str(round(s_statistic.words_count_in_topic(title) /
                               s_statistic.docs_count_in_topic(title))) +
                     ' слов')

    s_graphics.plot_words_len_freq(
        s_statistic.word_len_freq_in_topic(title), "plot.png")
    plot_file = open("plot.png", "rb")
    bot.send_photo(message.chat.id, plot_file)
    plot_file.close()

    bot_message = "Самые популярные слова:\n"
    for word in s_statistic.most_popular_words_in_topic(title,
                                                        STANDARD_WORD_NUMBER,
                                                        MIN_WORD_LEN_FOR_FREQ):
        bot_message += word[0] + ' - ' + str(word[1]) + ' раз\n'
    bot.send_message(message.chat.id, bot_message)


@bot.message_handler(commands=['start', 'help', 'topic',
                               'doc', 'tags', 'new_docs',
                               'new_topics', 'describe_topic',
                               'describe_doc'])
def if_send_command(message):
    """
    Принимает команду от пользователя
    :param message: сообщение пользователя (команда и текст)
    :return: выполняет одну из команд
    """
    command = re.findall(r'\w+', message.text)[0]
    exec("com_" + command + "(message)")


@bot.message_handler(content_types=['text'])
def if_send_text(message):
    """
    Принимает текст без команды
    :param message: сообщение пользователя
    :return: сообщение бота
    """
    bot.send_message(message.chat.id,
                     "Тут должна быть смешнявка, но ее нет. Извините.")


def start_bot():
    """
    Запуск бота с автоматическим обновлением базы данных
    """
    # s_loader.load_new(STANDARD_DATE)
    print("Я готов к работе")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    start_bot()
