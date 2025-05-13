import pandas as pd
from utils.SchemaRegistry import ValidSchemas
def validate(data: pd.DataFrame, fileName: str) -> bool:
    if fileName in ValidSchemas.keys():
        expected_columns = ValidSchemas[fileName].keys()
        if not all(col in data.columns for col in expected_columns):
            print(f"DataFrame does not have the expected columns for {fileName}.")
            return False
        
        for col, expected_type in ValidSchemas[fileName].items():
            if not pd.api.types.is_dtype_equal(data[col].dtype, expected_type):
                print(f"Column {col} in DataFrame does not have the expected type for {fileName}.")
                return False
            
    else :
        print(f"File name {fileName} is not recognized.")
        return False
    return True  

        



        