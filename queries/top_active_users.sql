-- This query retrieves the top 30 most active users based on the number of reviews they have written, along with their purchased products and the games they recommended.

with top_active_users as 
(select user_id, products from users order by reviews desc limit 30) 
select t.user_id,t.products as 'Products Bought', r.app_id,r.hours,g.title,
g.rating,g.positive_ratio from top_active_users t join recommendations r 
on t.user_id=r.user_id join games g on r.app_id = g.app_id limit 70;