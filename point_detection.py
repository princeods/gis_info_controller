import os
import glob
from re import X
from pandas import *
from snowpipe import *
from tqdm import tqdm


# -----------------------------------------------------------------------------------

_pathSBLocation = "./space_bridge/"
_pathSBPartner = "./partner_sb/"
_pathResult = "./changeSB/" 

_fStandardDistance = float(90)
_dResultCount = 0

_dfResult = pandas.DataFrame(index=range(0,0),columns = ["OriginKey", "OriginLatitude", "OriginLongitude",\
     "PartnerName", "PartnerLatitude", "PartnerLongitude", 'distance'])
#_dfPartner = pandas.DataFrame(index=range(0,0),columns = ["name", "latitude", "longitude"])

_dfPartner = pandas.read_csv(_pathSBPartner + "1.csv")

# -----------------------------------------------------------------------------------

CreateFolder(_pathResult)

# -----------------------------------------------------------------------------------

for _fileOriginSB in tqdm(glob.glob(_pathSBLocation+"*.csv")):

    _dfOrigin= pandas.DataFrame(index=range(0,0))
    _dfOrigin = pandas.read_csv(_fileOriginSB)

    for _pointOriginCount in tqdm(range(0,len(_dfOrigin))):

        for i in range(0,len(_dfPartner)):
            _fDiatance = CalcSb2SbDistance(_dfPartner.loc[i,'longitude'],_dfPartner.loc[i,'latitude'],\
                _dfOrigin.loc[_pointOriginCount,'longitude'],_dfOrigin.loc[_pointOriginCount,'latitude'])

            if _fDiatance < _fStandardDistance:
                _dfResult.loc[_dResultCount,'OriginKey'] = _dfOrigin.loc[_pointOriginCount,'PrimaryKey']
                _dfResult.loc[_dResultCount,'OriginLatitude'] = _dfOrigin.loc[_pointOriginCount,"latitude"]
                _dfResult.loc[_dResultCount,'OriginLongitude'] = _dfOrigin.loc[_pointOriginCount,'longitude']
                _dfResult.loc[_dResultCount,'PartnerName'] = _dfPartner.loc[i,'name']
                _dfResult.loc[_dResultCount,'PartnerLatitude'] = _dfPartner.loc[i,'latitude']
                _dfResult.loc[_dResultCount,'PartnerLongitude'] = _dfPartner.loc[i,'longitude']
                _dfResult.loc[_dResultCount,'distance'] = _fDiatance

                _dResultCount += 1

print(_dfResult)

result = pandas.ExcelWriter(_pathResult + 'toChange.xlsx')

_dfResult.to_excel(result, sheet_name='toChange')

result.save()