import morphologging
logger = morphologging.getLogger(__name__)

import allantools
import numpy as np

def plotASD(x,title=""):

    logger.info("plotting Allan Standard Deviation ({})".format(title))

    a = allantools.Dataset(data=x)
    a.compute("mdev")
    b = allantools.Plot()
    b.plot(a, errorbars=True, grid=True)
    b.ax.set_xlabel("Tau (#)")
    b.plt.title(title)
    b.plt.yscale('log')
    # b.show()
    b.plt.savefig('../plots/{}.pdf'.format(title))

def averageData(x,nAverage):
    logger.info("Average over {} samples".format(nAverage))
    array = np.asarray(x)
    def average(arr, n):
        end =  n * int(len(arr)/n)
        return np.mean(arr[:end].reshape(-1, n), 1)
    avArray = average(array, nAverage)
    return avArray.tolist()
        

    # import matplotlib.pyplot as plt
    # plt.figure(1)

