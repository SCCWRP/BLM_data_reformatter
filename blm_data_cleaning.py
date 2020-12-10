import pandas as pd
from pandasgui import show


relationships_map = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/RelationshipMap.xlsx").parse('Analytes')

# this is the original dataset

sccwrp_xls = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/SCCWRP_SWAMP_FieldDataSheet.xlsx")
sccwrp_field_results = sccwrp_xls.parse('sccwrp_swamp_fielddatasheet_0')


Field_Analytes = {'WaterTemperature': 'Temperature',
                  'WaterTempDuplicate' : 'Temperature',
                  'AirTemperature': 'Temperature',
                  'WaterpH': 'pH','WaterpHDuplicate': 'pH',
                  'AirWindSpeed': 'WindSpeed',
                  'WaterDOSaturation': 'Oxygen, Saturation',
                  'WaterDOSatDuplicate': 'Oxygen, Saturation',
                  'WaterDOConcentration': 'Oxygen, Dissolved',
                  'WaterDODuplicate': 'Oxygen, Dissolved',
                  'WaterSalinity': 'Salinity',
                  'WaterSalinityDuplicate': 'Salinity',
                  'WetStreamWidth': 'WettedWidth',
                  'StationWaterDepth': 'StationWaterDepth',
                  'FlowMeterSect1Depth': 'StationWaterDepth',
                  'FlowMeterSect2Depth': 'StationWaterDepth',
                  'FlowMeterSect3Depth': 'StationWaterDepth',
                  'FlowMeterSect4Depth': 'StationWaterDepth',
                  'FlowMeterSect5Depth': 'StationWaterDepth',
                  'FlowMeterSect1Velocity': 'Velocity',
                  'FlowMeterSect2Velocity': 'Velocity',
                  'FlowMeterSect3Velocity': 'Velocity',
                  'FlowMeterSect4Velocity': 'Velocity',
                  'FlowMeterSect5Velocity': 'Velocity'}


Habitat_Analytes = {'SiteOdor': 'Odor',
                  'WaterOdor': 'Odor',
                  'WaterColor': 'Color',
                  'WaterClarity': 'WaterClarity',
                  'SkyCode': 'SkyCode',
                  'WindDirection': 'WindDirection',
                  'Precipitation': 'Precipitation',
                  'PrecipitationLast24hrs': 'PrecipitationLast24hrs',
                  'EvidenceofFires': 'Evidence of Fire',
                  'OverlandRunoff': 'OverlandRunoff',
                  'DominantMaterial': 'DominantSubstrate',
                  'BeaufortScale': 'BeaufortScale',
                  'ObservedFlow': 'ObservedFlow'}



dict1 = relationships_map.loc[0:25,['OriginalAnalyteName','MatrixName']].set_index('OriginalAnalyteName').to_dict()
dict2 = relationships_map.loc[0:25,['OriginalAnalyteName','AnalyteName']].set_index('OriginalAnalyteName').to_dict()
Field_Matrix_Name = dict1['MatrixName']
Field_Analytes = dict2['AnalyteName']










# clean up blm_field_results data

blm_xls= pd.ExcelFile("BLM_Project_SWAMPformat_Field_CollectionResults.xlsx")
blm_field_results = blm_xls.parse('FieldResults')


blm_field_results.rename(columns={'StationCode': 'StationCode'},inplace=True)



# Task: Define all columns being used in the SWAMP FORMAT
# using the melt function specify the ID Varibales
# the variable names will be analytes such as airtemp

