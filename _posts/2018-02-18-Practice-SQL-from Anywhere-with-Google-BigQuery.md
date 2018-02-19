---
title: "Practice SQL from Anywhere with Google BigQuery"
layout: post
excerpt: "SQL is used ubiquitously for data manipulation, and although initially I found it challenging to set up an environment to practice on"
categories:
  - Tutorial
  - SQL
  - Data Manipulation
tags:
  - SQL
  - ETL
  - Google Big Querry

last_modified_at: 2018-02-20T12:43:31-05:00
---

SQL is used ubiquitously for data manipulation, and although initially I found it challenging to set up an environment to practice on, an easy solution is to use Google’s BigQuery platform.  This allows users to set up an account and run SQL queries on terabyte-scale databases in minutes.  Additionally, this can be run from anywhere, or on any platform or machine with a web browser.

## 1.	Setup

As of this date, Google’s 1-year free trial allows for $300 in credits.  This is more than sufficient to get up and running with the basics.  Users just [sign in](https://cloud.google.com/bigquery/?utm_source=google&utm_medium=cpc&utm_campaign=2015-q2-cloud-na-gcp-bkws-freetrial-en&gclid=Cj0KCQiA5aTUBRC2ARIsAPoPJk8e2GT7GPlmY5_kiRm48rSHg83aOh-bc3pXV3uTXceiR0fBeXPM2DQaAhWEEALw_wcB&dclid=CIiWjN6EsdkCFYOsyAodVd0MIw) with a google account.

[Google’s BigQuery tutorial:](https://cloud.google.com/bigquery/quickstart-web-ui)

Because Google's engineers are better at explaining this than I am.

[SQL Tutorial:](https://www.google.com/search?q=sql+tutorial)

Because there are already thousands of SQL tutorials out there.  BigQuery uses SQL standard 2011.

## 2.	 Select Data

Choose a table.  There are many data sets to choose from, including US Census Data, CMS Medical data, traffic fatalities, or about [200 years of digitalized book metadata](https://bigquery.cloud.google.com/dataset/gdelt-bq:hathitrustbooks?pli=1).

I chose the Baseball table (1.76GB), which has statistics from the 2016 MLB season.  Each row represents an event from an MLB game, such as a swinging strike, a foul ball, a ground out, etc.  The `Schema` shows the column names and character types.  Look at the `Preview` and `Details` pages for more info.  

Be careful about data usage, as the cost is determined by how much data is pulled from Google's servers.  For this example, I chose to limit the queries to only the Red Sox, and only Home Runs.  These queries were only about 30Mb in size.  Even with the `Limit xx` SQL clause, the full dataset needs to be processed by the server; my method was to use a `WHERE` clause, although there may be better ways of restricting the amount of data downloaded.

![useful image]({{ site.url }}/assets/css/google_big_query/schema.png)

## 3.  Run a Query

In this example, I want to know which Red Sox players had the most home runs during the 2016 season.  

```sql
/*Which player had the most home runs?*/
SELECT count(outcomeDescription) AS number_of_homeruns, 
       #Combines first and last name 
       CONCAT(hitterFirstName, " ", hitterLastName) as name

/*The syntax is [bigquery-public-data][name of database].[name of table]*/
FROM [bigquery-public-data:baseball.games_wide]

/*Only look at Red Sox players as the bottom of the inning is when the home team bats*/
WHERE ((homeTeamName = "Red Sox" AND inningHalf = "BOT") OR (awayTeamName = "Red Sox" AND inningHalf = "TOP")) 
AND outcomeDescription = "Homerun"

/*Aggregate by player*/
GROUP BY name
/*Sort the output to be in descending order*/
ORDER BY number_of_homeruns DESC
```

The output shows the number of home runs for each red sox player.  Notice the 38-homerun season from David Ortiz (AKA, Big Papi), the greatest DH of all time, on his final season with the Sox.

![useful image]({{ site.url }}/assets/css/google_big_query/query_output.png)

These data can be checked against the official MLB statistics recorded on [Baseball Reference](https://www.baseball-reference.com/teams/BOS/2016.shtml)

## 4.  Use the Output

There are many ways that the output from above could be exported.  For simplicity in this example, I copy the results to Google Sheets and can then create a graph of the output.  This is as easy as pressing `Save to Google Sheets` above the output.

![useful image]({{ site.url }}/assets/css/google_big_query/chart_output.png)

