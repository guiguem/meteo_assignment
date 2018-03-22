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

def addDerivatives(dataset,listName, timeName=None):
    logger.info("Add derivatives")
    if timeName is not None:
        times = dataset.get(timeName)
    else:
        times = [i for i in range(len(dataset.get(listName[0])))]
    for a_var in listName:
        values = dataset.get(a_var)
        derivatives = [(values[i+1] - values[i])/(times[i+1]-times[i]) for i in range(len(values)-1)]
        dataset.update({"der_{}".format(a_var): derivatives})
    return dataset



