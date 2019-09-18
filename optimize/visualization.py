import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def get_plot_of_optimization(list_of_mins, list_of_avgs):
    array_of_mins = np.array(list_of_mins)
    array_of_avgs = np.array(list_of_avgs)
    plt.plot(array_of_mins, label='mins')
    plt.plot(array_of_avgs, label='avgs')
    plt.title('History of optimization')
    plt.xlabel('iteration')
    plt.ylabel('value')
    plt.legend()
    plt.show()


def box_with_whiskers(min_data_frame, avg_data_frame):
    fig, ax = plt.subplots(2,1)
    sns.boxplot(data=min_data_frame, color='blue', ax=ax[0])
    sns.boxplot(data=avg_data_frame, color='blue', ax=ax[1])
    ax[0].set(xlabel='iteration', ylabel='min_distribution')
    ax[1].set(xlabel='iteration', ylabel='avg_distribution')
    plt.show()

