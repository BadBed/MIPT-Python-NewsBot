import matplotlib.pyplot as plt


def plot(x, y, title, xlabel, ylabel, file):
    """
    Построение графика
    :param x: разметка по х-координате
    :param y: разметка по у-координате
    :param title: название графика
    :param xlabel: название х-координаты
    :param ylabel: название у-координаты
    :param file: название файда для записи
    :return: сохранённый график
    """
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(file)
    plt.close()


def plot_words_len_freq(data, file):
    """
    Построение графика частот длин слов
    :param data: данные для построения графика
    :param file: название файда для записи
    """
    y = []
    for cur_len in data:
        while len(y) <= cur_len:
            y.append(0)
        y[cur_len] = data[cur_len]

    plot(range(len(y)), y, "Words' length frequency",
         'word length', 'frequency', file)
