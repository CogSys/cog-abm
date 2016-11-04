import numpy as np
import matplotlib.pyplot as plt

def chart(res, x_label, y_label):

    plt.ylabel(y_label)
    plt.xlabel(x_label)

    ax = np.array([x for x, _ in res])
    ay = np.array([y for _, y in res])
    plt.plot(ax, ay)
    plt.show()
