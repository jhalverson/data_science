-- Jonathan Halverson
-- Friday, December 9, 2016
-- (Based on the workshop by DataKitchen)
-- This Pig script loads a CSV file then filters the records,
-- groups the data by state and finally computes the populaion
-- of each state in the US

RAW = load 's3://piggyinputs/co-est2014-pop-data.csv' 
using PigStorage(',') as (
        SUMLEV: int
        ,REGION: int
        ,DIVISION: int
        ,STATE: int
        ,COUNTY: int
        ,STNAME: chararray
        ,CTYNAME: chararray
        ,CENSUS2010POP: int
        ,ESTIMATESBASE2010: int
        ,POPESTIMATE2010: int
        ,POPESTIMATE2011: int
        ,POPESTIMATE2012: int
        ,POPESTIMATE2013: int
        ,POPESTIMATE2014: int
);

-- select just the county level data
COUNTY_LIST = filter RAW by SUMLEV == 50;
-- dump COUNTY_LIST;

-- group by the state name
BY_STATE = group COUNTY_LIST by STNAME;
-- dump BY_STATE

-- do the sum
POP = foreach BY_STATE generate group as STNAME, SUM(COUNTY_LIST.POPESTIMATE2014);
-- dump POP;

-- save results to s3
STORE POP into 's3://piggyoutput/results-pig/' USING PigStorage (',');
