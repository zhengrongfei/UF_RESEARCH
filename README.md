## Introduction
In this project, we try to use photos of streets to find some sociological information using machine learning methods. For example, the relationship between the number of cars in the street and the average value of property in the street, and we also have some other hypotheses, such as whether the percentage of Japanese cars in the street is related to the average education level in that street.

## Timeline

 
### Gather Information
- Read through the example papers 
- Understand data
- Find coding resources


## Methodology

### data collection

intro: FIPS Place Codes: Used to identify cities, towns, and villages in the United States. These codes are essential for describing and analyzing geographic location information in census data.

Image source：Google Street View API

Number of pictures: 20000

Number of FIPS: 200 randomly 

Number of images per FIPS: 100


### data analysis and cleaning 

intro:For all the downloaded street maps, use the API to recognize vehicles, including the number, brand, types, and series.The recognized data is stored in a database and output to a csv table after performing relevant statistical operations, including counting information such as the number of vehicles in a fips area.

API: tecentcloud api

Database: MySQL


### modeling 


