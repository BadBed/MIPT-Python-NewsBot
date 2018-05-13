import matplotlib.pyplot as plt
import pandas as pnd
import statistic


def plot(x, y, title, xlabel, ylabel, file=None):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if file is not None:
        plt.savefig(file)


def plot_words_len_freq(data, file=None):
    y = []
    for cnt in data:
        while len(y) <= cnt:
            y.append(0)
        y[cnt] = data[cnt]

    plot(range(len(y)), y, None, 'word length', 'frequency', file)
