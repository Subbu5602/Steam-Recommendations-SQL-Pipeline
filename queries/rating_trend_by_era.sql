-- This query retrieves the average positive ratio and the number of games for two different eras: "old" (released in 2013 or earlier) and "new" (released after 2013).

select case when strftime('%Y',date_release)<='2013' then "old" 
else "new" end as game_age, avg(positive_ratio) as avg_positive_ratio,
count(*) as num_of_games from games group by game_age;