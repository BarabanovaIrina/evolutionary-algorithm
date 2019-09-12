import matplotlib.pyplot as plt
import numpy as np


def get_plot(number_of_generations, list_of_mins, list_of_avgs):
    mins = np.array(list_of_mins)
    avgs = np.array(list_of_avgs)
    plt.plot(mins, label='mins')
    plt.plot(avgs, label='avgs')
    plt.title('Hostory of optimization')
    plt.legend()
    plt.show()