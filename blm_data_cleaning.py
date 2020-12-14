import pandas as pd
from pandasgui import show


relationships_analytes = pd.ExcelFile("C:/Users/toled/Desktop/BLM_data_reformatter/RelationshipMap.xlsx").parse('Analytes')
relationships_columns = pd.ExcelFile("C:/Users/toled/Desktop/BLM_data_reformatter/RelationshipMap.xlsx").parse('Columns')
# this is the original dataset


sccwrp_xls = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/SCCWRP_SWAMP_FieldDataSheet.xlsx")
sccwrp_field_results = sccwrp_xls.parse('sccwrp_swamp_fielddatasheet_0')


BLM_SWAMPformat_Field_Results = pd.ExcelFile("C:/Users/toled/Desktop/BLM_data_reformatter/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx").parse('FieldResults')


# create field analytes
field_filter = relationships_analytes["AnalyteNameType"] == "Field"
Field_matrix_dict = relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'MatrixName']].set_index('OriginalAnalyteName').to_dict()
Field_analytes_dict = relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'AnalyteName']].set_index('OriginalAnalyteName').to_dict()
Field_unitname_dict = relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'UnitName']].set_index('OriginalAnalyteName').to_dict()


Field_Matrix_Name = Field_matrix_dict['MatrixName']
Field_Analytes = Field_analytes_dict['AnalyteName']
Field_UnitName = Field_unitname_dict['UnitName']


# create habitat analytes
habitat_filter = relationships_analytes["AnalyteNameType"] == "Habitat"
Habitat_matrix_dict = relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'MatrixName']].set_index('OriginalAnalyteName').to_dict()
Habitat_analytes_dict = relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'AnalyteName']].set_index('OriginalAnalyteName').to_dict()
Habitat_unitname_dict = relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'UnitName']].set_index('OriginalAnalyteName').to_dict()

Habitat_Matrix_Name = Habitat_matrix_dict['MatrixName']
Habitat_Analytes = Habitat_analytes_dict['AnalyteName']
Habitat_UnitName = Habitat_unitname_dict['UnitName']


# create melted field data

field_tabs = ['All', 'FieldResults']

field_IDvars = relationships_columns.loc[relationships_columns['Tab'].isin(field_tabs), 'OriginalColumn']
field_melt_dat = pd.melt(sccwrp_field_results, id_vars=field_IDvars, value_vars=list(Field_Analytes))

field_melt_dat['MatrixName'] = field_melt_dat['variable']
field_melt_dat['MatrixName'].replace(Field_Matrix_Name, inplace=True)


field_melt_dat['UnitName'] = field_melt_dat['variable']
field_melt_dat['UnitName'].replace(Field_UnitName, inplace=True)

field_melt_dat["variable"].replace(Field_Analytes, inplace=True)
field_melt_dat.rename(columns= {'variable': 'Analyte',
                       'value': 'Result'}, inplace=True)

field_melt_dat['ResQualCode'] = '='
field_melt_dat['QACode'] = 'None'
field_melt_dat['ComplianceCode'] =""
field_melt_dat['BatchVerificationCode'] =""


field_melt_dat['SampleDuplicatesTaken'].fillna(1, inplace=True)
field_melt_dat['SampleDuplicatesTaken'].replace({'Yes': int(2), 'No': int(1)}, inplace=True)

field_duplicates_filter = ((field_melt_dat['SampleDuplicatesTaken'] ==1) & (field_melt_dat['Result'].isna()))
field_results_dat = field_melt_dat[-field_duplicates_filter]

field_results_dat['Result'].fillna(-88, inplace=True)



# create melted habitat data

habitat_tabs = ['All', 'HabitatResults']

habitat_IDvars = relationships_columns.loc[relationships_columns['Tab'].isin(habitat_tabs), 'OriginalColumn']
habitat_melt_dat = pd.melt(sccwrp_field_results, id_vars=habitat_IDvars, value_vars=list(Habitat_Analytes))

