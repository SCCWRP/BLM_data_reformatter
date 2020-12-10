import pandas as pd
from pandasgui import show


relationships_map = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/RelationshipMap.xlsx").parse('Analytes')

# this is the original dataset

sccwrp_xls = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/SCCWRP_SWAMP_FieldDataSheet.xlsx")
sccwrp_field_results = sccwrp_xls.parse('sccwrp_swamp_fielddatasheet_0')


Field_matrix_dict = relationships_map.loc[0:25,['OriginalAnalyteName','MatrixName']].set_index('OriginalAnalyteName').to_dict()
Field_analytes_dict = relationships_map.loc[0:25,['OriginalAnalyteName','AnalyteName']].set_index('OriginalAnalyteName').to_dict()


Field_Matrix_Name = Field_matrix_dict['MatrixName']
Field_Analytes = Field_analytes_dict['AnalyteName']


Field_Analytes.keys()


Habitat_matrix_dict = relationships_map.loc[26:40,['OriginalAnalyteName','MatrixName']].set_index('OriginalAnalyteName').to_dict()
Habitat_analytes_dict = relationships_map.loc[26:40,['OriginalAnalyteName','AnalyteName']].set_index('OriginalAnalyteName').to_dict()


Habitat_Matrix_Name = Habitat_matrix_dict['MatrixName']
Habitat_Analytes = Habitat_analytes_dict['AnalyteName']

# clean up blm_field_results data

blm_xls= pd.ExcelFile("BLM_Project_SWAMPformat_Field_CollectionResults.xlsx")
blm_field_results = blm_xls.parse('FieldResults')


blm_field_results.rename(columns={'StationCode': 'StationCode'},inplace=True)



# Task: Define all columns being used in the SWAMP FORMAT
# using the melt function specify the ID Varibales
# the variable names will be analytes such as airtemp

