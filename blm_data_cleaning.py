import pandas as pd
from pandasgui import show

# Read in the relationship map
relationships_analytes = pd.ExcelFile("input/RelationshipMap.xlsx").parse('Analytes')
relationships_columns = pd.ExcelFile("input/RelationshipMap.xlsx").parse('Columns')

# this is the original dataset
sccwrp_field_results = pd.read_excel("input/SCCWRP_SWAMP_FieldDataSheet.xlsx", sheet_name = 'sccwrp_swamp_fielddatasheet_0')

# tack on missing columns
sccwrp_field_results.assign(BatchVerificationCode = '', QACode = '', ResQualCode = '=')
    
 
# create field analytes
field_filter = relationships_analytes["AnalyteNameType"] == "Field"

field = {
    **relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'MatrixName']].set_index('OriginalAnalyteName').to_dict(),
    **relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'AnalyteName']].set_index('OriginalAnalyteName').to_dict(),
    **relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'UnitName']].set_index('OriginalAnalyteName').to_dict()
}

# create habitat analytes
habitat_filter = relationships_analytes["AnalyteNameType"] == "Habitat"

habitat = {
    **relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'MatrixName']].set_index('OriginalAnalyteName').to_dict(),
    **relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'AnalyteName']].set_index('OriginalAnalyteName').to_dict(),
    **relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'UnitName']].set_index('OriginalAnalyteName').to_dict()
}



# create melted field data
field_tabs = ['All', 'FieldResults']

field_IDvars = relationships_columns.loc[relationships_columns['Tab'].isin(field_tabs), 'OriginalColumn']
field_melt_dat = pd.melt(sccwrp_field_results, id_vars=field_IDvars, value_vars=list(field['AnalyteName']))

# I want to preserve the original Analytename to set locationcodes to what they need to be for certain analytes
# It will also help us assign correct replicate numbers for the Dupes
field_melt_dat.rename(columns = {"variable": "OriginalAnalyteName", "value": "Result"}, inplace = True)

# We can use assign to create the new columns in this one line (technically its one line)
# Very clean, fast and efficient way of going about this whole process, 
# I'm impressed and it is certainly better than how i would have done it
# Here i am just adding some syntactic sugar
field_melt_dat = field_melt_dat.assign(
    MatrixName = field_melt_dat['OriginalAnalyteName'].replace(field['MatrixName']),
    UnitName = field_melt_dat['OriginalAnalyteName'].replace(field['UnitName']),
    AnalyteName = field_melt_dat["OriginalAnalyteName"].replace(field['AnalyteName'])
)



field_melt_dat['SampleDuplicatesTaken'].fillna(1,inplace=True)
field_melt_dat['SampleDuplicatesTaken'].replace({'Yes': int(2), 'No': int(1)}, inplace=True)

field_duplicates_filter = ((field_melt_dat['SampleDuplicatesTaken'] == 1) & (field_melt_dat['Result'].isna()))
field_results_dat = field_melt_dat[-field_duplicates_filter]

field_results_dat['Result'].fillna(-88,inplace=True)


# create melted habitat data

habitat_tabs = ['All', 'HabitatResults']

habitat_IDvars = relationships_columns.loc[relationships_columns['Tab'].isin(habitat_tabs), 'OriginalColumn']
habitat_melt_dat = pd.melt(sccwrp_field_results, id_vars=habitat_IDvars, value_vars=list(habitat['AnalyteName']))

habitat_melt_dat.rename(columns= {'variable': 'OriginalAnalyteName', 'value': 'Result'}, inplace=True)

habitat_melt_dat = habitat_melt_dat.assign(
    MatrixName = habitat_melt_dat['OriginalAnalyteName'].replace(habitat['MatrixName']),
    UnitName = habitat_melt_dat['OriginalAnalyteName'].replace(habitat['UnitName']),
    AnalyteName = habitat_melt_dat["OriginalAnalyteName"].replace(habitat['AnalyteName'])
)

habitat_melt_dat['HabitatReplicate'].fillna(1, inplace=True)
habitat_melt_dat['HabitatReplicate'].replace({'No': int(1)}, inplace=True)

habitat_duplicates_filter = ((habitat_melt_dat['HabitatReplicate'] == 1) & (habitat_melt_dat['Result'].isna()))
habitat_results_dat = habitat_melt_dat[-habitat_duplicates_filter]


# create excel file with field/habitat results as sheets
blm_swampformat = pd.ExcelWriter('output/blm_swampformat.xlsx', engine='xlsxwriter')

field_results_dat.sort_values(['StationID','SampleDate']).to_excel(blm_swampformat, sheet_name='FieldResults', index = False)
habitat_results_dat.sort_values(['StationID','SampleDate']).to_excel(blm_swampformat, sheet_name='HabitatResults', index = False)

blm_swampformat.save()