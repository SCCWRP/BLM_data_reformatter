import pandas as pd
from pandasgui import show
# Clean up sccwrp-field-results tab

sccwrp_xls = pd.ExcelFile("C:/Users/toled/Desktop/SCCWRP/SCCWRP_SWAMP_FieldDataSheet.xlsx")
sccwrp_field_results = sccwrp_xls.parse('sccwrp_swamp_fielddatasheet_0')

sccwrp_field_columns = list(sccwrp_field_results.columns)


print(sccwrp_field_results['SampleDuplicatesTaken'].unique())




# clean up blm_field_results data

blm_xls= pd.ExcelFile("BLM_Project_SWAMPformat_Field_CollectionResults.xlsx")
blm_field_results = blm_xls.parse('FieldResults')


blm_field_results.rename(columns={'StationCode': 'StationCode'},inplace=True)



# Task: Define all columns being used in the SWAMP FORMAT
# using the melt function specify the ID Varibales
# the variable names will be analytes such as airtemp

