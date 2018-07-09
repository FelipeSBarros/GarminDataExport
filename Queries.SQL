WITH ordered AS (
 SELECT "name", track_seg_point_id, ST_SetSRID(wkb_geometry, 4326) as wkb_geometry
 FROM public.track_points order by track_seg_point_id
), tmp as (
select "name", st_makeline(st_transform(wkb_geometry, 32723)) as geom from ordered GROUP BY "name")
SELECT "name", round(sum(ST_Length(geom))::numeric, 3)
FROM tmp
GROUP BY "name"
ORDER BY "name" limit 2
