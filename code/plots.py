import morphologging
logger = morphologging.getLogger(__name__)

import matplotlib.pyplot as plt

def plot(y,x=None,title=""):
    logger.info("plotting {}".format(title))
    plt.figure(1)
    
    plt.gcf().clear()
    plt.gcf().clear()
    if x==None:
        plt.plot(y, 'ro')
    else:
        plt.plot(x,y,'ro')
    plt.title(title)
    plt.savefig('../plots/{}.pdf'.format(title))