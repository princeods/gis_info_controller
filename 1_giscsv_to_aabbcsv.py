import math
import os
import glob
import re
import numpy
import pandas
from tqdm import tqdm
import datetime
import haversine 

_pathLocation = "./origin/"             #가져올 파일 위치
_pathToLocation = "./aabb/"             #출력폴더

_fDistanceSb2Sb = 90                    #스페이스 브리지 간 최소 거리

_tStartTime = datetime.datetime.now()

# lineC = int(input("파일 당 포인트 수량을 입력 하시오 ( max : 65535 ) : "))
_dLineC = 65535

def CreateFolder(_sDirectoryName): # 폴더 생성
    try:
        if not os.path.exists(_sDirectoryName):
            os.makedirs(_sDirectoryName)
    except OSError:
        print ('Error: Creating directory. ' +  _sDirectoryName)

def CalcSb2SbDistance(_fTempLon, _fTempLat):
    try:
        for i in reversed(range(int(len(_dfTemp)))):

            _fSTempLat = _dfTemp.loc[i,"y"]
            _fSTempLon = _dfTemp.loc[i,"x"]

            a = math.cos(math.radians(90 - _fSTempLat))
            b = math.cos(math.radians(90 - _fTempLat))
            c = math.sin(math.radians(90 - _fSTempLat))
            d = math.sin(math.radians(90 - _fTempLat))
            e = math.cos(math.radians(_fSTempLon - _fTempLon))

            _fTempDistance = math.acos((a * b) + (c * d * e)) * 6378.137 * 1000

            if _fTempDistance  < _fDistanceSb2Sb:
                return False
        return True

    except:
        # print(f"\n target lat : {_fTempLat}, target lon : {_fTempLon}, standard lat : {_fSTempLat}, standard lon : {_fSTempLon}")
        return False

_dOutputIndex = 0
_dFileIndex = 0

for _fileOriginCsvfile in glob.glob(_pathLocation+'*.csv'):

    _dfOutput = pandas.DataFrame(index=range(0,0),columns = ['osm_id','name','x','y'])
    _dfTemp = pandas.DataFrame(index=range(0,0),columns = ['osm_id','name','x','y'])
    
    _dTempIndex = 0

    if os.path.isdir(_pathToLocation) != True: #출력폴더 체크
        CreateFolder(_pathToLocation)

    _sFilename = os.path.basename(_fileOriginCsvfile)

    print(_fileOriginCsvfile)
    _dfOrigin = pandas.read_csv(_fileOriginCsvfile) #, error_bad_lines = False)
    
    print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )
    print( f"{_sFilename} point 정렬 중.")
    print( f"파일 당 point 수량 : {_dLineC}")
    print( f"포인트 간 최소 거리 : {_fDistanceSb2Sb} m")
    print( f"작업 시작 시간 : {_tStartTime}" )
    print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )

    for i in tqdm(range(int(len(_dfOrigin)))):
        
        if int(len(_dfTemp)) == 0:
            _dfTemp.loc[_dTempIndex] = _dfOrigin.loc[i]
            _dTempIndex += 1
        else:
            if CalcSb2SbDistance(_dfOrigin.loc[i, "x"], _dfOrigin.loc[i, "y"]):
                _dfTemp.loc[_dTempIndex] = _dfOrigin.loc[i]
                _dTempIndex += 1

        # if (( i / 10000 == int ( i / 10000 ) ) and ( i != 0 )) or ( i == int(len(_dfOrigin)) -1 ):
        #     print ( f"\n {i} 개 정렬 후 유효한 포인트 수량 : {len(_dfTemp)}" )

    print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )
    print(f"aabb ( csv ) 파일 생성 중.")
    print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )

    for j in tqdm(range(int(len(_dfTemp)))):

        _dfOutput.loc[_dOutputIndex] = _dfTemp.loc[j]

        if ( _dOutputIndex == ( _dLineC - 1 ) ) or ( j == int(len(_dfTemp) - 1 ) ):
            # _dfOutput.to_csv( os.replace(_fileOriginCsvfile, ".csv", "") )
            _dfOutput.to_csv( _pathToLocation + _sFilename.replace( ".csv", "_" ) + str( _dFileIndex ) + ".csv", sep=",", index = False, encoding = "utf-8-sig" , line_terminator = "\r\n", float_format = "%.7f" )

            _dfOutput = pandas.DataFrame(index=range(0,0),columns = ['osm_id','name','x','y'])
            _dOutputIndex = 0
            _dFileIndex += 1

            if j == int(len(_dfTemp) - 1):
                print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )
                print( f"{_sFilename} 지역에서 {len(_dfTemp )} 개 스페이스 브리지 포인트 생성 완료." )
                print( f"작업 완료 소요 시간 : {datetime.datetime.now() - _tStartTime}" )
                print( "\033[31m" + "-------------------------------------------------------------------"  + "\033[0m" )

        else:
            _dOutputIndex += 1

    