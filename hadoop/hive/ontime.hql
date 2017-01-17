-- Jonathan Halverson
-- Friday, January 13, 2017

-- Here is the query for MySQL
-- select a.description, count(f.arrival_time) as cnt, avg(f.arrival_delay) as Average_Delay from flights f join airlines a on f.airline_id=a.code group by a.description order by Average_Delay;


drop table if exists flights;
create external table flights (
    flight_date date
    ,airline_id int
    ,flight_num int
    ,origin string
    ,destination string
    ,departure_time int
    ,departure_delay float
    ,arrival_time int
    ,arrival_delay float
    ,air_time float
    ,distance float
    ) ROW FORMAT DELIMITED FIELDS TERMINATED by ','
    STORED as TEXTFILE LOCATION 's3://fridaybucket/flights.csv';

drop table if exists airlines;
create external table airlines (code int, description string) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' STORED as TEXTFILE LOCATION 's3://fridaybucket/airlines.csv';


-- Run a query interactively, population by state

select a.description, count(f.arrival_delay) as cnt, avg(f.arrival_delay) as Average_Delay from flights f join airlines a on (f.airline_id=a.code) group by a.description order by Average_Delay desc;


-- Create a mapping back to S3

drop table if exists avg_flight_delay;
create external table avg_flight_delay (
    AIRLINE string, AVERAGE_DELAY float
    ) row format delimited fields terminated by ','
    lines terminated by '\n' 
    STORED as TEXTFILE LOCATION 's3://fridaybucket/hiveOutput/';


-- Re-run the query and save the data to s3

insert OVERWRITE table avg_flight_delay select a.description, count(f.arrival_delay) as cnt, avg(f.arrival_delay) as Average_Delay from flights f join airlines a on (f.airline_id=a.code) group by a.description order by Average_Delay desc;
