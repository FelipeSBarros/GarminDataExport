WITH ordered AS (
 SELECT "name", track_seg_point_id, ST_SetSRID(wkb_geometry, 4326) as wkb_geometry
 FROM public.track_points order by track_seg_point_id
), tmp as (
select "name", st_makeline(st_transform(wkb_geometry, 32723)) as geom from ordered GROUP BY "name")
SELECT "name", round(sum(ST_Length(geom))::numeric, 3)
FROM tmp
GROUP BY "name"
ORDER BY "name" limit 2


--Altering SRID

CREATE TABLE Geomtest as select * from track_points limit 5

select * from Geomtest 

UPDATE Geomtest SET wkb_geometry = ST_SetSRID(wkb_geometry, 4326);

select st_srid(wkb_geometry) from Geomtest 
select st_srid(wkb_geometry) from track_points

-- delta time
select * from Geomtest 
-- Difference between two timestamp
with date1 as (select "time" as t1 from track_points where "name" = '2662026807' and ogc_fid = 1),
date2 as (select "time" as t2 from track_points where "name" = '2662026807' and ogc_fid = 5)
  SELECT d1.t1 - d2.t2 from date1 d1, date2 d2 ;
