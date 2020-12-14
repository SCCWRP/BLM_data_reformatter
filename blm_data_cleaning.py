import pandas as pd
from pandasgui import show


relationships_analytes = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/RelationshipMap.xlsx").parse('Analytes')
relationships_columns = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/RelationshipMap.xlsx").parse('Columns')
# this is the original dataset


sccwrp_xls = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/SCCWRP_SWAMP_FieldDataSheet.xlsx")
sccwrp_field_results = sccwrp_xls.parse('sccwrp_swamp_fielddatasheet_0')

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

<<<<<<< HEAD
=======

>>>>>>> 79ae24f4a74e95fcfa7874bd658ae291078ffc22
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

<<<<<<< HEAD

=======
field_melt_dat['SampleDuplicatesTaken'].fillna(1,inplace=True)
field_melt_dat['SampleDuplicatesTaken'].replace({'Yes': int(2), 'No': int(1)}, inplace=True)

field_duplicates_filter = ((field_melt_dat['SampleDuplicatesTaken'] ==1) & (field_melt_dat['Result'].isna()))
field_results_dat = field_melt_dat[-field_duplicates_filter]

field_results_dat['Result'].fillna(-88,inplace=True)
>>>>>>> 79ae24f4a74e95fcfa7874bd658ae291078ffc22


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

<<<<<<< HEAD
=======
habitat_melt_dat['HabitatReplicate'].fillna(1, inplace=True)
habitat_melt_dat['HabitatReplicate'].replace({'No': int(1)}, inplace=True)

habitat_duplicates_filter = ((habitat_melt_dat['HabitatReplicate'] == 1) & (habitat_melt_dat['Result'].isna()))
habitat_results_dat = habitat_melt_dat[-habitat_duplicates_filter]
>>>>>>> 79ae24f4a74e95fcfa7874bd658ae291078ffc22




<<<<<<< HEAD
blm_swampformat = pd.ExcelWriter('blm_swampformat.xlsx', engine='xlsxwriter')

field_melt_dat.to_excel(blm_swampformat, sheet_name='FieldResults')
habitat_melt_dat.to_excel(blm_swampformat, sheet_name='HabitatResults')
=======
# create excel file with field/habitat results as sheets
blm_swampformat = pd.ExcelWriter('blm_swampformat.xlsx', engine='xlsxwriter')

field_results_dat.to_excel(blm_swampformat, sheet_name='FieldResults')
habitat_results_dat.to_excel(blm_swampformat, sheet_name='HabitatResults')
>>>>>>> 79ae24f4a74e95fcfa7874bd658ae291078ffc22

blm_swampformat.save()