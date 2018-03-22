import morphologging
logger = morphologging.getLogger(__name__)

from IO import extractData, saveDictionaryIntoFile
from misc import plotASD, averageData
from plots import plot

from os import listdir
from os.path import isfile, join
import allantools
import numpy as np

pathToData = "../data"
pathToResults = "../results"
outputFile = "sgpmetavgE13.b1.20180101.000000.cdf"
listVOI = ["time","atmos_pressure", "qc_atmos_pressure", "rh_mean", "qc_rh_mean", "temp_mean", "qc_temp_mean"]
listVOIToAvg = [
    {"nameVar": "time","alias": "timeSinceBaseTime", "units": "seconds"},
    {"nameVar": "atmos_pressure","alias": "atmospheric_pressure", "units": "kPa"},
    {"nameVar": "rh_mean","alias": "relative_humidity", "units": "%"},
    {"nameVar": "temp_mean","alias": "mean_temperature", "units": "degC"}
]
NAverage = 50

##############################################################

onlyfiles = [join(pathToData,f) for f in sorted(listdir(pathToData)) if isfile(join(pathToData, f))]
# logger.info(onlyfiles)
dataset = None
for file in onlyfiles:
    dataset = extractData(file,listVOI,dataset)
    if isinstance(dataset[listVOI[0]],list):
        logger.debug("Length of data = {}".format(len(dataset[listVOI[0]])))

# checking that the data are doing all right
plot(dataset["qc_atmos_pressure"],dataset["time"],title="qc_atmos_pressure")
plot(dataset["qc_rh_mean"],dataset["time"],title="qc_rh_mean")
plot(dataset["qc_temp_mean"],dataset["time"],title="qc_temp_mean")

# plotting data
plot(dataset["atmos_pressure"],dataset["time"],title="atmos_pressure")
plot(dataset["rh_mean"],dataset["time"],title="rh_mean")
plot(dataset["temp_mean"],dataset["time"],title="temp_mean")

# use the time and timeoffset to build the time since begining of time
# timeSinceBaseTime = [dataset["time"][i]+dataset["time_offset"][i] for i in range(len(dataset["time"]))]
# dataset.update({"timeSinceBaseTime":timeSinceBaseTime})
# plot(dataset["base_time"],title = "base_time")
# plot(dataset["timeSinceBaseTime"],title = "timeSinceBaseTime")
plot(dataset["time"],title = "time")
# plot(dataset["time_offset"],title = "time_offset")

# Calculate the ASD to determine the best averaging period
plotASD(dataset["atmos_pressure"],"asd_atmos_pressure")
plotASD(dataset["rh_mean"],"asd_rh_mean")
plotASD(dataset["temp_mean"],"asd_temp_mean")

# Create new dictionary containing the avergaed data
avgDataset = {}
for item in listVOIToAvg:
    avgDataset.update({ str(item["nameVar"]): averageData(dataset[item["nameVar"]],NAverage)  })

# plotting averaged data
# plot()
plot(avgDataset["rh_mean"],avgDataset["time"],title="avg_rh_mean")
plot(avgDataset["temp_mean"],avgDataset["time"],title="avg_temp_mean")
plot(avgDataset["atmos_pressure"],avgDataset["time"],title="avg_atmos_pressure")

# Save Averaged data into file
saveDictionaryIntoFile(join(pathToResults,outputFile),avgDataset, varToSave=listVOIToAvg)

# Checking on one variable everything is fine
dataset = None
dataset = extractData(join(pathToResults,outputFile),["atmospheric_pressure"],dataset)
logger.debug("Length of data = {}".format(len(dataset["atmospheric_pressure"])))
logger.debug(dataset)

# print(parms)

