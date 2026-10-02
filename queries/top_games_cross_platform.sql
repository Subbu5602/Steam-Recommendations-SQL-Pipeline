-- This query retrieves the top 50 games with the highest reviews with their rating and cross platform score which is calculated by adding the number of platforms the game is available on (Windows, Mac, Linux).

select app_id,title,rating,user_reviews,win+mac+linux as cross_platform_score
from games order by user_reviews desc
limit 50;