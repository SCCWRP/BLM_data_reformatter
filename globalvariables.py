import pandas as pd
# Read in the relationship map
relmap = {
    'analytes' : pd.ExcelFile("input/RelationshipMap.xlsx").parse('Analytes'),
    'columns'  : pd.ExcelFile("input/RelationshipMap.xlsx").parse('Columns'),
    'aliases'  : pd.ExcelFile("input/RelationshipMap.xlsx").parse('Aliases'),
}

relmap['aliases'] = relmap['aliases'].dropna()

# I could have totally not defined the relmap variable above.. 
# its ok though
relationships_analytes = relmap['analytes']
relationships_columns = relmap['columns']

# Literally the only purpose of this is to be able to get the columns in order
# These will be imported in each respective function to be used at the end in ordering the column names
template_path = "info/SWAMP_Field_CollectionResults_Template_v2.5_081420.xlsx"
sample_ordered_cols = pd.read_excel(template_path, sheet_name = 'Sample').columns
samplehistory_ordered_cols = pd.read_excel(template_path, sheet_name = 'SampleHistory').columns
personnel_ordered_cols = pd.read_excel(template_path, sheet_name = 'PersonnelDuty').columns
locations_ordered_cols = pd.read_excel(template_path, sheet_name = 'Locations').columns
field_ordered_cols = pd.read_excel(template_path, sheet_name = 'FieldResults').columns
habitat_ordered_cols = pd.read_excel(template_path, sheet_name = 'HabitatResults').columns