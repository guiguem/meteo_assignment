import morphologging
logger = morphologging.getLogger(__name__)


from scipy.cluster.vq import vq, kmeans, kmeans2, whiten
import numpy as np

def buildCodeBook(features, k):
    whitened = whiten(features)
    codebook, distortion = kmeans(whitened, k)
    return (whitened, codebook, distortion)

def _prepareDataset(dataset, listName):
    '''
    Transform a dictionary into a np.array
    '''
    array = []
    length = -1
    for a_key, a_list in dataset.items():
        if length<0 or length>len(a_list):
            length = len(a_list)
    for i in range(length): 
        subarray = []    
        for a_key in listName:
            subarray.append(dataset[a_key][i])
        array.append(subarray)
    return np.array(array)

def splitDataset(datasetArray, trainingProportion=0.5, shuffle=False):
    length = datasetArray.shape[0]
    trainingLength = int(length*trainingProportion)
    datasetArray2 = datasetArray
    if shuffle:
        np.random.shuffle(datasetArray2)
        return datasetArray2[:trainingLength], datasetArray2[trainingLength:]
    return datasetArray[:trainingLength], datasetArray[trainingLength:]


def buildAndCompare(features, k, listItem, trainingProportion=0.5):
    '''
    Split the data in a training set and a testing set, train on the training set and extract the errors from the testing one.
    '''
    # logger.info("Clustering in split set")
    dataArray = _prepareDataset(features,listItem)
    whitenedDataArray = whiten(dataArray)
    trainingSet, analysisSet = splitDataset(whitenedDataArray,trainingProportion,True)
    whitened, codebook, distortion = buildCodeBook(trainingSet, k)
    codebook, distortionTraining = kmeans(whitened, k)
    obs_code, distortionAnalysis = vq(analysisSet, codebook, check_finite=False)
    return distortionTraining.mean(), distortionAnalysis.mean(), codebook, trainingSet, analysisSet
