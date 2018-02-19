---
title: "Practice SQL with Google Big Querry"
layout: post
excerpt: "Practice SQL with Google Big Querry in 10 Minutes"
categories:
  - Tutorial
  - Data Manipulation
tags:
  - SQL
  - ETL
  - Google Big Querry

last_modified_at: 2018-02-20T12:43:31-05:00
---

SQL is useful, and a great introduction is by using Google Big Querry.  In this example, I access Google Big Querry with SQL.

![useful image]({{ site.url }}/assets/css/boston_data_story/Heading.PNG)


```sql
#Which player had the most home runs?
SELECT count(outcomeDescription) AS number_of_homeruns, 
       #Combines first and last name 
       CONCAT(hitterFirstName, " ", hitterLastName) as name

#The syntax is [bigquery-public-data][name of database].[name of table]
FROM [bigquery-public-data:baseball.games_wide]

#Only look at Red Sox players as the bottom of the inning is when the home team bats
WHERE ((homeTeamName = "Red Sox" AND inningHalf = "BOT") OR (awayTeamName = "Red Sox" AND inningHalf = "TOP")) 
AND outcomeDescription = "Homerun"

#Aggregate by player
GROUP BY name
#Sort the output to be in descending order
ORDER BY number_of_homeruns DESC
```


