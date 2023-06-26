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

SHEETS = {"Summary Mapping": 
             {"Existing Generator": Table(name="Existing Generator", header=3, row_start=6, row_end=208, col_start=0, col_end=-1),
              "New Entrant": Table(name="New Entrant", header=3, row_start=261, row_end=443, col_start=0, col_end=-1)},
         "Build costs": 
             {"Central": Table(name="Central", header=11, row_start=12, row_end=31, col_start=0, col_end=-1),
             },
         "Gas and Liquid fuel price": 
             {"Existing, central": Table("Existing, central", header=9, row_start=10, row_end=44, col_start=1, col_end=-3),
              "New, central": Table("New, central", header=9, row_start=45, row_end=55, col_start=1, col_end=-3),
              "Existing, step change": Table("Existing, step change", header=58, row_start=59, row_end=93, col_start=1, col_end=-3),
              "New, step change": Table("New, step change", header=58, row_start=94, row_end=104, col_start=1, col_end=-3),
              "Existing, gas": Table("Existing, gas", header=156, row_start=157, row_end=191, col_start=1, col_end=-3),
              "New, gas": Table("New, gas", header=156, row_start=192, row_end=202, col_start=1, col_end=-3)}
         }

def header_mod(header, *a):
    header_list = list(header)
    a
    return a


def data_melt(table):
    None

def gas_merge(ws, tech="New"):
    tables = ["{0}, central".format(tech),
              "{0}, step change".format(tech),
              "{0}, gas".format(tech)]

    data = [ws[i] for i in tables]

    df = pd.concat(data)

    df['Region'] = df.Generator.apply(lambda x: x.split(" ")[0]) 
    df.Generator = df.Generator.apply(lambda x: x.split(" ")[-1]) 

    return df.melt(id_vars=["Region", "Generator", "Gas price scenario"], value_name="Price", var_name = "FY")