habitat_melt_dat["variable"].replace(Habitat_Analytes, inplace=True)


habitat_melt_dat['MatrixName'] = habitat_melt_dat['variable']
habitat_melt_dat['MatrixName'].replace(Habitat_Matrix_Name, inplace=True)


habitat_melt_dat['UnitName'] = habitat_melt_dat['variable']
habitat_melt_dat['UnitName'].replace(Habitat_UnitName, inplace=True)


habitat_melt_dat["variable"].replace(Habitat_Analytes, inplace=True)

habitat_melt_dat.rename(columns= {'variable': 'Analyte',
                       'value': 'Result'}, inplace=True)


habitat_melt_dat['ResQualCode'] = '='
habitat_melt_dat['QACode'] = 'None'
habitat_melt_dat['ComplianceCode'] =""
habitat_melt_dat['BatchVerificationCode'] =""


habitat_melt_dat['HabitatReplicate'].fillna(1, inplace=True)
habitat_melt_dat['HabitatReplicate'].replace({'No': int(1)}, inplace=True)

habitat_duplicates_filter = ((habitat_melt_dat['HabitatReplicate'] == 1) & (habitat_melt_dat['Result'].isna()))
habitat_results_dat = habitat_melt_dat[-habitat_duplicates_filter]


# create excel file with units in them for field/habitat
blm_swampformat = pd.ExcelWriter('blm_swampformat2.xlsx', engine='xlsxwriter')
field_results_dat.to_excel(blm_swampformat, sheet_name='FieldResults')
habitat_results_dat.to_excel(blm_swampformat, sheet_name='HabitatResults')
blm_swampformat.save()


# Trying to add the units for each analyte
field_blm_results = pd.ExcelFile("C:/Users/toled/Desktop/BLM_data_reformatter/blm_swampformat2.xlsx").parse('FieldResults')
show(field_blm_results)


field_blm_results['ResQualCode'] = '='
field_blm_results['QACode'] = 'None'
field_blm_results['ComplianceCode'] =""
field_blm_results['BatchVerificationCode'] =""


watertempunit_filter = field_blm_results['UnitName'] =='WaterTemperatureUnit'
print(field_blm_results.loc[watertempunit_filter, ['Result', 'WaterTemperatureUnit']])


airtemp_filter = field_blm_results['UnitName'] == 'AirTemperatureUnit'
print(field_blm_results.loc[airtemp_filter,['Result', 'AirTemperatureUnit']])


ph_filter = field_blm_results['UnitName'] == 'none'
print(field_blm_results.loc[ph_filter,'Result'])


airwindspeed_filter = field_blm_results['UnitName'] == 'AirWindSpeedUnit'
print(field_blm_results.loc[airwindspeed_filter, ['Result', 'AirWindSpeedUnit']])


waterDOsat_filter = field_blm_results['UnitName'] == 'WaterDOSatUnit'
print(field_blm_results.loc[waterDOsat_filter,['Result', 'WaterDOSatUnit']])


#waterDO_filter = field_blm_results['UnitName'] == 'WaterDOUnit'
#field_blm_results.loc[waterDO_filter,['Result', 'WaterDOUnit']]


waterSpConduct_filter = field_blm_results['UnitName'] == 'WaterSpConductivityUnit'
print(field_blm_results.loc[waterSpConduct_filter,['Result', 'WaterSpConductivityUnit']])

watersalinity_filter = field_blm_results['UnitName'] == 'WaterSalinityUnit'
print(field_blm_results.loc[watersalinity_filter,['Result', 'WaterSalinityUnit']])


#WettedStreamWidUnit_filter = field_blm_results['UnitName'] == 'WettedStreamWidUnit'
#field_blm_results.loc[WettedStreamWidUnit_filter,['Result', 'WettedStreamWidUnit']]







