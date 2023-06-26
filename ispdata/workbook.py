import os
from dataclasses import dataclass
import openpyxl
import pandas as pd

from ispdata import CONFIG 

def workbook(version="20201211.xlsx"):
    #"Draft 2021-22 Inputs and Assumptions Workbook.xlsx"    
    filepath = os.path.join(CONFIG["data_dir"], "workbooks", version)
    return openpyxl.open(filepath, data_only=True)

def worksheet(workbook, sheetname="Summary Mapping"):
    tables = SHEETS[sheetname]
    data = list(workbook[sheetname].values)    

    dataframes = {}
    for name, table in tables.items():
        dataframes[name] = df_from_table(data,table)
    return dataframes

def df_from_table(data, table):
    header = data[table.header][table.col_start:table.col_end]    
    rows = data[table.row_start: table.row_end]
    data = [row[table.col_start:table.col_end] for row in rows]
    df = pd.DataFrame(data, columns=header)
    return df.rename(columns={None: "Generator"})        
        
@dataclass
class Table:
    name: str
    header: int
    row_start: int
    row_end: int
    col_start: int
    col_end: int
