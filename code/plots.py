import morphologging
logger = morphologging.getLogger(__name__)

import matplotlib.pyplot as plt

def plot(y,x=None,title="plot", save=True):
    logger.info("plotting {}".format(title))
    plt.figure(1)
    
    plt.gcf().clear()
    plt.gcf().clear()
    if x==None:
        plt.plot(y, 'ro')
    else:
        plt.plot(x,y,'ro')
    plt.title(title)
    if save:
        plt.savefig('../plots/{}.pdf'.format(title))

def clusterPlot(whitened,book, iX, iY, title="boxPlots", save=True):
    logger.info("cluster plotting {}".format(title))
    plt.figure(1)
    plt.gcf().clear()
    plt.gcf().clear()
    plt.scatter(whitened[:,iX],whitened[:,iY])
    plt.scatter(book[:,iX],book[:,iY], c='r')
    plt.title(title)
    if save:
        plt.savefig('../plots/{}.pdf'.format(title))
    

        

