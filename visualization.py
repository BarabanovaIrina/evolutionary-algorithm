import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def get_plot(list_of_mins, list_of_avgs):
    mins = np.array(list_of_mins)
    avgs = np.array(list_of_avgs)
    plt.plot(mins, label='mins')
    plt.plot(avgs, label='avgs')
    plt.title('Hostory of optimization')
    plt.legend()
    plt.show()


def box_with_whiskers(data_frame):
    sns.boxplot(data=data_frame)
    plt.show()
