import matplotlib.pyplot as plt
import pandas as pnd


def plot(x, y, title, xlabel, ylabel, file):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(file)
    plt.close()


def plot_words_len_freq(data, file):
    y = []
    for cnt in data:
        while len(y) <= cnt:
            y.append(0)
        y[cnt] = data[cnt]

    plot(range(len(y)), y, None, 'word length', 'frequency', file)
