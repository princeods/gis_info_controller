import os
import glob
from pandas import *
from snowpipe import *
from tqdm import tqdm


# -----------------------------------------------------------------------------------

_pathSBLocation = "./space_bridge/"
_pathSBPartner = "./partner_SB/"

_dfTargetSB = pandas.DataFrame(index=range(0,0),columns = ["PrimaryKey", "name", "latitude", "longitude"])

# -----------------------------------------------------------------------------------

for _fileOriginSB in tqdm(glob.glob(_pathSBPartner+"*.csv")):

    for _fileTargetSB in tqdm(glob.glob(_pathSBLocation+"*.csv")):

        _dfOriginSB = pandas.read_csv(_fileTargetSB)

        for i in tqdm(range(int(len(_dfOriginSB)))):

            _dfOriginSB.loc[i,"latitude"]
            _dfOriginSB.loc[i,"longitude"]

        _sFilename = os.path.basename(_fileOriginSB)
        _sNameField = _sFilename[:2]

    _ltTarget = []