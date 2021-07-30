import pandas as pd
import re

from globalvariables import \
    relmap, \
    sample_ordered_cols, samplehistory_ordered_cols, personnel_ordered_cols, locations_ordered_cols

def sample(rawdata):
    # Looks like I goofed when I put all .... 
    col_filter = ( (relmap['columns'].Tab == 'All') & ( ~relmap['columns'].Column.isin(['LocationCode','GeometryShape']) ) )
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }
    df = rawdata.rename(columns = relevant_cols)[list(relevant_cols.values())][sample_ordered_cols]
    # Fix common mistakes in df
    df.loc[df['AnalyteName']=='Salinity' ,'UnitName']= 'ppt'
    return 

def samplehistory(rawdata):
    # All, or SampleHistory would get us the relevant columns... of course except LocationCode and GeometryShape. My mistake there
    # We can fix that later
    col_filter = ( (relmap['columns'].Tab.isin(['All','SampleHistory'])) & ( ~relmap['columns'].Column.isin(['LocationCode','GeometryShape']) ) )
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }
    
    newdata = rawdata.rename(columns = relevant_cols)[list(relevant_cols.values())][samplehistory_ordered_cols]
    newdata.PurposeFailureName = newdata.PurposeFailureName.str.replace("Dry_NoWater_","Dry (no water)")
    newdata.SamplePurposeCode = "WaterChem" # Wont accept FieldMeasure and WaterChem
    
    return newdata

def personnel(rawdata):
    # All, or PersonnelDuty would get us the relevant columns... of course except LocationCode and GeometryShape. My mistake there
    # We can fix that later
    col_filter = ( (relmap['columns'].Tab.isin(['All','PersonnelDuty'])) & ( ~relmap['columns'].Column.isin(['LocationCode','GeometryShape']) ) )
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }
 
    return \
    rawdata[list(relevant_cols)] \
        .melt(
            id_vars = list(set(relevant_cols.keys()) - {'TeamLeader','OtherTeamMembers'}), 
            value_vars = ['TeamLeader','OtherTeamMembers']
        ) \
        .rename(columns = {'value':'PersonnelCode', 'AnySpecificDuties':'PersonnelDutyCode'}) \
        .rename(columns = relevant_cols) \
        .drop('variable', axis = 1) \
        .dropna(subset = ['PersonnelCode','PersonnelDutyCode'], how = 'all') \
        [personnel_ordered_cols]

def locations(rawdata):
    # All, or Locations, would be the relevant columns here
    col_filter = relmap['columns'].Tab.isin(['All','Locations'])
    relevant_cols = {v[0]:v[1] for v in  zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }

    newdata = rawdata.rename(columns = relevant_cols)[list(relevant_cols.values())][locations_ordered_cols]
    newdata.Hydromod = newdata.Hydromod.str.replace("ConcretChannel","ConChan")
    newdata.Hydromod = newdata.apply(
        lambda x: 
        "Weir" if x['StationCode'] == 'SGR2-Wht'
        else "Culvert" if x['StationCode'] == 'SGR3-Dam'
        else "Dam" if x['StationCode'] == 'SGR3-Sjc'
        else x['Hydromod']
        ,
        axis = 1
    )
    newdata.CoordinateNumber = 1
    newdata.OccupationMethod = newdata.OccupationMethod \
        .apply(
            lambda x:
            "Walk In"
            if bool(re.search("walk\s*in",str(x).lower()))
            else x
        )
    newdata.UnitElevation = "m" # This is literally the only value they accept for this column
    return newdata