import pandas as pd
import xlsxwriter

# custom imports from the local files
from field import field
from habitat import habitat
from sampleinfo import sample, samplehistory, personnel, locations

# strings to formulas set to false, because that ResQualCode equal sign was being interpreted as an excel formula
writer = pd.ExcelWriter(
    "output/blm_swampformat.xlsx",
    engine = 'xlsxwriter',
    options = {
        'strings_to_urls': False,
        'strings_to_formulas': False
    }
)

# Call each function and write to excel
sample().to_excel(writer, sheet_name = "Sample", index = False)
samplehistory().to_excel(writer, sheet_name = "SampleHistory", index = False)
personnel().to_excel(writer, sheet_name = "PersonnelDuty", index = False)
locations().to_excel(writer, sheet_name = "Locations", index = False)
field().to_excel(writer, sheet_name = "FieldResults", index = False)
habitat().to_excel(writer, sheet_name = "HabitatResults", index = False)

# Save it and we're done!
writer.save()