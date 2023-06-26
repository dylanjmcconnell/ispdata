"""Module to manage and download ISP files from AEMO"""

import os
import datetime
from io import BytesIO
from hashlib import sha1
import requests
import pandas as pd
from tqdm import tqdm
from ispdata import CONFIG

def download_file(url, block_size=1024):
    """Function to download, and archive AEMO files"""
    headers = {"User-Agent": CONFIG['user_agent']}
    response = requests.get(url, headers=headers, stream=True)

    pbar = None
    total_size = int(response.headers.get('content-length', 0))
    pbar = tqdm(total=total_size, unit='iB', unit_scale=True)
    pbar.set_description("Downloading {0}".format(url.split("/")[-1]))

    fileobj = BytesIO()
    for data in response.iter_content(block_size):
        pbar.update(len(data))
        fileobj.write(data)
    fileobj.seek(0)

    pbar.close()

    return response, fileobj

def download_traces(dataset="2022-final"):
    traces = CONFIG['aemo_datasets'][dataset]["trace-data"].values()
    urls = [url for trace in traces for url in trace]
    for url in urls:
        _, fileobj = download_file(url, block_size=1024)
        archive_file(fileobj=fileobj, subdir=dataset, filename=url.split("/")[-1])

def download_workbook(dataset="2022-final"):
    """Function to download, and archive workbook"""
    url=CONFIG['aemo_datasets'][dataset]['workbook']
    response, fileobj = download_file(url=url, description="latest workbook")
    date = parse_date(response)
    process_response(response, fileobj, subdir="workbooks", filename=date, _format="xlsx")

def parse_date(response):
    """Function parse date from Last-Modified field in headers"""
    last_modified = response.headers['Last-Modified']
    last_modified = datetime.datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    return last_modified.strftime("%Y%m%d")

def process_response(response, fileobj, subdir, filename, _format):
    """Function to check and store metadata of different files
    (for maintain version control of different AEMO input files)
    Checks reponse and metadata againts locally downloaded data"""
    metadata = response.headers
    checksum = sha1(fileobj.read()).hexdigest()
    fileobj.seek(0)
    meta_df = pd.DataFrame.from_dict(metadata, orient="index").T
    meta_df['Checksum'] = checksum

    filepath = os.path.join(CONFIG['source_data_dir'], "file_log.csv")
    try:
        df_log = pd.read_csv(filepath, index_col=None)
        if checksum not in df_log.Checksum.values:
            meta_df = df_log.append(meta_df)
            archive_file(fileobj, subdir, filename, _format)
        else:
            print ("Aready up todate")

    except OSError as error:
        print(error.args)
        archive_file(fileobj, subdir, filename, _format)


    meta_df.to_csv(filepath, index=None)

def archive_file(fileobj, subdir, filename):
    """Function to save file (filename) in particular format and subdir"""
    path = os.path.join(CONFIG['source_data_dir'], subdir)
    os.makedirs(path, exist_ok=True)

    filepath =  os.path.join(path, filename)

    with open(filepath, 'wb') as _file:
        _file.write(fileobj.read())