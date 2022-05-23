import os
import glob
import pandas
from tqdm import tqdm

# -----------------------------------------------------------------------------------

def CreateFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ("Error: Creating directory. " +  directory)

# -----------------------------------------------------------------------------------

# _pathLocation = "./origin/"
_pathLocation = "./locationlog/"
_pathToLocation = "./locationgeojson/"

# check & generate folder ---------------------------------------------------------------------------------------

if os.path.isdir(_pathToLocation) != True:
    CreateFolder(_pathToLocation)

# generate geojson ----------------------------------------------------------------------------------------------

for _fileOriginCsvfile in tqdm(glob.glob(_pathLocation+"*.csv")):

    _sFilename = os.path.basename(_fileOriginCsvfile)
    _dfOrigin = pandas.read_csv(_fileOriginCsvfile)
    _ltTarget = []

    _affiliation = ""

    for i in tqdm(range(int(len(_dfOrigin)))):

        if str(_dfOrigin.loc[i, "affiliation"]) == "1":
            _affiliation = 'autobot'
        else:
            _affiliation ='decepticon'

        _sTemp = ""
        _sTemp = '{ "type": "Feature", "properties": { "name": "'
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "nickname"])
        _sTemp = _sTemp + '", "auid": "'
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "auid"])
        _sTemp = _sTemp + '", "affiliation": "'
        _sTemp = _sTemp + _affiliation        
        _sTemp = _sTemp + '", "token": "'
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "token"])
        _sTemp = _sTemp + '", "lv": "'
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "lv"])
        _sTemp = _sTemp + '", "regdatetime": "'
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "reg_date"])
        _sTemp = _sTemp + '", "스트리트 뷰" : "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=' + str(_dfOrigin.loc[i, "lat"]) \
             + '%2C' + str(_dfOrigin.loc[i, "lon"])
        _sTemp = _sTemp + '"}, "geometry": { "type": "Point", "coordinates": [ '
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "lon"])
        _sTemp = _sTemp + ','
        _sTemp = _sTemp + str(_dfOrigin.loc[i, "lat"])
        _sTemp = _sTemp + '] } }'
        _sTemp = _sTemp + '\n'

        _ltTarget.append( _sTemp )

    with open(_pathToLocation + _sFilename.replace('.csv','.json'), 'w', encoding='utf-8') as f1:
        f1.writelines(_ltTarget)