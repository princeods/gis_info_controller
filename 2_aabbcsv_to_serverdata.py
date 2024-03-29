from cmath import isnan
import os
import glob
import math
import random
import re
import pandas
from tqdm import tqdm
import datetime
from enum import Enum
import randy
import numpy
from snowpipe import *

# -----------------------------------------------------------------------------------

_pathLocation = "./aabb/"
_pathToSBLocation = "./space_bridge/"
_pathToNameLocation = "./space_bridge_name/"
_pathToHQLocation = "./space_bridge_hq/"
_pathToSquadLocation = "./space_bridge_squad/"
_fileSeed = "./seed.xlsm"

# -----------------------------------------------------------------------------------

_tStartTime = datetime.datetime.now()

_dMaxNameLenth = 20
_dSBLod = 65536     # 스페이스 브리지 영역 구분을 위한 기준 레벨
_dSBLv3Gap = 8      # Lv. 3 스페이스 브리지 간격
_dSBLv4Gap = 25     # Lv. 1 스페이스 브리지 간격

_sNoName = "NO NAME"

_wsTransformers = "transformers"
_wsCubeSocket = "cubesocket"

# create Structure Level list -----------------------------------------------------------------------------------

_liBaseLv = [ [ 1, 2, 3, 4, 5,  6 ],
              [ 3, 4, 5, 6, 7,  8 ],
              [ 5, 6, 7, 8, 9, 10 ],
              [ 5, 6, 7, 8, 9, 10 ] ]

_liBaseFactor = [ [ 2, 2, 2, 1, 1,  1 ],
                  [ 2, 2, 2, 1, 1,  1 ],
                  [ 2, 2, 2, 1, 1,  1 ],
                  [ 1, 1, 1, 5, 7, 10 ] ]

_liFortressLv = [ [ 1, 2, 3, 4, 5,  6 ],
                  [ 3, 4, 5, 6, 7,  8 ],
                  [ 5, 6, 7, 8, 9, 10 ],
                  [ 5, 6, 7, 8, 9, 10 ] ]

_liFortressFactor = [ [ 1, 1, 0, 0, 0,  0 ],
                      [ 2, 2, 2, 1, 1,  1 ],
                      [ 2, 2, 2, 1, 1,  1 ],
                      [ 1, 1, 1, 5, 7, 10 ] ]

_liLabLv = [ [ 1, 2, 3, 4, 5,  6 ],
             [ 3, 4, 5, 6, 7,  8 ],
             [ 5, 6, 7, 8, 9, 10 ],
             [ 5, 6, 7, 8, 9, 10 ] ]

_liLabFactor = [ [ 2, 2, 2, 1, 1,  1 ],
                 [ 2, 2, 2, 1, 1,  1 ],
                 [ 2, 2, 2, 1, 1,  1 ],
                 [ 1, 1, 1, 5, 7, 10 ] ]

_liWarehouseLv = [ [ 1, 2, 3, 4, 5,  6 ],
                   [ 3, 4, 5, 6, 7,  8 ],
                   [ 5, 6, 7, 8, 9, 10 ],
                   [ 5, 6, 7, 8, 9, 10 ] ]

_liWarehouseFactor = [ [ 6, 5, 4, 3, 2, 1 ],
                       [ 6, 5, 4, 3, 2, 1 ],
                       [ 6, 5, 4, 3, 2, 1 ],
                       [ 1, 1, 1, 1, 1, 1 ] ]

_liWorkshopLv = [ [ 1, 2, 3, 4, 5,  6 ],
                  [ 3, 4, 5, 6, 7,  8 ],
                  [ 5, 6, 7, 8, 9, 10 ],
                  [ 5, 6, 7, 8, 9, 10 ] ]

_liWorkshopFactor = [ [ 2, 2, 2, 1, 1,  1 ],
                      [ 2, 2, 2, 1, 1,  1 ],
                      [ 2, 2, 2, 1, 1,  1 ],
                      [ 1, 1, 1, 5, 7, 10 ] ]

_liEventTime =       [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1]
_liEventTimeFactor = [1, 2, 2, 1,  1,  4,  4,  3,  2,  2,  2,  2,  3,  4,  5,  5,  5,  4, 3, 1]

# -----------------------------------------------------------------------------------

