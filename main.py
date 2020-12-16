import pandas as pd
import xlsxwriter, openpyxl, argparse, sys
from datetime import datetime

# Build the argument parser
parser = argparse.ArgumentParser(prog='BLM Reformatter')
parser.add_argument('--file', help = 'Path to the file that contains the raw data')
parser.add_argument('--month', help = 'Path to the file that contains the raw data')
args = parser.parse_args()

# custom imports from the local files
from field import field
from habitat import habitat
from sampleinfo import sample, samplehistory, personnel, locations

month_dict = {
    1: 'Jan',  2: 'Feb',  3: 'Mar',  4: 'Apr',
    5: 'May',  6: 'Jun',  7: 'Jul',  8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec',
}


# These will be used to subset the raw data
rawdatapath = args.file if args.file else "input/SCCWRP_SWAMP_FieldDataSheet.xlsx"

try:
    month = int(args.month) if args.month else None
except:
    raise Exception(f"The --month argument must be an integer from 1 to 12. You entered the value of {args.month}")


# this is the original dataset
sccwrp_field_results = pd.read_excel(rawdatapath, sheet_name = 'sccwrp_swamp_fielddatasheet_0')

# Project Name should always be Biotic Ligand Model
sccwrp_field_results = sccwrp_field_results[
    (sccwrp_field_results.SccwrpProjectName == 'BioticLigandModel')
    &
    ( True if month is None else sccwrp_field_results.SampleDate.apply(lambda x: x.month == month) )
]

# only run if there are records for the month they are asking for
if sccwrp_field_results.empty:
    print(f"No results found for month {month}")
    sys.exit()


# output file path to be used both times the file gets written
output_filepath = f"output/blm_swampformat_{month_dict[month] if month else ''}.xlsx"

# use xlsxwriter to write the data out without the resqualcode equal signs getting interpreted as formulas
# I am not sure if openpyxl also has a similar capability, but I do know how to do it with xlsxwriter
with \
pd.ExcelWriter(output_filepath, engine = 'xlsxwriter', options = {'strings_to_urls': False, 'strings_to_formulas': False}) \
as writer:
    
    # Call each function and write to excel
    sample(sccwrp_field_results).to_excel(writer, sheet_name = "Sample", index = False)
    samplehistory(sccwrp_field_results).to_excel(writer, sheet_name = "SampleHistory", index = False)
    personnel(sccwrp_field_results).to_excel(writer, sheet_name = "PersonnelDuty", index = False)
    locations(sccwrp_field_results).to_excel(writer, sheet_name = "Locations", index = False)
    field(sccwrp_field_results).to_excel(writer, sheet_name = "FieldResults", index = False)
    habitat(sccwrp_field_results).to_excel(writer, sheet_name = "HabitatResults", index = False)

    # Save it and we're done!
    writer.save()


# Use openpyxl to fit the columns to character width
# I remember researching this before, and i don't think xlsxwriter has this kind of feature
with pd.ExcelWriter(output_filepath, engine = 'openpyxl') as writer:
    writer.book = openpyxl.load_workbook(output_filepath)

    for worksheet in writer.book._sheets:
        for column_cells in worksheet.columns:
            length = max(len(str(cell.value) if cell.value else "") for cell in column_cells) + 2
            worksheet.column_dimensions[openpyxl.utils.get_column_letter(column_cells[0].column)].width = length

    writer.save()
    writer.close()

