import pandas as pd
from pandasgui import show

from globalvariables import relmap, relationships_analytes, relationships_columns, field_ordered_cols

def field(rawdata):

    # create field analytes
    field_filter = relationships_analytes["AnalyteNameType"] == "Field"

    # We can use the double asterisk syntax to unpack the dictionaries and combine to one
    field_relmap = {
        **relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'MatrixName']].set_index('OriginalAnalyteName').to_dict(),
        **relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'AnalyteName']].set_index('OriginalAnalyteName').to_dict(),
        **relationships_analytes.loc[field_filter, ['OriginalAnalyteName', 'UnitName']].set_index('OriginalAnalyteName').to_dict()
    }

    # create melted field data
    field_tabs = ['All', 'FieldResults']

    field_IDvars = relationships_columns.loc[relationships_columns['Tab'].isin(field_tabs), 'OriginalColumn']

    print(rawdata[[c for c in rawdata.columns if list(rawdata.columns).count(c) > 1]])

    field_melt_dat = pd.melt(rawdata.loc[~rawdata.index.duplicated(keep='first')], id_vars=field_IDvars, value_vars=list(field_relmap['AnalyteName']))

    # I want to preserve the original Analytename to set locationcodes to what they need to be for certain analytes
    # It will also help us assign correct replicate numbers for the Dupes
    field_melt_dat.rename(columns = {"variable": "OriginalAnalyteName", "value": "Result"}, inplace = True)


    # We can use assign to create the new columns in this one line (technically its one line)
    # assign is just like dplyr::mutate
    # Very clean, fast and efficient way of going about this whole process, 
    # I'm impressed and it is certainly better than how i would have done it
    # Here i am just adding some syntactic sugar
    field_melt_dat = field_melt_dat.assign(
        MatrixName = field_melt_dat['OriginalAnalyteName'].replace(field_relmap['MatrixName']),
        UnitName = field_melt_dat['OriginalAnalyteName'].replace(field_relmap['UnitName']),
        AnalyteName = field_melt_dat["OriginalAnalyteName"].replace(field_relmap['AnalyteName'])
    )

    # Replicate is 2 for the analytes that have "Duplicate" in the name
    # After beginning to actually work on this, i realized it was a lot more simple than i thought
    # If you had more familiarity with the data itself you would have been able to correct me
    field_melt_dat['SampleDuplicatesTaken'] = field_melt_dat \
        .OriginalAnalyteName \
        .apply(
            lambda x:
            2 if "duplicate" in str(x).lower() # wrap in str function since it will error out if x is None or NA
            else 1
        )

    # At the end of the day that column should be Replicate
    field_melt_dat.rename(columns = {'SampleDuplicatesTaken': 'Replicate'}, inplace = True)

    # there shouldnt be a null duplicate value, since that would mean they simply did not take a duplicate measurement
    field_duplicates_filter = ((field_melt_dat['Replicate'] == 2) & (field_melt_dat['Result'].isna()))
    field_results_dat = field_melt_dat[-field_duplicates_filter]

    field_results_dat['Result'].fillna(-88,inplace=True)


    # Get the LocationCode based on OriginalAnalyteName
    # Complicated for Flowmeter Depth and Velocity
    field_results_dat = field_results_dat.sort_values(['StationID','SampleDate','AnalyteName','OriginalAnalyteName'])
    field_results_dat.LocationCode = field_results_dat.apply(
        lambda x:
        x['LocationCode']
        if "Flowmeter" not in x['OriginalAnalyteName']
        else
        # May want to check with Dario here. Either way, no big deal if this one is wrong.
        # It was definitely wrong last time we gave it to SWAMP
        'Nominal' if x['OriginalAnalyteName'] == 'StationWaterDepth' 
        else
        'Bank, Left' if 'FlowmeterSect1' in x['OriginalAnalyteName']
        else
        'Midchannel' if 'FlowmeterSect2' in x['OriginalAnalyteName']
        else
        'Midchannel2' 
            if 'FlowmeterSect3' in x['OriginalAnalyteName'] 
            and field_results_dat.Result[min(x.name + 1, max(field_results_dat.index))] != -88
        else
        'Midchannel3' if 'FlowmeterSect4' in x['OriginalAnalyteName'] and field_results_dat.Result[min(x.name + 1, max(field_results_dat.index))] != -88
        else
        'Bank, Right'
        ,
        axis = 1
    )

    # Tack on the units
    field_results_dat = field_results_dat.merge(
        pd.melt(
            rawdata, 
            id_vars = ['StationID','SampleDate'], 
            value_vars = [x for x in field_relmap['UnitName'].values() if x in rawdata.columns]
        ) \
        .rename(
            columns = {'variable':'UnitName'}
        ) \
        .drop_duplicates(),
        on = ['StationID','SampleDate','UnitName'],
        how = 'left'
    ) \
    .drop('UnitName', axis = 1) \
    .rename(
        columns = {'value':'UnitName'}
    )

    # Get the CollectionDeviceNames
    field_results_dat = field_results_dat.merge(
        pd.melt(
            rawdata[['StationID','SampleDate','InstrumentAir','InstrumentWater']] \
            .rename(columns = {'InstrumentAir': 'air', 'InstrumentWater': 'samplewater'}) \
            .fillna("Not Recorded"), 
            id_vars = ['StationID','SampleDate'], 
            value_vars = ['air','samplewater']
        ) \
        .rename(
            columns = {'variable':'MatrixName', 'value' : 'CollectionDeviceName'}
        ) \
        .drop_duplicates(),
        on = ['StationID','SampleDate','MatrixName'],
        how = 'left'
    )

    # fill in the blanks
    field_results_dat = field_results_dat.assign(
        BatchVerificationCode = '', 
        QACode = '', 
        ComplianceCode = '',
        ResQualCode = "=",
        UnitName = field_results_dat \
            .UnitName.fillna("None") \
            .str.replace("_","/") \
            .str.replace("µ","u") \
            .str.replace("percent","%") \
            .str.replace("degree\s*C","deg C", regex = True)
        ,
        FieldReplicate = 1,
        # No info on fractionname in raw original data. Total is for Oxygen, Saturation or Dissolved Oxygen Concentration.
        FractionName = field_results_dat.AnalyteName.apply(lambda x: 'Total' if "Oxygen" in str(x) else 'None'),
        # Need to ask Dario about CollectionDevice, etc
        # We can probably enter manually in excel. Its in the data sheet, but seems like not all info is there
        # (InstrumentAir and InstrumentWater columns)
        #CollectionDeviceName YSI Pro1020 should be YSI Pro1020
        CollectionDeviceName = field_results_dat \
            .apply(
                lambda x:
                'Wading Rod'
                if x['MatrixName'] == 'habitat'
                else 
                x['CollectionDeviceName'].replace("YSIP","YSI P")
                ,
                axis = 1
            )
    )

    field_results_dat = field_results_dat \
        .sort_values(['StationID','SampleDate','AnalyteName']) \
        .drop("OriginalAnalyteName", axis = 1)

    col_filter = relmap['columns'].Tab.isin(['All','FieldResults'])
    field_results_dat.rename(
        columns = {v[0]:v[1] for v in zip( relmap['columns'][col_filter].OriginalColumn, relmap['columns'][col_filter].Column ) }, 
        inplace = True
    )
    
    return field_results_dat.sort_values(['StationCode','SampleDate','AnalyteName'])[field_ordered_cols]