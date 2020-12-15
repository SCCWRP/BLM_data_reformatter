import pandas as pd
from pandasgui import show

from globals import \
    sccwrp_field_results, relmap, \
    sample_ordered_cols, samplehistory_ordered_cols, personnel_ordered_cols, locations_ordered_cols

def sample():
    # Looks like I goofed when I put all .... 
    col_filter = ( (relmap['columns'].Tab == 'All') & ( ~relmap['columns'].Column.isin(['LocationCode','GeometryShape']) ) )
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }
    
    return sccwrp_field_results.rename(columns = relevant_cols)[list(relevant_cols.values())][sample_ordered_cols]

def samplehistory():
    # All, or SampleHistory would get us the relevant columns... of course except LocationCode and GeometryShape. My mistake there
    # We can fix that later
    col_filter = ( (relmap['columns'].Tab.isin(['All','SampleHistory'])) & ( ~relmap['columns'].Column.isin(['LocationCode','GeometryShape']) ) )
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }
    
    return sccwrp_field_results.rename(columns = relevant_cols)[list(relevant_cols.values())][samplehistory_ordered_cols]

def personnel():
    # All, or PersonnelDuty would get us the relevant columns... of course except LocationCode and GeometryShape. My mistake there
    # We can fix that later
    col_filter = ( (relmap['columns'].Tab.isin(['All','PersonnelDuty'])) & ( ~relmap['columns'].Column.isin(['LocationCode','GeometryShape']) ) )
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }
    
    return \
    sccwrp_field_results[list(relevant_cols)] \
        .melt(
            id_vars = list(set(relevant_cols.keys()) - {'TeamLeader','OtherTeamMembers'}), 
            value_vars = ['TeamLeader','OtherTeamMembers']
        ) \
        .rename(columns = {'value':'PersonnelCode', 'AnySpecificDuties':'PersonnelDutyCode'}) \
        .rename(columns = relevant_cols) \
        .drop('variable', axis = 1) \
        .dropna(subset = ['PersonnelCode','PersonnelDutyCode'], how = 'all') \
        [personnel_ordered_cols]

def locations():
    # All, or Locations, would be the relevant columns here
    col_filter = relmap['columns'].Tab.isin(['All','Locations'])
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }

    return sccwrp_field_results.rename(columns = relevant_cols)[list(relevant_cols.values())][locations_ordered_cols]