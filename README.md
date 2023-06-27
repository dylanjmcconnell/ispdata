# ispdata
A basic python package for wrangling the input data used in [AEMO's Integrated System Plan (ISP)](https://aemo.com.au/en/energy-systems/major-publications/integrated-system-plan-isp/2022-integrated-system-plan-isp). 

AEMO publishes a huge range of input data, in a variety of formats (typically zip files and excel spreadsheets). The longer term goal is to make this data available in more useful and machine readable formats for use in other modelling excercises. 

This repository is intended to help convert the data to these more standard and useful (hopefully) formats, but also maintain a record and provide some degree of "data provenance". I am hoping (🤞) that the documentation of this (...when it exists) will be able to provide a useful resource for people trying to use and understand this AEMO data.

You could use this to manage the data yourself locally (note: there are some quite big datasets). But also hopefully you won't have to - there will be some resouce (tbc) where you can access the process data yourself, with appropriate documentation on how it was developed etc. 

## data

A (very) non-exhaustive list of the data includes:
- Trace data:
    - solar & wind
    - demand data
    - rooftop PV
    - electric vehicles
- Generator data:
    - capital cost
    - variable & fixed O&M
    - fuel costs
    - emmission rates
    - ...etc etc

# installation

So far this has been built with `pipenv` on linux with python version 3.11.4. If you did want play around with it, the best way to install would be clone the package and run `pipenv install` from the working directory.

You'll need to creata a `config.yml` in the `ispdata` directory (copy from the `config-example.yml` as approproiate). Basically needs you to elect a directory to download raw AEMO data to, and an other to store the processed / parsed data. 

###

p.s. this is extremely extremely pre-alpha so subject to lots of change