_dicCountryCode = {"ko":"1", "jp":"2", "ch":"3", "tw":"4", "us":"5", "ru":"6", "de":"7", "as":"e", "te":"f"}
_dfSeedTFSS = pandas.read_excel(_fileSeed, _wsTransformers + "_SS", engine='openpyxl')
_dfSeedTFS = pandas.read_excel(_fileSeed, _wsTransformers + "_S", engine='openpyxl')
_dfSeedTFA = pandas.read_excel(_fileSeed, _wsTransformers + "_A", engine='openpyxl')
_dfSeedTFB = pandas.read_excel(_fileSeed, _wsTransformers + "_B", engine='openpyxl')
_dfSeedTFC = pandas.read_excel(_fileSeed, _wsTransformers + "_C", engine='openpyxl')
_dfCubeSocket = pandas.read_excel(_fileSeed, _wsCubeSocket, engine='openpyxl')

#_dSeedTFCount = len(_dfSeedTF)
_dSeedCubeSocketCount = len(_dfCubeSocket) - 1

# -----------------------------------------------------------------------------------

class SBLevel:
    Lv1 = 1
    Lv2 = 2
    Lv3 = 3
    Lv4 = 4

# -----------------------------------------------------------------------------------

# def CreateFolder(directory):
#     try:
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#     except OSError:
#         print ("Error: Creating directory. " +  directory)

# -----------------------------------------------------------------------------------

typeGeData = str(input("생성할 데이터 선택 ( A : 모든 데이터, N : 이름, S : 스페이스 브리지, SQ : 스쿼드, HQ : 건물 ) : "))
typeLevelData = int(input("생성 방식 선택 ( 0 ( 기본 ) : 일반, 1 ~ 3 : 모든 브리지 레벨을 입력한 값으로 ): "))

# -----------------------------------------------------------------------------------

print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )
print( f"서버 데이터 생성 시작.")
print( f"작업 시작 시간 : {_tStartTime}" )
print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )

# check & generate folder ---------------------------------------------------------------------------------------

if os.path.isdir(_pathToSBLocation) != True and ( typeGeData.upper() == "A" or typeGeData.upper() == "S" ):
    CreateFolder(_pathToSBLocation)
if os.path.isdir(_pathToNameLocation) != True and ( typeGeData.upper() == "A" or typeGeData.upper() == "N" ):
    CreateFolder(_pathToNameLocation)
if os.path.isdir(_pathToHQLocation) != True and ( typeGeData.upper() == "A" or typeGeData.upper() == "HQ" ):
    CreateFolder(_pathToHQLocation)
if os.path.isdir(_pathToSquadLocation) != True and ( typeGeData.upper() == "A" or typeGeData.upper() == "SQ" ):
    CreateFolder(_pathToSquadLocation)    

# generate server data ( csv )-----------------------------------------------------------------------------------

