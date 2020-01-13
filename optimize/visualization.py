import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns
import os


def get_plot_of_optimization(list_of_mins, list_of_avgs, save_to_file=False, dir=''):
    array_of_mins = np.array(list_of_mins)
    array_of_avgs = np.array(list_of_avgs)
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    plt.plot(array_of_mins, label='mins')
    plt.plot(array_of_avgs, label='avgs')
    plt.title('History of optimization')
    plt.xlabel('iteration')
    plt.ylabel('value')
    plt.legend()

    if save_to_file:
        plt.savefig(os.path.join(dir, 'debit_prod.png'))
    else:
        plt.show()


def box_with_whiskers(min_data_frame, avg_data_frame, save_to_file=False, dir=''):
    fig, ax = plt.subplots(2, 1, figsize=(30, 15))
    sns.boxplot(data=min_data_frame, color='blue', ax=ax[0])
    sns.boxplot(data=avg_data_frame, color='blue', ax=ax[1])
    ax[0].set(xlabel='iteration', ylabel='min_distribution')
    ax[1].set(xlabel='iteration', ylabel='avg_distribution')

    if save_to_file:
        plt.savefig(os.path.join(dir, 'loss_history_boxplots.png'))
    else:
        plt.show()


def fun(x, y):
    return x**2 + y**2

# TODO object function transfer
def three_d_surface(generation):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.array([generation[i][0] for i in range(len(generation))])
    y = np.array([generation[i][1] for i in range(len(generation))])
    X, Y = np.meshgrid(x, y)
    zs = np.array(fun(np.ravel(X), np.ravel(Y)))
    Z = zs.reshape(X.shape)

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.pause(0.5)
    plt.draw()


def three_d_scatter(generation):
    data = data_update(generation)
    plt.style.use('ggplot')
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_zlabel(f'iter')
    # ax.set_ylabel()
    # ax.set_xlabel()
    for global_index, gen in enumerate(data):
        for index in range(len(gen)):
            individuals = [(gen[x][0], gen[x][1], global_index) for x in range(len(gen))]
            for ind in individuals:
                ax.scatter(ind[0], ind[1], ind[2])
    plt.pause(0.5)
    plt.draw()


data = []


def data_update(generation):
    data.append(generation)
    return data
