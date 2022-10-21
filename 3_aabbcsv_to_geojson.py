import os
import glob
import pandas
from tqdm import tqdm
import datetime

# -----------------------------------------------------------------------------------

def CreateFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ("Error: Creating directory. " +  directory)

# -----------------------------------------------------------------------------------

_pathLocation = "./aabb_origin/"
_pathToLocation = "./geojson/"

# check & generate folder ---------------------------------------------------------------------------------------

if os.path.isdir(_pathToLocation) != True:
    CreateFolder(_pathToLocation)

# generate geojson ----------------------------------------------------------------------------------------------

for _fileOriginCsvfile in tqdm(glob.glob(_pathLocation+"*.csv")):

    _sFilename = os.path.basename(_fileOriginCsvfile)
    _dfOrigin = pandas.read_csv(_fileOriginCsvfile)
    _ltTarget = []

    for i in tqdm(range(int(len(_dfOrigin)))):

        _sTemp = ""
        _sTemp = '{ "type": "Feature", "properties": { "name": "'
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "name"])
        _sTemp = _sTemp + '" }, "geometry": { "type": "Point", "coordinates": [ '
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "x"])
        _sTemp = _sTemp + ','
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "y"])
        _sTemp = _sTemp + '] } }'
        _sTemp = _sTemp + '\n'

        _ltTarget.append( _sTemp )

    with open(_pathToLocation + _sFilename.replace('.csv','.json'), 'w', encoding='utf-8') as f1:
        f1.writelines(_ltTarget)