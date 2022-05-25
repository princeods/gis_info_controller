import os
import glob
import pandas
import math
from tqdm import tqdm

# -----------------------------------------------------------------------------------

def CreateFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ("Error: Creating directory. " +  directory)

# -----------------------------------------------------------------------------------

def HQTypeName(type):
    if type == 0:
        return "본부"
    elif type == 1:
        return "요새"
    elif type == 2:
        return "연구소"
    elif type == 3:
        return "에너존 창고"
    elif type == 4:
        return "전시관"
    elif type == 5:
        return "파츠 제작소"
    else:
        return "Unidentify building type!"

# -----------------------------------------------------------------------------------

def Dec2Hex(_dValue,_dDigit):
    try:
        _sTemp = format(_dValue,"X")
        for i in range(_dDigit - len(_sTemp)):
            _sTemp = "0" + _sTemp
        return _sTemp
    
    except:
        print (f"_dValue : {_dValue}, _dDigit : {_dDigit}")

# -----------------------------------------------------------------------------------

def CalcSb2SbDistance(_fTargetLon, _fTargetLat, _fTempLon, _fTempLat):
    try:
        a = math.cos(math.radians(90 - _fTargetLat))
        b = math.cos(math.radians(90 - _fTempLat))
        c = math.sin(math.radians(90 - _fTargetLat))
        d = math.sin(math.radians(90 - _fTempLat))
        e = math.cos(math.radians(_fTargetLon - _fTempLon))

        _fTempDistance = math.acos((a * b) + (c * d * e)) * 6378.137 * 1000

        return _fTempDistance

    except:
        print(f"\n target lat : {_fTempLat}, target lon : {_fTempLon}, standard lat : {_fTargetLat}, standard lon : {_fTargetLon}, _fTempDistance : {_fTempDistance}")