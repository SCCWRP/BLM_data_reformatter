from arcgis.gis import GIS
import pandas as pd
import xlsxwriter, openpyxl, argparse, sys
from datetime import datetime

pd.set_option("display.max_columns", 30)

# Build the argument parser
parser = argparse.ArgumentParser(prog='BLM Reformatter')
parser.add_argument('--file', help = 'Path to the file that contains the raw data')
parser.add_argument('--month', help = '5')
args = parser.parse_args()

# custom imports from the local files
from field import field
from habitat import habitat
from sampleinfo import sample, samplehistory, personnel, locations
from globalvariables import relmap

month_dict = {
    1: 'Jan',  2: 'Feb',  3: 'Mar',  4: 'Apr',
    5: 'May',  6: 'Jun',  7: 'Jul',  8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec',
}

if args.file:
    # These will be used to subset the raw data
    rawdatapath = args.file
    # this is the original dataset
    sccwrp_field_results = pd.read_excel(rawdatapath, sheet_name = 'sccwrp_swamp_fielddatasheet_0')
else:
    gis = GIS("https://www.arcgis.com","ReadOnly","92626$Harbor")
    
    #search_results = gis.content.search('title: sccwrp_landstationoccupationform', 'Feature Layer')
    search_results = gis.content.search(f'title: SCCWRP_SWAMP_FieldDataSheet_v1', 'Feature Layer')
    results = search_results[0]

    # import into dataframe
    sccwrp_field_results = results.layers[0].query().sdf
    
    # rename column to aliases
    sccwrp_field_results = sccwrp_field_results.rename(
        columns = {
            x[0] : x[1] 
            for x in zip(relmap['aliases'].OriginalColumnName, relmap['aliases'].Alias) 
            if x[0] in sccwrp_field_results.columns
        }
    )

try:
    month = int(args.month) if args.month else None
except:
    raise Exception(f"The --month argument must be an integer from 1 to 12. You entered the value of {args.month}")

# Project Name should always be Biotic Ligand Model
sccwrp_field_results = sccwrp_field_results[
    (sccwrp_field_results.SccwrpProjectName == 'BioticLigandModel')
    &
    ( True if month is None else sccwrp_field_results.SampleDate.apply(lambda x: x.month == month) )
]


# clean up the stations a bit
sccwrp_field_results.StationID = sccwrp_field_results.StationID.str.replace("BLM-RB4-","")

# Put hte dates as strings like how SWAMP likes them
for c in sccwrp_field_results.columns:
    if "date" in c.lower():
        sccwrp_field_results[c] = pd.to_datetime(sccwrp_field_results[c])




# only run if there are records for the month they are asking for
if sccwrp_field_results.empty:
    print(f"No results found for month {month}")
    sys.exit()

# Get all data starting the month
start_month = 5
sccwrp_field_results = sccwrp_field_results[
                        sccwrp_field_results['SampleDate'] >= pd.Timestamp(
                            f'{start_month}-01-2021 00:00:00'
                        )
]

# output file path to be used both times the file gets written
# output_filepath = f"output/blm_swampformat_{month_dict[month] if month else ''}.xlsx"
output_filepath = f"output/blm_swampformat_from_{month_dict[start_month]}2021.xlsx"

# use xlsxwriter to write the data out without the resqualcode equal signs getting interpreted as formulas
# I am not sure if openpyxl also has a similar capability, but I do know how to do it with xlsxwriter
with \
pd.ExcelWriter(
    output_filepath, 
    engine = 'xlsxwriter', 
    date_format = 'dd/mmm/yyyy',
    datetime_format = 'dd/mmm/yyyy',
    options = {'strings_to_urls': False, 'strings_to_formulas': False}
) \
as writer:
    
    # Call each function and write to excel
    sample(sccwrp_field_results).to_excel(writer, sheet_name = "Sample", index = False)
    samplehistory(sccwrp_field_results).to_excel(writer, sheet_name = "SampleHistory", index = False)
    personnel(sccwrp_field_results).to_excel(writer, sheet_name = "PersonnelDuty", index = False)
    locations(sccwrp_field_results).to_excel(writer, sheet_name = "Locations", index = False)
    field(sccwrp_field_results).to_excel(writer, sheet_name = "FieldResults", index = False)
    pd.read_excel('info/SWAMP_Field_CollectionResults_Template_v2.5_081420.xlsx', sheet_name = "HabitatResults") \
        .to_excel(writer, sheet_name = "HabitatResults", index = False)
    pd.read_excel('info/SWAMP_Field_CollectionResults_Template_v2.5_081420.xlsx', sheet_name = "BenthicResults") \
        .to_excel(writer, sheet_name = "BenthicResults", index = False) 
    pd.read_excel('info/SWAMP_Field_CollectionResults_Template_v2.5_081420.xlsx', sheet_name = "ChemResults") \
        .to_excel(writer, sheet_name = "ChemResults", index = False) 
    pd.read_excel('info/SWAMP_Field_CollectionResults_Template_v2.5_081420.xlsx', sheet_name = "LabBatch") \
        .to_excel(writer, sheet_name = "LabBatch", index = False) 

    # Save it and we're done!
    writer.save()


# Use openpyxl to fit the columns to character width
# I remember researching this before, and i don't think xlsxwriter has this kind of feature
# with pd.ExcelWriter(output_filepath, engine = 'openpyxl') as writer:
#     writer.book = openpyxl.load_workbook(output_filepath)

#     for worksheet in writer.book._sheets:
#         for column_cells in worksheet.columns:
#             length = max(len(str(cell.value) if cell.value else "") for cell in column_cells) + 2
#             worksheet.column_dimensions[openpyxl.utils.get_column_letter(column_cells[0].column)].width = length

#     writer.save()

