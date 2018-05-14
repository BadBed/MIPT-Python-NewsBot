from telebot import TeleBot
import statistic
import graphics
import loader


bot = TeleBot('560308205:AAF2VvyafzjeL0Oe3CFzHm4nV5bbMDRh9Og')

@bot.message_handler(commands=['nbh'])
def f(message):
    message.text
    message.chat.id
    bot.send_message(message.chat.id, "kek")


@bot.message_handler(commands=['help'])
def com_help(message):
    bot.send_message(message.chat.id,
    """\\help - показать все, что может бот. \n
    \\new_docs <N> - показать N самых свежих новостей. \n
    \\new_topics <N> - показать N самых свежих тем. \n
    \\topic <topic_name> - показать описание темы и заголовки 5 самых
     свежих новостей в этой теме. \n
    \\doc <doc_title> - показать текст документа с заданным заголовком. \n
    \\words <topic_name> - показать 5 самых популярных тегов по этой тему. \n
    \\describe_doc <doc_title> - вывести статистику по документу. \n
    \\describe_topic <topic_name> - вывести статистику по теме. \n
    """)


@bot.message_handler(commands=['new_docs'])
def com_new_docs(message):
    try:
        n = int(message.text.split()[1])
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    for i in statistic.last_articles(n):
        bot.send_message(message.chat.id, str(i.title) + '\n' + str(i.url))


@bot.message_handler(commands=['new_topics'])
def com_new_topics(message):
    try:
        n = int(message.text.split()[1])
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    for i in statistic.last_topics(n):
        bot.send_message(message.chat.id, i.title + '\n' + i.url)


@bot.message_handler(commands=['topic'])
def com_topic(message):
    try:
        topic_title = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    topic = statistic.find_topic(topic_title)
    bot.send_message(message.chat.id, topic.title + '\n' + topic.description)

    for i in statistic.articles_by_topic(topic_title):
        bot.send_message(message.chat.id, i.title + '\n' + i.url)


@bot.message_handler(commands=['doc'])
def com_doc(message):
    try:
        art_title = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    art = statistic.find_article(art_title)
    bot.send_message(message.chat.id, art.title + '\n' + art.text)


@bot.message_handler(commands=['words'])
def com_words(message):
    try:
        topic = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    for t in statistic.best_tags(5):
        bot.send_message(message.chat.id, t)


@bot.message_handler(commands=['describe_doc'])
def com_descr_doc(message):
    try:
        title = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    graphics.plot_words_len_freq(
        statistic.word_freq(statistic.find_article(title).text), "plot.png")
    f = open("plot.png", "rb")
    bot.send_photo(message.chat.id, f)
    f.close()

    mes = "Самые популярные слова:\n"
    for i in statistic.most_popular_words(title, 15):
        mes += i[0] + ' - ' + str(i[1]) + 'раз\n'
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=['describe_topic'])
def com_descr_doc(message):
    try:
        title = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Некорректная команда")
        return None

    bot.send_message(message.chat.id, "Количесвто слов в теме:" +
                     statistic.words_count_in_topic(title))

    bot.send_message(message.chat.id, "Количесвто статей в теме:" +
                     statistic.docs_count_in_topic(title))

    graphics.plot_words_len_freq(
        statistic.word_freq_in_topic(title), "plot.png")
    f = open("plot.png", "rb")
    bot.send_photo(message.chat.id, f)
    f.close()

    mes = "Самые популярные слова:\n"
    for i in statistic.most_popular_words_in_topic(title, 15):
        mes += i[0] + ' - ' + str(i[1]) + 'раз\n'
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=['text'])
def if_send_text(message):
    bot.send_message(message.chat.id, "Тут должна быть смешнявка, но ее нет. Извините.")


def start_bot():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    start_bot()
