from scipy.cluster.vq import vq, kmeans, kmeans2, whiten
import numpy as np

def buildCodeBook(features, k):
    whitened = whiten(features)
    codebook, distortion = kmeans(whitened, k)
    return (whitened, codebook, distortion)

def _prepareDataset(dataset, listName):
    # Transform a dictionary into a np.array
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
    # datasetArray = np.zeros(10)
    length = datasetArray.shape[0]
    trainingLength = int(length*trainingProportion)
    # print(datasetArray.shape[0])
    # print(trainingLength,datasetArray[:trainingLength].shape)
    # print(length-trainingLength,datasetArray[trainingLength:].shape)
    datasetArray2 = datasetArray
    if shuffle:
        np.random.shuffle(datasetArray2)
        return datasetArray2[:trainingLength], datasetArray2[trainingLength:]
    return datasetArray[:trainingLength], datasetArray[trainingLength:]


def buildAndCompare(features, k, listItem, trainingProportion=0.5):

    dataArray = _prepareDataset(features,listItem)
    whitenedDataArray = whiten(dataArray)
    trainingSet, analysisSet = splitDataset(whitenedDataArray,trainingProportion,True)
    whitened, codebook, distortion = buildCodeBook(trainingSet, k)
    codebook, distortionTraining = kmeans(whitened, k)
    obs_code, distortionAnalysis = vq(analysisSet, codebook, check_finite=False)
    # print(distortionAnalysis.mean())
    return distortionTraining.mean(), distortionAnalysis.mean(), codebook, trainingSet, analysisSet
    # whitenedAnalysis = whiten(analysisSet)
    # whitenedTraining = whiten(trainingSet)
    # print(whitenedAnalysis)
    # print(whitenedTraining)
    # for i in range(1,20):
    #     whitened, codebook, distortion = buildCodeBook(trainingSet, i)
    #     obs_code, distort = vq(analysisSet, codebook, check_finite=False)
    #     listNumberCluster.append(i)
    #     listDistortions.append(distortion)
    # plot(listDistortions,listNumberCluster,title="distance_to_centroids_vs_number_of_clusters_analysis")
