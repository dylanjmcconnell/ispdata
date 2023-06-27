from io import BytesIO
import re
import zipfile
import pandas as pd 
import datetime
from ispdata import CONFIG

def parse(df: pd.DataFrame, value_name="MW"):
    """
    Function for parsing an AEMO dateframe (wide format, intervals as columns) to a
    long format (with datetime index) 
    """
    dx = df.melt(id_vars=["Year", "Month", "Day"], 
                 var_name="Interval",
                 value_name=value_name)
    dt_index = dx.apply(lambda x: row_to_datetime(x), axis=1)
    return dx.set_index(dt_index)[value_name]

def row_to_datetime(x: pd.Series):
    """
    Function to convert a row (with year, month, day and interal number) to a
    datetime object
    """
    return datetime.datetime(x.Year, x.Month, x.Day) + \
           datetime.timedelta(hours=int(x.Interval)/2-.5)

def extract_to_dataframe(zfile: zipfile.ZipFile, zipname: str):
    """
    Extracts `zipname` from ZipFile (`zfile`) as a pandas dataframe
    """
    with BytesIO() as f:
        f.write(zfile.read(zipname))
        f.seek(0)
        return pd.read_csv(f)
    
def _dataframe_generator(zipfilepath: str):
    """
    Generator that yields all csv files in zipfile as dataframes
    """
    with zipfile.ZipFile(zipfilepath) as zfile:
        for zipname in zfile.namelist():
            pattern = re.compile("(?i).*\.csv")
            if re.match(pattern, zipname):
                yield zipname, extract_to_dataframe(zfile, zipname)