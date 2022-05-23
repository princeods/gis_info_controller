import os
import glob
import math
import random
import re
import pandas
from tqdm import tqdm
import datetime


# -----------------------------------------------------------------------------------

_pathLocation = "./aabb/"
_pathToSBLocation = "./space_bridge/"
_pathToNameLocation = "./space_bridge_name/"
_pathToHQLocation = "./space_bridge_hq/"
_pathToSquadLocation = "./space_bridge_squad/"
_pathSeed = "./"
_fileSeed = "seed.xlsm"

# -----------------------------------------------------------------------------------

_tStartTime = datetime.datetime.now()

_dMaxNameLenth = 20
_dSBLod = 65536     # 스페이스 브리지 영역 구분을 위한 기준 레벨
_dSBLv3Gap = 500    # Lv. 3 스페이스 브리지 간격
_dSBLv3Count = 0

_sNoName = "NO NAME"

_wsTransformers = "transformers"
_wsCubeSocket = "cubesocket"

# create Structure Level list -----------------------------------------------------------------------------------

_liLv1StructureNor = []
_liLv2StructureNor = []
_liLv3StructureNor = []
_liLv1StructureLab = []
_liLv2StructureLab = []
_liLv3StructureLab = []

# for i in range(1,7):
#     for j in reversed(range(1,pow(2,6-i)+1)):
#         _liLv1StructureNor.append(i)
#         _liLv2StructureNor.append(i+3)

# for i in range(1,7):
#     for j in reversed(range(1,pow(2,6-i)+1)):
#         _liLv3StructureNor.append(i+3)

for i in range(1,7):
    for j in reversed(range(1,int(pow(1.3,6-i)+1))):
        _liLv1StructureNor.append(i)
        _liLv2StructureNor.append(i+2)
        _liLv3StructureNor.append(i+4)

_liLv1StructureLab = [1]
_liLv2StructureLab = [1, 1, 2]
_liLv3StructureLab = [1, 1, 1, 1, 2, 2, 3]

# -----------------------------------------------------------------------------------

_dicCountryCode = {"ko":"1", "jp":"2", "ch":"3", "tw":"4", "us":"5", "ru":"6", "de":"7", "as":"e", "te":"f"}
_dfSeedTF = pandas.read_excel(_pathSeed + _fileSeed, _wsTransformers)
_dfCubeSocket = pandas.read_excel(_pathSeed + _fileSeed, _wsCubeSocket)

_dSeedTFCount = len(_dfSeedTF)
_dSeedCubeSocketCount = len(_dfCubeSocket) - 1

# -----------------------------------------------------------------------------------

def Dec2Hex(_dValue,_dDigit):
    _sTemp = format(_dValue,"X")
    for i in range(_dDigit - len(_sTemp)):
        _sTemp = "0" + _sTemp
    return _sTemp

# -----------------------------------------------------------------------------------

def CreateFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ("Error: Creating directory. " +  directory)

# -----------------------------------------------------------------------------------