for _fileOriginCsvfile in glob.glob(_pathLocation+"*.csv"):
    
    _sFilename = os.path.basename(_fileOriginCsvfile)
    _sNameField = _sFilename[:2]
    _sCountryCode = _dicCountryCode[_sNameField]
    _sFileNum = Dec2Hex( int( _sFilename[_sFilename.rindex("_")+1:].replace(".csv","") ), 2 )

    _dfOrigin = pandas.DataFrame(index=range(0,0),columns = ["osm_id", "name", "x", "y"])
    _dfSBFile = pandas.DataFrame(index=range(0,0),columns = ["PrimaryKey", "level", "latitude", "longitude", "cubeSocketKey", "indexTile", \
        "weekEvent00", "timeEvent00", "minuteEvent00", "weekEvent01", "timeEvent01", "minuteEvent01", \
            "spacebridgepoint", "buildingLevelInfo" ]) #"HQBaseLevel", "HQFortressLevel", "HQLabLevel", "HQWarehouseLevel", "HQExhibitionLevel", "HQWorkshopLevel"])
    _dfNameFile = pandas.DataFrame(index=range(0,0),columns = ["PrimaryKey", _sNameField])
    _dfHQFile = pandas.DataFrame(index=range(0,0),columns = ["auid", "hq_type", "owner", "lv", "state"])
    _dfSquadFile = pandas.DataFrame(index=range(0,0),columns = ["PrimaryKey", "squad_type", "transformers_1", "transformers_2", "transformers_3"])

    _dfOrigin = pandas.read_csv(_fileOriginCsvfile)

    for i in tqdm(range(int(len(_dfOrigin)))):

        # generate primary key -----------------------------------------------------------------------------------
        # 브리지 레벨 ( 1 ) + 국가 코드 ( 1 ) + 파일 넘버 ( 2 ) + 인덱스 ( 4 )

        _sTempName = (_dfOrigin.loc[i, "name"])

        if ( typeLevelData != 0 ):
            _sSBLevel = typeLevelData
        else:
            if _sTempName == "" or _dfOrigin.isnull().loc[i, "name"] or "," in _sTempName or \
                "\n" in _sTempName or "\t" in _sTempName or "\"" in _sTempName or  "\'" in _sTempName or \
                    "\r" in _sTempName:
                _sSBLevel = 1
            else:
                if (i / _dSBLv3Gap) == int(i / _dSBLv3Gap):
                    _sSBLevel = 3
                elif (i / _dSBLv4Gap) == int(i / _dSBLv4Gap):
                    _sSBLevel = 1
                else:
                    _sSBLevel = 2

        _xPrimaryKey = _sCountryCode + Dec2Hex(_sSBLevel, 1) + _sFileNum + Dec2Hex(i, 4)

        # name dataframe append -----------------------------------------------------------------------------------

        if typeGeData.upper() == "A" or typeGeData.upper() == "N":
            
            _dfNameFile.loc[i, "PrimaryKey"] = int( _xPrimaryKey, 16 )

            if _sSBLevel == 1:
                _dfNameFile.loc[i, _sNameField] = _sNoName
            else:
                if len( _sTempName ) > _dMaxNameLenth:
                    _dfNameFile.loc[i, _sNameField] = _sTempName[:_dMaxNameLenth] + "...."
                else:
                    _dfNameFile.loc[i, _sNameField] = _sTempName

        # HQ building level generate ------------------------------------------------------------------------------

        _dTempHQBaseLevel = 0
        _dTempHQFortressLevel = 0
        _dTempHQLabLevel = 0
        _dTempHQWarehouseLevel = 0
        _dTempHQExhibitionLevel = 0
        _dTempHQWorkshopLevel = 0

        for j in range(0,6):
            if j == 0:    # 본부
                _dTempHQBaseLevel = random.choices(_liBaseLv[_sSBLevel-1], _liBaseFactor[_sSBLevel-1])[0]
            elif j == 1:    # 요새
                _dTempHQFortressLevel = random.choices(_liFortressLv[_sSBLevel-1], _liFortressFactor[_sSBLevel-1])[0]
            elif j == 2:    # 연구소
                _dTempHQLabLevel = random.choices(_liLabLv[_sSBLevel-1], _liLabFactor[_sSBLevel-1])[0]
            elif j == 3:    # 창고
                _dTempHQWarehouseLevel = random.choices(_liWarehouseLv[_sSBLevel-1], _liWarehouseFactor[_sSBLevel-1])[0]
            elif j == 4:    # 전시관
                _dTempHQExhibitionLevel = 1
            elif j == 5:    # 파츠 제작소
                _dTempHQWorkshopLevel = random.choices(_liWorkshopLv[_sSBLevel-1], _liWorkshopFactor[_sSBLevel-1])[0]

        # spacebridge dataframe append ----------------------------------------------------------------------------

        if typeGeData.upper() == "A" or typeGeData.upper() == "S":
            
            _dfSBFile.loc[i, "PrimaryKey"] = int( _xPrimaryKey, 16 )
            _dfSBFile.loc[i, "level"] = _sSBLevel
            _dfSBFile.loc[i, "latitude"] = _dfOrigin.loc[i, "y"]
            _dfSBFile.loc[i, "longitude"] = _dfOrigin.loc[i, "x"]
            _dfSBFile.loc[i, "cubeSocketKey"] = int( _dfCubeSocket.loc[random.randint(0,_dSeedCubeSocketCount), "PrimaryKey"], 16 )

            _dTempX = int( _dSBLod * ( ( _dfOrigin.loc[i, "x"] + 180 ) / 360 ) )

            _fTempY_1 = math.tan( math.radians( _dfOrigin.loc[i, "y"] ) ) + ( 1 / math.cos( math.radians( _dfOrigin.loc[i, "y"] ) ) )
            _fTempY_2 = 1 - ( math.log( _fTempY_1 ) / math.pi )
            _dTempY = int( _dSBLod * _fTempY_2 / 2 )

            _dIndexTile = _dTempX + ( _dTempY * _dSBLod )
            _dfSBFile.loc[i, "indexTile"] = _dIndexTile

            # sb 레벨 별 메인 이벤트가 24 로 동작할 비율 지정.
            # 지정된 비율 외의 것은 

            _fRatioMainEvent = 0

            if SBLevel.Lv1 == _sSBLevel:
                _fRatioMainEvent = 0.05
                _dfSBFile.loc[i, "spacebridgepoint"] = 10
            elif SBLevel.Lv2 == _sSBLevel:
                _fRatioMainEvent = 0.1
                _dfSBFile.loc[i, "spacebridgepoint"] = 20
            elif SBLevel.Lv3 == _sSBLevel:
                _fRatioMainEvent = 1.0
                _dfSBFile.loc[i, "spacebridgepoint"] = 30
            elif SBLevel.Lv4 == _sSBLevel:
                _fRatioMainEvent = 1.0
                _dfSBFile.loc[i, "spacebridgepoint"] = 40

            _dfSBFile.loc[i, "weekEvent00"] = "1111111"

            if random.random() <= _fRatioMainEvent:
                _dfSBFile.loc[i, "timeEvent00"] = 24
                _dfSBFile.loc[i, "minuteEvent00"] = random.randint(0,59)
            else:
                # 1 차 이벤트 중 24 시간이 아닌 경우, 가중치를 적용해서 동접 많은 시간에 많이 나오게..                
                _dfSBFile.loc[i, "timeEvent00"] = _hhMainEventTime = random.choices(_liEventTime, _liEventTimeFactor)[0]
                if _hhMainEventTime == 1:
                    _dfSBFile.loc[i, "minuteEvent01"] = random.randint(0,29)
                else:
                    _dfSBFile.loc[i, "minuteEvent01"] = random.randint(0,59)

            if random.random() <= 0.5:
                # 50% 는 2 차 이벤트 발생
                # 2 차 이벤트는 고르게 - 무작위로..
                _dfSBFile.loc[i, "weekEvent01"] = "1111111"
                _hhMainEventTime = random.randint(6,25) % 24
                _dfSBFile.loc[i, "timeEvent01"] = _hhMainEventTime
                if _hhMainEventTime == 1:
                    _dfSBFile.loc[i, "minuteEvent01"] = random.randint(0,29)
                else:
                    _dfSBFile.loc[i, "minuteEvent01"] = random.randint(0,59)
            else:
                _dfSBFile.loc[i, "weekEvent01"] = "0000000"
                _dfSBFile.loc[i, "timeEvent01"] = 0
                _dfSBFile.loc[i, "minuteEvent01"] = 0

            _sBuildingInfo = Dec2Hex(_dTempHQWorkshopLevel, 1) + Dec2Hex(_dTempHQExhibitionLevel, 1) + \
                Dec2Hex(_dTempHQWarehouseLevel, 1) + Dec2Hex(_dTempHQLabLevel, 1) + Dec2Hex(_dTempHQFortressLevel, 1) + Dec2Hex(_dTempHQBaseLevel, 1)

            _dfSBFile.loc[i, "buildingLevelInfo"] = _sBuildingInfo

        # hq dataframe append -------------------------------------------------------------------------------------

        if typeGeData.upper() == "A" or typeGeData.upper() == "HQ":

            for j in range(0,6):
                _dfHQFile.loc[i * 6 + j, "auid"] = int( _xPrimaryKey, 16 )
                _dfHQFile.loc[i * 6 + j, "hq_type"] = j

                if j == 0:      # 본부
                    _dfHQFile.loc[i * 6 + j, "lv"] = _dTempHQBaseLevel
                elif j == 1:    # 요새
                    _dfHQFile.loc[i * 6 + j, "lv"] = _dTempHQFortressLevel
                elif j == 2:    # 연구소
                    _dfHQFile.loc[i * 6 + j, "lv"] = _dTempHQLabLevel
                elif j == 3:    # 에너존 창고
                    _dfHQFile.loc[i * 6 + j, "lv"] = _dTempHQWarehouseLevel
                elif j == 4:    # 전시관
                    _dfHQFile.loc[i * 6 + j, "lv"] = _dTempHQExhibitionLevel
                elif j == 5:    # 파츠 제작소
                    _dfHQFile.loc[i * 6 + j, "lv"] = _dTempHQWorkshopLevel

                _dfHQFile.loc[i * 6 + j, "owner"] = 2
                _dfHQFile.loc[i * 6 + j, "state"] = 0

        # squad dataframe append ----------------------------------------------------------------------------------

        if typeGeData.upper() == "A" or typeGeData.upper() == "SQ":

            _dfSquadFile.loc[i, "PrimaryKey"] = 0
            _dfSquadFile.loc[i, "squad_type"] = int( _xPrimaryKey, 16 )

            _ltTF = []
            _dDefenceTFCount = 0
            _dTempTFLevel = 0
            
            # 브리지 레벨에 따라, 방어 스쿼드 후보군을 리스트로 만들고

            if _sSBLevel == SBLevel.Lv4:
                _ltTF = [ _dfSeedTFS['StandardCode'].values.tolist() + _dfSeedTFSS['StandardCode'].values.tolist(), \
                          _dfSeedTFS['rankup'].values.tolist() + _dfSeedTFSS['rankup'].values.tolist() ]
            elif _sSBLevel == SBLevel.Lv3:
                _ltTF = [ _dfSeedTFA['StandardCode'].values.tolist() + _dfSeedTFS['StandardCode'].values.tolist() + _dfSeedTFSS['StandardCode'].values.tolist(), \
                          _dfSeedTFA['rankup'].values.tolist() + _dfSeedTFS['rankup'].values.tolist() + _dfSeedTFSS['rankup'].values.tolist() ]
            elif _sSBLevel == SBLevel.Lv2:
                _ltTF = [ _dfSeedTFB['StandardCode'].values.tolist() + _dfSeedTFA['StandardCode'].values.tolist() + _dfSeedTFS['StandardCode'].values.tolist(), \
                          _dfSeedTFB['rankup'].values.tolist() + _dfSeedTFA['rankup'].values.tolist() + _dfSeedTFS['rankup'].values.tolist() ]
            elif _sSBLevel == SBLevel.Lv1:
                _ltTF = [ _dfSeedTFC['StandardCode'].values.tolist() + _dfSeedTFB['StandardCode'].values.tolist(), \
                          _dfSeedTFC['rankup'].values.tolist() + _dfSeedTFB['rankup'].values.tolist() ]

            # 요새 레벨에 따라, 스쿼드 구성 수량 지정.

            if _dTempHQFortressLevel < 3:
                _dDefenceTFCount = 1
            elif _dTempHQFortressLevel > 5:
                _dDefenceTFCount = 3
            else:
                _dDefenceTFCount = 2

            # 브리지 레벨에 따라 방어 스쿼드의 레벨을 지정하고
            # 지정된 스쿼드 리스트에서 수량만큼 중복되지 않게 common id 픽.
            # 레벨과 common id 를 조합해서 방어 스쿼드 완성.

            for k in range(1,4):

                #range(1,_dDefenceTFCount + 1):
                if ( k <= _dDefenceTFCount ):
                    _dTempTFLevel = 0
                    
                    if _sSBLevel == SBLevel.Lv4:
                        _dTempTFLevel = random.randint(16,20)
                    elif _sSBLevel == SBLevel.Lv3:
                        _dTempTFLevel = random.randint(10,17)
                    elif _sSBLevel == SBLevel.Lv2:
                        _dTempTFLevel = random.randint(4,11)
                    elif _sSBLevel == SBLevel.Lv1:
                        _dTempTFLevel = random.randint(2,5)

                    _sTempTFIndex = random.randint( 0, len(_ltTF[0]) - 2 )
                    _sTempTFStandardCode = str(_ltTF[0][_sTempTFIndex])
                    _sTempTFIsRankup =  _ltTF[1][_sTempTFIndex]

                    _sTFPrimaryKey = "01" + _sTempTFStandardCode + Dec2Hex(_dTempTFLevel + ( 0 if numpy.isnan(_sTempTFIsRankup)  else 20 ), 3)
                    _dfSquadFile.loc[i, "transformers_" + str(k) ] = int( _sTFPrimaryKey, 16 )
                    _ltTF[0].pop(_sTempTFIndex)
                    _ltTF[1].pop(_sTempTFIndex)
                else:
                    _dfSquadFile.loc[i, "transformers_" + str(k) ] = 0

    # csv export --------------------------------------------------------------------------------------------------

    if typeGeData.upper() == "A" or typeGeData.upper() == "S":
        _dfSBFile.to_csv( _pathToSBLocation + _sFilename, sep=",", index = False, encoding = "utf-8-sig" , line_terminator = "\r\n", float_format = "%.10f" )
    if typeGeData.upper() == "A" or typeGeData.upper() == "N":
        _dfNameFile.to_csv( _pathToNameLocation + _sFilename, sep=",", index = False, encoding = "utf-8-sig" , line_terminator = "\r\n", float_format = "%.10f" )
    if typeGeData.upper() == "A" or typeGeData.upper() == "HQ":
        _dfHQFile.to_csv( _pathToHQLocation + _sFilename, sep=",", index = False, encoding = "utf-8-sig" , line_terminator = "\r\n", float_format = "%.10f" )
    if typeGeData.upper() == "A" or typeGeData.upper() == "SQ":
        _dfSquadFile.to_csv( _pathToSquadLocation + _sFilename, sep=",", index = False, encoding = "utf-8-sig" , line_terminator = "\r\n", float_format = "%.10f" )

print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )
print( f"{_sFilename[:2]} 지역에서 스페이스 브리지 데이터 생성 완료." )
print( f"작업 완료 소요 시간 : {datetime.datetime.now() - _tStartTime}" )
print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )