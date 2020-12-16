import pandas as pd
# Read in the relationship map
relmap = {
    'analytes' : pd.ExcelFile("input/RelationshipMap.xlsx").parse('Analytes'),
    'columns'  : pd.ExcelFile("input/RelationshipMap.xlsx").parse('Columns')   
}

# I could have totally not defined the relmap variable above.. 
# its ok though
relationships_analytes = relmap['analytes']
relationships_columns = relmap['columns']

# Literally the only purpose of this is to be able to get the columns in order
# These will be imported in each respective function to be used at the end in ordering the column names
sample_ordered_cols = pd.read_excel("info/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx", sheet_name = 'Sample').columns
samplehistory_ordered_cols = pd.read_excel("info/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx", sheet_name = 'SampleHistory').columns
personnel_ordered_cols = pd.read_excel("info/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx", sheet_name = 'PersonnelDuty').columns
locations_ordered_cols = pd.read_excel("info/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx", sheet_name = 'Locations').columns
field_ordered_cols = pd.read_excel("info/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx", sheet_name = 'FieldResults').columns
habitat_ordered_cols = pd.read_excel("info/BLM_Project_SWAMPformat_Field_CollectionResults.xlsx", sheet_name = 'HabitatResults').columns