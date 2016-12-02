-- MAP REDUCE HIVE

drop table if exists pop;
create external table pop (
    SUMLEV int
    ,REGION int
    ,DIVISION int
    ,state int
    ,COUNTY int
    ,STNAME string
    ,CTYNAME string
    ,CENSUS2010POP int
    ,ESTIMATESBASE2010 int
    ,POPESTIMATE2010 int
    ,POPESTIMATE2011 int
    ,POPESTIMATE2012 int
    ,POPESTIMATE2013 int
    ,POPESTIMATE2014 int
    ) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' 
    STORED as TEXTFILE LOCATION 's3://fridaybucket/hiveInput/';


-- Run a query interactively, population by state

select stname, sum(popestimate2014) from pop where sumlev=50 group by stname;


-- Create a mapping back to S3

drop table if exists state_pop;
create external table state_pop (
    STNAME string, POP_EST_2014 int
    ) row format delimited fields terminated by ','
    lines terminated by '\n' 
    STORED as TEXTFILE LOCATION 's3://fridaybucket/hiveOutput/';


-- Re-run the query and save the data to s3

insert OVERWRITE table state_pop select stname, sum(popestimate2014) from pop where sumlev=50 group by stname;
