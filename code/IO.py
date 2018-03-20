import morphologging
logger = morphologging.getLogger(__name__)

import numpy as np
from netCDF4 import Dataset


def extractData(filename, variables, dataset=None, timeShift=True):
    '''
    Extract the data from a file and save them in a dictionary
    '''
    logger.info("Extracting data {} from file {}".format(variables,filename))
    file = Dataset(filename)
    if dataset == None:
        logger.info("No init dataset given; creating one")
        dataset = {}
    elif isinstance(dataset,dict):
        logger.info("Updating given dataset")
    else:
        logger.error("Given dataset is not a dict")
        return 
    for a_var in variables:
        a_data = dataset.get(str(a_var)) or []
        try:
            if timeShift and a_var=="time":
                base_time = file.variables["base_time"][:]
                a_data.extend([t+base_time for t in file.variables[str(a_var)][:].tolist()])
            else:
                a_data.extend(file.variables[str(a_var)][:].tolist())
        except AttributeError:
            a_data.extend([file.variables[str(a_var)][:]])
        dataset.update({str(a_var): a_data})
    return dataset

def saveDictionaryIntoFile(filename, data, varToSave=None, groupName = "data"):
    '''
    varToSave should be a dictionary of the variables to save with their name (nameVar) and alias (alias).
    I had to do some weird things, where I defined a new dictionary for the varToSave; otherwise it would modify the varToSave input dictionary
    TODO: add fields to set units, long_name...
    '''
    logger.info("Writing data to file {}".format(filename))
    f = Dataset(str(filename), 'w')
    obj = f.createGroup(str(groupName))
    if varToSave == None:
        varToSave_copy = []
        for a_varName in data.keys():
            varToSave.append({"nameVar": a_varName, "alias": a_varName})
    else:
        varToSave_copy = []
        # varToSave_copy.extend(varToSave.copy())
    # varToSave = None

    logger.debug("Adding variables to the data dictionary")
    for item in varToSave:
        logger.debug(item["nameVar"])
        newItem = {
            "nameVar": item["nameVar"],
            "dimensions": f.createDimension(item["alias"], None),
            "variableObj": f.createVariable(item["alias"], np.float32, (item["alias"],))
            }
        newItem["variableObj"].units = item.get("units")
        varToSave_copy.append(newItem)

    logger.debug("Saving data")
    for item in varToSave_copy:
        item["variableObj"][:] = data[item["nameVar"]]
        # print(item["variableObj"][:])

    logger.debug("Closing file")
    f.close()


if __name__=="main":
    logger.info("Results: {}".format(extractData("../data/sgpmetE13.b1.20180101.000000.cdf",["atmos_pressure","time"])))


