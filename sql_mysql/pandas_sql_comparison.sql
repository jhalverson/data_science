Thursday, July 14, 2016

Sample insurance portfolio (download .csv file)

The sample insurance file contains 36,634 records in Florida for 2012 from a sample company that implemented an agressive growth plan in 2012.  There are total insured value (TIV) columns containing TIV from 2011 and 2012, so this dataset is great for testing out the comparison feature.  This file has address information that you can choose to geocode, or you can use the existing latitude/longitude in the file.


Upload file to:
http://www.convertcsv.com/csv-to-sql.htm

In Step 2, be sure to check "First row is column names"

If find ^M as line returns then in vi do: s/ctrl+v+m/\r/g

DROP TABLE mytable;

CREATE TABLE insur(
   policy_id          INTEGER  NOT NULL PRIMARY KEY 
  ,statecode          VARCHAR(2) NOT NULL
  ,county             VARCHAR(19) NOT NULL
  ,eq_site_limit      NUMERIC(11,1) NOT NULL
  ,hu_site_limit      NUMERIC(12,2) NOT NULL
  ,fl_site_limit      NUMERIC(11,1) NOT NULL
  ,fr_site_limit      NUMERIC(11,1) NOT NULL
  ,tiv_2011           NUMERIC(12,2) NOT NULL
  ,tiv_2012           NUMERIC(12,2) NOT NULL
  ,eq_site_deductible NUMERIC(9,1) NOT NULL
  ,hu_site_deductible NUMERIC(9,1) NOT NULL
  ,fl_site_deductible NUMERIC(8,1) NOT NULL
  ,fr_site_deductible INTEGER  NOT NULL
  ,point_latitude     NUMERIC(9,6) NOT NULL
  ,point_longitude    NUMERIC(10,6) NOT NULL
  ,line               VARCHAR(11) NOT NULL
  ,construction       VARCHAR(19) NOT NULL
  ,point_granularity  INTEGER  NOT NULL
);

The table can be made as a regular user. However, to fill the table one must
be root. Then do:

mysql> load data infile "/Users/jhalverson/data_science/sql_mysql/FL_insurance_sample_no_header.csv" into table insur columns terminated by ',' lines terminated by '\n';
Query OK, 36634 rows affected (0.81 sec)
Records: 36634  Deleted: 0  Skipped: 0  Warnings: 0


mysql> desc insur;
+--------------------+---------------+------+-----+---------+-------+
| Field              | Type          | Null | Key | Default | Extra |
+--------------------+---------------+------+-----+---------+-------+
| policy_id          | int(11)       | NO   | PRI | NULL    |       |
| statecode          | varchar(2)    | NO   |     | NULL    |       |
| county             | varchar(19)   | NO   |     | NULL    |       |
| eq_site_limit      | decimal(11,1) | NO   |     | NULL    |       |
| hu_site_limit      | decimal(12,2) | NO   |     | NULL    |       |
| fl_site_limit      | decimal(11,1) | NO   |     | NULL    |       |
| fr_site_limit      | decimal(11,1) | NO   |     | NULL    |       |
| tiv_2011           | decimal(12,2) | NO   |     | NULL    |       |
| tiv_2012           | decimal(12,2) | NO   |     | NULL    |       |
| eq_site_deductible | decimal(9,1)  | NO   |     | NULL    |       |
| hu_site_deductible | decimal(9,1)  | NO   |     | NULL    |       |
| fl_site_deductible | decimal(8,1)  | NO   |     | NULL    |       |
| fr_site_deductible | int(11)       | NO   |     | NULL    |       |
| point_latitude     | decimal(9,6)  | NO   |     | NULL    |       |
| point_longitude    | decimal(10,6) | NO   |     | NULL    |       |
| line               | varchar(11)   | NO   |     | NULL    |       |
| construction       | varchar(19)   | NO   |     | NULL    |       |
| point_granularity  | int(11)       | NO   |     | NULL    |       |
+--------------------+---------------+------+-----+---------+-------+


mysql> select avg(point_latitude), min(point_latitude), max(point_latitude), stddev(point_latitude) from insur;
+---------------------+---------------------+---------------------+------------------------+
| avg(point_latitude) | min(point_latitude) | max(point_latitude) | stddev(point_latitude) |
+---------------------+---------------------+---------------------+------------------------+
|       28.0874765122 |           24.547514 |           30.989820 |     1.6477116104781675 |
+---------------------+---------------------+---------------------+------------------------+


