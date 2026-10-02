-- this query retrieves the distribution of playtime for recommended games, specifically focusing on whether users have played over 200 hours or not.

select case when hours>200 then 'yes' else 'no' end as played_over_200,
count(*) as num_reviews, round(100.0*count(*)/(select count(*) from recommendations 
where is_recommended=1),1) as percent_recommended from recommendations
where is_recommended = 1 group by played_over_200;