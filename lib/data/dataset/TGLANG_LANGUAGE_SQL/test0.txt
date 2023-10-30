select distinct(CITY)
from STATION
where substr(CITY,1,1) in ('a','e','i','o','u'); 