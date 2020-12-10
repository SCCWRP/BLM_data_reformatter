import pandas as pd
from pandasgui import show


relationships_analytes = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/RelationshipMap.xlsx").parse('Analytes')
relationships_columns = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/RelationshipMap.xlsx").parse('Columns')
# this is the original dataset


sccwrp_xls = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/SCCWRP_SWAMP_FieldDataSheet.xlsx")
sccwrp_field_results = sccwrp_xls.parse('sccwrp_swamp_fielddatasheet_0')

# create field analytes
field_filter = relationships_analytes["AnalyteNameType"] == "Field"
Field_matrix_dict = relationships_analytes.loc[field_filter,['OriginalAnalyteName','MatrixName']].set_index('OriginalAnalyteName').to_dict()
Field_analytes_dict = relationships_analytes.loc[field_filter,['OriginalAnalyteName','AnalyteName']].set_index('OriginalAnalyteName').to_dict()


Field_Matrix_Name = Field_matrix_dict['MatrixName']
Field_Analytes = Field_analytes_dict['AnalyteName']


# create habitat analytes
habitat_filter = relationships_analytes["AnalyteNameType"] == "Habitat"
Habitat_matrix_dict = relationships_analytes.loc[habitat_filter,['OriginalAnalyteName','MatrixName']].set_index('OriginalAnalyteName').to_dict()
Habitat_analytes_dict = relationships_analytes.loc[habitat_filter,['OriginalAnalyteName','AnalyteName']].set_index('OriginalAnalyteName').to_dict()


Habitat_Matrix_Name = Habitat_matrix_dict['MatrixName']
Habitat_Analytes = Habitat_analytes_dict['AnalyteName']




# create melted field data

field_IDvars = relationships_columns.loc[0:16,'OriginalColumn']
field_melt_dat = pd.melt(sccwrp_field_results, id_vars=field_IDvars, value_vars=list(Field_Analytes))


field_melt_dat["variable"].replace(Field_Analytes,inplace=True)

field_melt_dat.rename(columns= {'variable': 'Analyte',
                       'value': 'Result'})



# create melted habitat data


pd.melt(sccwrp_field_results, id_vars=field_IDvars, value_vars=list(Habitat_Analytes))





# clean up blm_field_results data

blm_xls= pd.ExcelFile("BLM_Project_SWAMPformat_Field_CollectionResults.xlsx")
blm_field_results = blm_xls.parse('FieldResults')
blm_field_results.rename(columns={'StationCode': 'StationCode'},inplace=True)






# Task: Define all columns being used in the SWAMP FORMAT
# using the melt function specify the ID Varibales
# the variable names will be analytes such as airtemp

