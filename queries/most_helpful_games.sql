-- This query retrieves the top 40 games with the highest number of helpful recommendations.

with helpful_total as (select app_id,sum(helpful) as helpful_count
from recommendations group by app_id order by helpful_count desc limit 40)
select g.app_id,g.title,g.rating,h.helpful_count from games g join helpful_total h 
on g.app_id = h.app_id;