import morphologging
logger = morphologging.getLogger(__name__)

from IO import extractData
from misc import addDerivatives
from plots import clusterPlot, plot
from clustering import buildCodeBook, _prepareDataset, splitDataset, buildAndCompare

from os import listdir
from os.path import isfile, join
import numpy as np
from scipy.cluster.vq import vq, whiten


datafile = "../results/sgpmetavgE13.b1.20180101.000000.cdf"
pathToResults = "../results"
listVOI = ["timeSinceBaseTime","atmospheric_pressure", "relative_humidity", "mean_temperature"]
listDer = ["atmospheric_pressure", "relative_humidity", "mean_temperature"]
listItem = ["atmospheric_pressure","mean_temperature","relative_humidity","der_atmospheric_pressure","der_mean_temperature","der_relative_humidity"]
# listItem = ["atmospheric_pressure","mean_temperature"]

##############################################################

dataset = extractData(datafile,listVOI,timeShift=False)
dataset = addDerivatives(dataset,listDer,"timeSinceBaseTime")



# checking that the data are doing all right
# plot(dataset["atmospheric_pressure"],dataset["timeSinceBaseTime"],title="atmospheric_pressure_2")

from scipy.cluster.vq import vq, kmeans, whiten
pts = 50
a = np.random.multivariate_normal([0, 0], [[4, 1], [1, 4]], size=pts)
b = np.random.multivariate_normal([30, 10],
                                  [[10, 2], [2, 1]],
                                  size=pts)
features = np.concatenate((a, b))


whitened, codebook, distortion = buildCodeBook(_prepareDataset(dataset,listItem), 2)
clusterPlot(whitened, codebook,0, 1,"0_1")
clusterPlot(whitened, codebook,0, 2,"0_2")
clusterPlot(whitened, codebook,0, 3,"0_3")
clusterPlot(whitened, codebook,0, 4,"0_4")
clusterPlot(whitened, codebook,0, 5,"0_5")
clusterPlot(whitened, codebook,1, 2,"1_2")
clusterPlot(whitened, codebook,1, 3,"1_3")
clusterPlot(whitened, codebook,1, 4,"1_4")
clusterPlot(whitened, codebook,1, 5,"1_5")
clusterPlot(whitened, codebook,2, 3,"2_3")
clusterPlot(whitened, codebook,2, 4,"2_4")
clusterPlot(whitened, codebook,2, 5,"2_5")
clusterPlot(whitened, codebook,3, 4,"3_4")
clusterPlot(whitened, codebook,3, 5,"3_5")
clusterPlot(whitened, codebook,4, 5,"4_5")

# Look at the training distortion getting better everytime
listNumberCluster = []
listDistortions = []
for i in range(1,20):
    whitened, codebook, distortion = buildCodeBook(_prepareDataset(dataset,listItem), i)
    # from scipy.cluster.vq import vq
    # obs_code, distort = vq(whitened, codebook, check_finite=False)
    listNumberCluster.append(i)
    listDistortions.append(distortion)
plot(listDistortions,listNumberCluster,title="distance_to_centroids_vs_number_of_clusters")

listNumberCluster = []
listDistortionsTraining = []
listDistortionsAnalysis = []

for i in range(1,40):   
    print(i)
    listDistortionsTrainingTemp = [] 
    listDistortionsAnalysisTemp = [] 
    for j in range(0,100):
        distortionTraining, distortionAnalysis, codebook, trainingSet, analysisSet = buildAndCompare(dataset,i,listItem,0.9)
        listDistortionsTrainingTemp.append(distortionTraining)
        listDistortionsAnalysisTemp.append(distortionAnalysis)
    
    listNumberCluster.append(i)
    listDistortionsTraining.append(sum(listDistortionsTrainingTemp) / float(len(listDistortionsTrainingTemp)))
    listDistortionsAnalysis.append(sum(listDistortionsAnalysisTemp) / float(len(listDistortionsAnalysisTemp)))
    # print(distortionTraining, distortionAnalysis)
# print(listDistortions)
plot(listDistortionsTraining,listNumberCluster,title="distance_to_centroids_vs_number_of_clusters_training")
plot(listDistortionsAnalysis,listNumberCluster,title="distance_to_centroids_vs_number_of_clusters_analysis")

# dataArray = _prepareDataset(dataset,listItem)
# whitenedDataArray = whiten(dataArray)
# trainingSet, analysisSet = splitDataset(whitenedDataArray,0.5,True)
# # whitenedAnalysis = whiten(analysisSet)
# # whitenedTraining = whiten(trainingSet)
# # print(whitenedAnalysis)
# # print(whitenedTraining)
# # for i in range(1,20):
# #     whitened, codebook, distortion = buildCodeBook(trainingSet, i)
# #     obs_code, distort = vq(analysisSet, codebook, check_finite=False)
# #     listNumberCluster.append(i)
# #     listDistortions.append(distortion)
# # plot(listDistortions,listNumberCluster,title="distance_to_centroids_vs_number_of_clusters_analysis")

# whitened, codebook, distortion = buildCodeBook(trainingSet, 2)
# print(whitened)
# print(codebook)
# clusterPlot(whitened, codebook,0, 1,"0_1_training")
# whitened, codebook, distortion = buildCodeBook(analysisSet, 2)
# clusterPlot(analysisSet, codebook,0, 1,"0_1_analysis")

# print(whitened)
# print(codebook)

# clusterPlot(whitened, codebook,0, 1,"0_1_analysis")


