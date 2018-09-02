select * from track_points where "idGarmin" = 2372283405
select * from tracks where "idGarmin" = 2372283405
select * from partials where "idGarmin" = 2372283405
select * from summary where "idGarmin" = 2372283405

--track_points:
--track_seg_point_id, ele, time, geometry

--tracks:
--name, type, geometry

-- Creating VIEWS
CREATE OR REPLACE VIEW IF EXISTS viewtp as select 
	track_seg_point_id, ele, time, geometry from track_points 
	where "idGarmin" = 2372283405 order by track_seg_point_id

-- Tracks
CREATE OR REPLACE VIEW trackview as 
	with stime as (select 
	"time"(time) as start_time,
	 temp."idGarmin" as id
	 from track_points as temp where "idGarmin"=2372283405 and 
	 track_seg_point_id = '0')

select 
	t."idGarmin", t.name, t.type, t.geometry,
	 stime.start_time,
	 s."Time" as tempo,
	 "interval"(stime.start_time) + "time"(s."Time") as end_time
	from stime join tracks as t on stime.id = t."idGarmin"
	join summary as s on t."idGarmin" = s."idGarmin" 
	

	 
-- palying with time:
SELECT
    time,
    EXTRACT (DAY FROM time) as day,
    EXTRACT (MONTH FROM time) as month,
    EXTRACT (YEAR FROM time) as year,
    EXTRACT (HOUR FROM time) as hour,
    EXTRACT (MINUTE FROM time) as minute, 
    EXTRACT (SECOND FROM time) as second,
    EXTRACT (milliseconds FROM time) as milliseconds
    from track_points 
	where "idGarmin" = 2372283405 order by track_seg_point_id; 
-- Trying to create time interval

SELECT
    time,
    time - lag(time) over (order by time) as increase
    from track_points 
	where "idGarmin" = 2372283405 order by track_seg_point_id; 

select time '1970-01-01 09:00';
select time '01:00:00' + interval '3 hours'
SELECT TO_TIMESTAMP('2017-03-31 9:30:20','HH24:MI:SS');

--SELECT pg_catalog.time(column_name) AS myTime
select "time"(temp.time)
	 from track_points as temp where "idGarmin"=2372283405 and 
	 track_seg_point_id = '0'

-- getting start time and end time
with stime as (select 
	"time"(time) as start_time,
	 temp."idGarmin" as id
	 from track_points as temp where "idGarmin"=2372283405 and 
	 track_seg_point_id = '0')
	 select 
	 stime.start_time ,
	 s."Time" as tempo,
	 "interval"(stime.start_time) + "time"(s."Time") as end_time
	from stime 
	join summary as s on stime.id = s."idGarmin"
	where stime.id = 2372283405


-- QGIS
select t."idGarmin", t.geometry, s."Time" 
from tracks as t join summary as s on 
t."idGarmin" = s."idGarmin" where t."idGarmin" = 2372283405