select county, count(county) from insur group by county order by count(county) desc;
+---------------------+---------------+
| county              | count(county) |
+---------------------+---------------+
| MIAMI DADE COUNTY   |          4315 |
| BROWARD COUNTY      |          3193 |
| PALM BEACH COUNTY   |          2791 |
| DUVAL COUNTY        |          1894 |
| ORANGE COUNTY       |          1811 |
| PINELLAS COUNTY     |          1774 |
| POLK COUNTY         |          1629 |
| VOLUSIA COUNTY      |          1367 |
| HILLSBOROUGH COUNTY |          1166 |
| MARION COUNTY       |          1138 |
| OKALOOSA COUNTY     |          1115 |
| SEMINOLE COUNTY     |          1100 |
| ALACHUA COUNTY      |           973 |
| BREVARD COUNTY      |           872 |
...


# avg total insured value difference by construction material of the property
mysql> select construction, avg(tiv_2012 - tiv_2011) from insur group by construction;
+---------------------+--------------------------+
| construction        | avg(tiv_2012 - tiv_2011) |
+---------------------+--------------------------+
| Masonry             |            181117.849026 |
| Reinforced Concrete |           3561250.852741 |
| Reinforced Masonry  |            796516.138596 |
| Steel Frame         |          16508382.352941 |
| Wood                |             19777.946735 |
+---------------------+--------------------------+

# a simple example of the where clause
mysql> select policy_id, tiv_2011, tiv_2012, construction from insur where construction='wood' and (tiv_2012 - tiv_2011 > 250000.0);
+-----------+-----------+-----------+--------------+
| policy_id | tiv_2011  | tiv_2012  | construction |
+-----------+-----------+-----------+--------------+
|    118775 | 349906.50 | 600607.51 | Wood         |
|    222173 | 355414.25 | 649046.12 | Wood         |
|    226317 | 303766.20 | 566463.21 | Wood         |
|    307614 | 342198.00 | 605323.62 | Wood         |
|    321321 | 293965.28 | 545011.62 | Wood         |
|    412421 | 358402.50 | 611365.85 | Wood         |
|    437709 | 359482.50 | 610030.30 | Wood         |
|    476120 | 356865.79 | 623665.79 | Wood         |
|    584847 | 326592.00 | 592326.85 | Wood         |
|    640441 | 354681.00 | 610388.27 | Wood         |
|    758391 | 341280.46 | 634269.73 | Wood         |
|    856215 | 350161.20 | 602679.25 | Wood         |
|    870827 | 348955.20 | 609223.44 | Wood         |
|    925819 | 343412.76 | 594724.62 | Wood         |
|    948662 | 339359.71 | 602122.54 | Wood         |
|    969495 | 357947.10 | 608309.62 | Wood         |
|    975826 | 353849.81 | 607132.67 | Wood         |
+-----------+-----------+-----------+--------------+
17 rows in set (0.03 sec)


mysql> select distinct county from insur where county like '%c%m%';
+-----------------+
| county          |
+-----------------+
| ESCAMBIA COUNTY |
| COLUMBIA COUNTY |
+-----------------+
2 rows in set (0.02 sec)


# defining variables
mysql> select @ax := avg(tiv_2011) from insur;
+----------------------+
| @ax := avg(tiv_2011) |
+----------------------+
|    2172875.000322924 |
+----------------------+

mysql> select sum(@ax - tiv_2012) from insur;
+---------------------------------------------+
| sum(@ax - tiv_2012)                         |
+---------------------------------------------+
| -14585061340.200002184000000000000000000000 |
+---------------------------------------------+

# computing the correlation in SQL
create table sample( x float not null, y float not null );
insert into sample values (1, 10), (2, 4), (3, 5), (6,17);

select @ax := avg(x), 
       @ay := avg(y), 
       @div := (stddev_samp(x) * stddev_samp(y))
from sample;

select sum( ( x - @ax ) * (y - @ay) ) / ((count(x) -1) * @div) from sample;
+---------------------------------------------------------+
| sum( ( x - @ax ) * (y - @ay) ) / ((count(x) -1) * @div) |
+---------------------------------------------------------+
|                                       0.700885077729073 |
+---------------------------------------------------------+
