import pandas as pd
from pandasgui import show

from globals import sccwrp_field_results, relmap, relationships_analytes, relationships_columns, habitat_ordered_cols

def habitat():
    # create habitat analytes
    habitat_filter = relationships_analytes["AnalyteNameType"] == "Habitat"

    # We can use the double asterisk notation to unpack dictionaries, and combine as one like this
    habitat_relmap = {
        **relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'MatrixName']].set_index('OriginalAnalyteName').to_dict(),
        **relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'AnalyteName']].set_index('OriginalAnalyteName').to_dict(),
        **relationships_analytes.loc[habitat_filter, ['OriginalAnalyteName', 'UnitName']].set_index('OriginalAnalyteName').to_dict()
    }


    # create melted habitat data

    habitat_tabs = ['All', 'HabitatResults']

    habitat_IDvars = relationships_columns.loc[relationships_columns['Tab'].isin(habitat_tabs), 'OriginalColumn']
    habitat_melt_dat = pd.melt(sccwrp_field_results, id_vars=habitat_IDvars, value_vars=list(habitat_relmap['AnalyteName']))

    # No need to preserve original analytename in habitat
    habitat_melt_dat = habitat_melt_dat.assign(
            MatrixName = habitat_melt_dat['variable'].replace(habitat_relmap['MatrixName']),
            UnitName = habitat_melt_dat['variable'].replace(habitat_relmap['UnitName']),
            AnalyteName = habitat_melt_dat["variable"].replace(habitat_relmap['AnalyteName'])
        ).drop(
            'variable', axis = 1
        ).rename(
            columns = {'value': 'Result'}
        )

    habitat_melt_dat['HabitatReplicate'].fillna(1, inplace=True)
    habitat_melt_dat['HabitatReplicate'].replace({'No': int(1)}, inplace=True)

    habitat_duplicates_filter = ((habitat_melt_dat['HabitatReplicate'] == 1) & (habitat_melt_dat['Result'].isna()))
    habitat_results_dat = habitat_melt_dat[-habitat_duplicates_filter]

    # fill in the blanks
    habitat_results_dat = habitat_results_dat \
        .rename(
            # Habitat uses VariableResult rather than result, which is numeric
            columns = {'Result':'VariableResult'}
        ) \
        .assign(
            BatchVerificationCode = '', 
            QACode = '', 
            ComplianceCode = '',
            ResQualCode = "=",
            FractionName = 'None',
            CollectionDeviceName = 'Not Recorded',
            HabitatResultComments = '',
            Result = -88
        )

    col_filter = relmap['columns'].Tab.isin(['All','HabitatResults'])
    habitat_results_dat.rename(
        columns = {v[0]:v[1] for v in zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }, 
        inplace = True
    )

    return habitat_results_dat.sort_values(['StationCode','SampleDate','AnalyteName'])[habitat_ordered_cols]