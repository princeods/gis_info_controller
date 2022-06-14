import os
import glob
import pandas
from snowpipe import *
from tqdm import tqdm
import openpyxl

# -----------------------------------------------------------------------------------

_pathSBLocation = "./space_bridge/"
_pathNameLocation = "./space_bridge_name/"
_pathHQLocation = "./space_bridge_hq/"
_pathSquadLocation = "./space_bridge_squad/"
_pathToLocation = "./sbgeojson/"

_pathSeed = "./"
_fileSeed = "seed.xlsm"

_wsTransformers = "transformers_Origin"

_dfSeedTF = pandas.read_excel(_pathSeed + _fileSeed, _wsTransformers, engine='openpyxl')

# check & generate folder ---------------------------------------------------------------------------------------

if os.path.isdir(_pathToLocation) != True:
    CreateFolder(_pathToLocation)

# generate geojson ----------------------------------------------------------------------------------------------

for _fileOriginCsvfile in tqdm(glob.glob(_pathSBLocation+"*.csv")):

    _sFilename = os.path.basename(_fileOriginCsvfile)
    _sNameField = _sFilename[:2]

    _dfSB = pandas.read_csv(_fileOriginCsvfile)
    _dfName = pandas.read_csv(_pathNameLocation + _sFilename)
    _dfHQ = pandas.read_csv(_pathHQLocation + _sFilename)
    _dfSquad = pandas.read_csv(_pathSquadLocation + _sFilename)

    _ltTarget = []

    # { "type": "Feature", "properties": { "name": "이름", "level": "레벨" }, "geometry": { "type": "Point", "coordinates": [ xx.xxx, yy.yyy ] } }

    for i in tqdm(range(int(len(_dfSB)))):

        _sTemp = ""
        _sTemp = '{ "type": "Feature", "properties": { "기본 키": "'
        _sTemp = _sTemp + str(_dfSB.loc[i, "PrimaryKey"])
        _sTemp = _sTemp + '", "이름": "'
        _sTemp = _sTemp + str(_dfName.loc[i, _sNameField])
        _sTemp = _sTemp + '", "레벨": '
        _sTemp = _sTemp + str(_dfSB.loc[i, "level"])
        _sTemp = _sTemp + ', '

        for j in range(0,6):
            _sTemp = _sTemp + '"'
            _sTemp = _sTemp + HQTypeName(_dfHQ.loc[i * 6 + j, "hq_type"])
            _sTemp = _sTemp + '": '
            _sTemp = _sTemp + str(_dfHQ.loc[i * 6 + j, "lv"])
            _sTemp = _sTemp + ', '

        for j in range(0,3):
            temp = Dec2Hex(_dfSquad.loc[i, "transformers_" + str( j + 1 )], 8)[2:5]

            if temp != "000":
                tempLevel = Dec2Hex(_dfSquad.loc[i, "transformers_" + str( j + 1 )], 8)[7:8]
                tempIndex = _dfSeedTF.index[_dfSeedTF['StandardCode'] == temp].tolist()
                tempName = _dfSeedTF.loc[tempIndex[0], "Name"]

                _sTemp = _sTemp + '"배치(' + str(j) + ')" : "'
                _sTemp = _sTemp + str(tempName)
                _sTemp = _sTemp + '('
                _sTemp = _sTemp + str(int(tempLevel, 16))
                _sTemp = _sTemp + ')", '

        # https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=37.464732%2C127.043236

        _sTemp = _sTemp + '"스트리트 뷰" : "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=' + str(_dfSB.loc[i, "latitude"]) + '%2C' + str(_dfSB.loc[i, "longitude"])

        _sTemp = _sTemp + '" }, "geometry": { "type": "Point", "coordinates": [ '
        _sTemp = _sTemp + str(_dfSB.loc[i, "longitude"])
        _sTemp = _sTemp + ', '
        _sTemp = _sTemp + str(_dfSB.loc[i, "latitude"])
        _sTemp = _sTemp + ' ] } }'
        _sTemp = _sTemp + '\n'

        _ltTarget.append( _sTemp )

    with open(_pathToLocation + _sFilename.replace('.csv','.json'), 'w', encoding='utf-8') as f1:
        f1.writelines(_ltTarget)