import pandas as pd

try:
    df = pd.read_excel('students.xlsx')
    print("Excel file contents:")
    print("=" * 50)
    print(df.to_string())
    print("=" * 50)
    print("Columns:", df.columns.tolist())
    print("Data types:", df.dtypes.to_dict())
except Exception as e:
    print("Error reading Excel file:", str(e))