typeGeData = str(input("생성할 데이터 선택 ( A : 모든 데이터, N : 이름, S : 스페이스 브리지, SQ : 스쿼드, HQ : 건물 ) : "))

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

        _sTempName = (_dfOrigin.loc[i, "name"])

        if _sTempName == "" or _dfOrigin.isnull().loc[i, "name"] or "," in _sTempName or \
            "\n" in _sTempName or "\t" in _sTempName or "\"" in _sTempName or  "\'" in _sTempName or \
                "\r" in _sTempName:
            _sSBLevel = Dec2Hex(1, 1)
        else:
            #if (_dSBLv3Count / _dSBLv3Gap) == int(_dSBLv3Count / _dSBLv3Gap):
            if "학교" in _sTempName:
                _sSBLevel = Dec2Hex(3, 1)
            else:
                _sSBLevel = Dec2Hex(2, 1)

        _dSBLv3Count += 1
        _xPrimaryKey = _sSBLevel + _sCountryCode + _sFileNum + Dec2Hex(i, 4)

        # name dataframe append -----------------------------------------------------------------------------------

        if typeGeData.upper() == "A" or typeGeData.upper() == "N":
            
            _dfNameFile.loc[i, "PrimaryKey"] = int( _xPrimaryKey, 16 )

            if int( "0x" + _sSBLevel, 16 ) == 1:
                _dfNameFile.loc[i, _sNameField] = _sNoName
            else:
                if len( _sTempName ) > _dMaxNameLenth:
                    _dfNameFile.loc[i, _sNameField] = _sTempName[:_dMaxNameLenth] + "...."
                else:
                    _dfNameFile.loc[i, _sNameField] = _sTempName

        # HQ building level generate ------------------------------------------------------------------------------

        _arHQ = []

        for j in range(0,6):
            if j == 0:    # 본부
                if _sSBLevel == "1":
                    _dTempHQBaseLevel = random.choice(_liLv1StructureNor)
                elif _sSBLevel == "2":
                    _dTempHQBaseLevel = random.choice(_liLv2StructureNor)
                elif _sSBLevel == "3":
                    _dTempHQBaseLevel = random.choice(_liLv3StructureNor)
            elif j == 1:    # 요새
                if _sSBLevel == "1":
                    _dTempHQFortressLevel = random.choice(_liLv1StructureNor)
                elif _sSBLevel == "2":
                    _dTempHQFortressLevel = random.choice(_liLv2StructureNor)
                elif _sSBLevel == "3":
                    _dTempHQFortressLevel = random.choice(_liLv3StructureNor)
            elif j == 2:    # 연구소
                if _sSBLevel == "1":
                    _dTempHQLabLevel = random.choice(_liLv1StructureLab)
                elif _sSBLevel == "2":
                    _dTempHQLabLevel = random.choice(_liLv2StructureLab)
                elif _sSBLevel == "3":
                    _dTempHQLabLevel = random.choice(_liLv3StructureLab)
            elif j == 3:    # 창고
                if _sSBLevel == "1":
                    _dTempHQWarehouseLevel = random.choice(_liLv1StructureNor)
                elif _sSBLevel == "2":
                    _dTempHQWarehouseLevel = random.choice(_liLv2StructureNor)
                elif _sSBLevel == "3":
                    _dTempHQWarehouseLevel = random.choice(_liLv3StructureNor)
            elif j == 4:    # 전시관
                _dTempHQExhibitionLevel = 1
            elif j == 5:    # 파츠 제작소
                if _sSBLevel == "1":
                    _dTempHQWorkshopLevel = random.choice(_liLv1StructureNor)
                elif _sSBLevel == "2":
                    _dTempHQWorkshopLevel = random.choice(_liLv2StructureNor)
                elif _sSBLevel == "3":
                    _dTempHQWorkshopLevel = random.choice(_liLv3StructureNor)


        # spacebridge dataframe append ----------------------------------------------------------------------------

        if typeGeData.upper() == "A" or typeGeData.upper() == "S":
            
            _dfSBFile.loc[i, "PrimaryKey"] = int( _xPrimaryKey, 16 )
            _dfSBFile.loc[i, "level"] = int( _sSBLevel )
            _dfSBFile.loc[i, "latitude"] = _dfOrigin.loc[i, "y"]
            _dfSBFile.loc[i, "longitude"] = _dfOrigin.loc[i, "x"]
            _dfSBFile.loc[i, "cubeSocketKey"] = int( _dfCubeSocket.loc[random.randint(0,_dSeedCubeSocketCount), "PrimaryKey"], 16 )

            _dTempX = int( _dSBLod * ( ( _dfOrigin.loc[i, "x"] + 180 ) / 360 ) )

            _fTempY_1 = math.tan( math.radians( _dfOrigin.loc[i, "y"] ) ) + ( 1 / math.cos( math.radians( _dfOrigin.loc[i, "y"] ) ) )
            _fTempY_2 = 1 - ( math.log( _fTempY_1 ) / math.pi )
            _dTempY = int( _dSBLod * _fTempY_2 / 2 )

            _dIndexTile = _dTempX + ( _dTempY * _dSBLod )
            _dfSBFile.loc[i, "indexTile"] = _dIndexTile

            _dfSBFile.loc[i, "weekEvent00"] = "1111111"

            if random.random() <= 0.9:
                # 90% 는 6 ~ 24 % 24 중 랜덤하게 이벤트 발생
                # 분은 0 ~ 59 랜덤으로
                # 분은 0 ~ 29 랜덤으로 - 서버에서 동일 시간 이벤트 검색만을 하기 위한 처리
                _dfSBFile.loc[i, "timeEvent00"] = random.randint(6,24) % 24
                _dfSBFile.loc[i, "minuteEvent00"] = random.randint(0,59)
            else:
                # 나머지 10 % 는 24 시간 발생하는 24 로..
                _dfSBFile.loc[i, "timeEvent00"] = 24
                _dfSBFile.loc[i, "minuteEvent00"] = random.randint(0,59)

            if random.random() <= 0.5:
                # 50% 는 2 차 이벤트 발생
                _dfSBFile.loc[i, "weekEvent01"] = "1111111"
                _dfSBFile.loc[i, "timeEvent01"] = random.randint(6,25) % 24
                _dfSBFile.loc[i, "minuteEvent01"] = random.randint(0,59)
            else:
                _dfSBFile.loc[i, "weekEvent01"] = "0000000"
                _dfSBFile.loc[i, "timeEvent01"] = 0
                _dfSBFile.loc[i, "minuteEvent01"] = 0

            if int( _sSBLevel ) == 3:
                _dfSBFile.loc[i, "spacebridgepoint"] = 100
            elif int( _sSBLevel ) == 2:
                _dfSBFile.loc[i, "spacebridgepoint"] = 50
            elif int ( _sSBLevel ) == 1:
                _dfSBFile.loc[i, "spacebridgepoint"] = 25

            # print ( f"_dTempHQWorkshopLevel : {_dTempHQWorkshopLevel}" )
            # print ( f"_dTempHQExhibitionLevel : {_dTempHQExhibitionLevel}" ) 
            # print ( f"_dTempHQWarehouseLevel : {_dTempHQWarehouseLevel}" )
            # print ( f"_dTempHQLabLevel : {_dTempHQLabLevel}" )
            # print ( f"_dTempHQFortressLevel : {_dTempHQFortressLevel}" )
            # print ( f"_dTempHQBaseLevel : {_dTempHQBaseLevel}" )

            _sBuildingInfo = Dec2Hex(_dTempHQWorkshopLevel, 1) + Dec2Hex(_dTempHQExhibitionLevel, 1) + \
                Dec2Hex(_dTempHQWarehouseLevel, 1) + Dec2Hex(_dTempHQLabLevel, 1) + Dec2Hex(_dTempHQFortressLevel, 1) + Dec2Hex(_dTempHQBaseLevel, 1)

            # print ( f"_sBuildingInfo : {_sBuildingInfo}" )

            _dfSBFile.loc[i, "buildingLevelInfo"] = _sBuildingInfo

            # _dfSBFile.loc[i, "HQBaseLevel"] = _dTempHQBaseLevel
            # _dfSBFile.loc[i, "HQFortressLevel"] = _dTempHQFortressLevel
            # _dfSBFile.loc[i, "HQLabLevel"] = _dTempHQLabLevel
            # _dfSBFile.loc[i, "HQWarehouseLevel"] = _dTempHQWarehouseLevel
            # _dfSBFile.loc[i, "HQExhibitionLevel"] = _dTempHQExhibitionLevel
            # _dfSBFile.loc[i, "HQWorkshopLevel"] = _dTempHQWorkshopLevel

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

            _ltTFCount = []
            _ltTFCount = list(range(0,_dSeedTFCount))
            
            if _sSBLevel == "3":
                _dDefenceTFCount = 3
            elif _sSBLevel == "2":
                _dDefenceTFCount = random.randint(2, 3)
            elif _sSBLevel == "1":
                _dDefenceTFCount = random.randint(1, 3)

            for k in range(1,4):
                _dTempTFLevel = 0
                
                if _sSBLevel == "3":
                    _dTempTFLevel = random.randint(10,15)
                elif _sSBLevel == "2":
                    _dTempTFLevel = random.randint(5,12)
                elif _sSBLevel == "1":
                    _dTempTFLevel = random.randint(1,7)

                if k <= _dDefenceTFCount:
                    _sTempTFStandardCode = random.randint( 0, len(_ltTFCount) - 1 )
                    _sTFPrimaryKey = "01" + _dfSeedTF.loc[_sTempTFStandardCode, "StandardCode"] + "00" + Dec2Hex(_dTempTFLevel, 1)
                    _dfSquadFile.loc[i, "transformers_" + str(k) ] = int( _sTFPrimaryKey, 16 )
                    _ltTFCount.pop(_sTempTFStandardCode)
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