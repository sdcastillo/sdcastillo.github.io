# Data manipulation




About two hours in this exam will be spent just on data manipulation.  Putting in extra practice in this area is garanteed to give you a better score because it will free up time that you can use elsewhere.

Suggested reading of *R for Data Science* (https://r4ds.had.co.nz/index.html):


| Chapter | Topic           |
|---------|-----------------|
| 9       | Introduction    |
| 10      | Tibbles         |
| 12      | Tidy data       |
| 15      | Factors         |
| 16      | Dates and times |
| 17      | Introduction    |
| 18      | Pipes           |
| 19      | Functions       |
| 20      | Vectors         |


All data for this book can be accessed from the package `ExamPAData`.  In the real exam, you will read the file from the Prometric computer.  To read files into R, the [readr](https://readr.tidyverse.org/articles/readr.html) package has several tools, one for each data format.  For instance, the most common format, comma separated values (csv) are read with the `read_csv()` function.

Because the data is already loaded, simply use the below code to access the data.


```r
library(ExamPAData)
```


## Look at the data

The data that we are using is `health_insurance`, which has information on patients and their health care costs.

The descriptions of the columns are below.  The technical name for this is a "data dictionary", and one will be provided to you on the real exam.

- `age`: Age of the individual
- `sex`: Sex
- `bmi`: Body Mass Index
- `children`: Number of children
- `smoker`: Is this person a smoker?
- `region`: Region
- `charges`: Annual health care costs.

`head()` shows the top n rows.  `head(20)` shows the top 20 rows.  


```r
library(tidyverse)
head(health_insurance)
```

```
## # A tibble: 6 x 7
##     age sex      bmi children smoker region    charges
##   <dbl> <chr>  <dbl>    <dbl> <chr>  <chr>       <dbl>
## 1    19 female  27.9        0 yes    southwest  16885.
## 2    18 male    33.8        1 no     southeast   1726.
## 3    28 male    33          3 no     southeast   4449.
## 4    33 male    22.7        0 no     northwest  21984.
## 5    32 male    28.9        0 no     northwest   3867.
## 6    31 female  25.7        0 no     southeast   3757.
```

Using a pipe is an alternative way of doing this. Because this is more time-efficient, this will be the preferred method in this manual.  


```r
health_insurance %>% head()
```

The `glimpse` function is a transpose of the `head()` function, which can be more spatially efficient.  This also gives you the dimension (1,338 rows, 7 columns).


```r
health_insurance %>% glimpse()
```

```
## Observations: 1,338
## Variables: 7
## $ age      <dbl> 19, 18, 28, 33, 32, 31, 46, 37, 37, 60, 25, 62, 23, 5...
## $ sex      <chr> "female", "male", "male", "male", "male", "female", "...
## $ bmi      <dbl> 27.900, 33.770, 33.000, 22.705, 28.880, 25.740, 33.44...
## $ children <dbl> 0, 1, 3, 0, 0, 0, 1, 3, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0,...
## $ smoker   <chr> "yes", "no", "no", "no", "no", "no", "no", "no", "no"...
## $ region   <chr> "southwest", "southeast", "southeast", "northwest", "...
## $ charges  <dbl> 16884.924, 1725.552, 4449.462, 21984.471, 3866.855, 3...
```

One of the most useful data science tools is counting things.  The function `count()` gives the number of records by a categorical feature.   


```r
health_insurance %>% count(children)
```

```
## # A tibble: 6 x 2
##   children     n
##      <dbl> <int>
## 1        0   574
## 2        1   324
## 3        2   240
## 4        3   157
## 5        4    25
## 6        5    18
```

Two categories can be counted at once.  This creates a table with all combinations of `cut` and `color` and shows the number of records in each category.


```r
health_insurance %>% count(region, sex)
```

```
## # A tibble: 8 x 3
##   region    sex        n
##   <chr>     <chr>  <int>
## 1 northeast female   161
## 2 northeast male     163
## 3 northwest female   164
## 4 northwest male     161
## 5 southeast female   175
## 6 southeast male     189
## 7 southwest female   162
## 8 southwest male     163
```

The `summary()` function is shows a statistical summary.  One caveat is that each column needs to be in it's appropriate type.  For example, `smoker`, `region`, and `sex` are all listed as characters when if they were factors, `summary` would give you count info.

**With incorrect data types**


```r
health_insurance %>% summary()
```

```
##       age            sex                 bmi           children    
##  Min.   :18.00   Length:1338        Min.   :15.96   Min.   :0.000  
##  1st Qu.:27.00   Class :character   1st Qu.:26.30   1st Qu.:0.000  
##  Median :39.00   Mode  :character   Median :30.40   Median :1.000  
##  Mean   :39.21                      Mean   :30.66   Mean   :1.095  
##  3rd Qu.:51.00                      3rd Qu.:34.69   3rd Qu.:2.000  
##  Max.   :64.00                      Max.   :53.13   Max.   :5.000  
##     smoker             region             charges     
##  Length:1338        Length:1338        Min.   : 1122  
##  Class :character   Class :character   1st Qu.: 4740  
##  Mode  :character   Mode  :character   Median : 9382  
##                                        Mean   :13270  
##                                        3rd Qu.:16640  
##                                        Max.   :63770
```

**With correct data types**

This tells you that there are 324 patients in the northeast, 325 in the northwest, 364 in the southeast, and so fourth.


```r
health_insurance <- health_insurance %>% 
  modify_if(is.character, as.factor)

health_insurance %>% 
  summary()
```

```
##       age            sex           bmi           children     smoker    
##  Min.   :18.00   female:662   Min.   :15.96   Min.   :0.000   no :1064  
##  1st Qu.:27.00   male  :676   1st Qu.:26.30   1st Qu.:0.000   yes: 274  
##  Median :39.00                Median :30.40   Median :1.000             
##  Mean   :39.21                Mean   :30.66   Mean   :1.095             
##  3rd Qu.:51.00                3rd Qu.:34.69   3rd Qu.:2.000             
##  Max.   :64.00                Max.   :53.13   Max.   :5.000             
##        region       charges     
##  northeast:324   Min.   : 1122  
##  northwest:325   1st Qu.: 4740  
##  southeast:364   Median : 9382  
##  southwest:325   Mean   :13270  
##                  3rd Qu.:16640  
##                  Max.   :63770
```

## Transform the data

Transforming, manipulating, querying, and wrangling are all words for the task of changing the values in a data frame. For those Excel users out there, this can be interpreted as "what Pivot tables, VLOOKUP, INDEX/MATCH, and SUMIFF do". 

R syntax is designed to be similar to SQL.  They begin with a `SELECT`, use `GROUP BY` to aggregate, and have a `WHERE` to remove records.  Unlike SQL, the ordering of these does not matter.  `SELECT` can come after a `WHERE`.

**R to SQL translation**

```
select() -> SELECT
mutate() -> user-defined columns
summarize() -> aggregated columns
left_join() -> LEFT JOIN
filter() -> WHERE
group_by() -> GROUP BY
filter() -> HAVING
arrange() -> ORDER BY

```


```r
health_insurance %>% 
  select(age, region) %>% 
  head()
```

```
## # A tibble: 6 x 2
##     age region   
##   <dbl> <fct>    
## 1    19 southwest
## 2    18 southeast
## 3    28 southeast
## 4    33 northwest
## 5    32 northwest
## 6    31 southeast
```

Tip: use `CTRL + SHIFT + M` to create pipes `%>%`.

Let's look at only those in the southeast region.  Instead of `WHERE`, use `filter`.


```r
health_insurance %>% 
  filter(region == "southeast") %>% 
  select(age, region) %>% 
  head()
```

```
## # A tibble: 6 x 2
##     age region   
##   <dbl> <fct>    
## 1    18 southeast
## 2    28 southeast
## 3    31 southeast
## 4    46 southeast
## 5    62 southeast
## 6    56 southeast
```

The SQL translation is


```sql
SELECT age, region
FROM health_insurance
WHERE region = 'southeast'
```


Instead of `ORDER BY`, use `arrange`.  Unlike SQL, the order does not matter and `ORDER BY` doesn't need to be last.


```r
health_insurance %>% 
  arrange(age) %>% 
  select(age, region) %>% 
  head()
```

```
## # A tibble: 6 x 2
##     age region   
##   <dbl> <fct>    
## 1    18 southeast
## 2    18 southeast
## 3    18 northeast
## 4    18 northeast
## 5    18 northeast
## 6    18 southeast
```

The `group_by` comes before the aggregation, unlike in SQL where the `GROUP BY` comes last.


```r
health_insurance %>% 
  group_by(region) %>% 
  summarise(avg_age = mean(age))
```

```
## # A tibble: 4 x 2
##   region    avg_age
##   <fct>       <dbl>
## 1 northeast    39.3
## 2 northwest    39.2
## 3 southeast    38.9
## 4 southwest    39.5
```

In SQL, this would be


```sql
SELECT region, 
       AVG(age) as avg_age
FROM health_insurance
GROUP BY region
```


Just like in SQL, many different aggregate functions can be used such as `SUM`, `MEAN`, `MIN`, `MAX`, and so forth.


```r
health_insurance %>% 
  group_by(region) %>% 
  summarise(avg_age = mean(age),
            max_age = max(age),
            median_charges = median(charges),
            bmi_std_dev = sd(bmi))
```

```
## # A tibble: 4 x 5
##   region    avg_age max_age median_charges bmi_std_dev
##   <fct>       <dbl>   <dbl>          <dbl>       <dbl>
## 1 northeast    39.3      64         10058.        5.94
## 2 northwest    39.2      64          8966.        5.14
## 3 southeast    38.9      64          9294.        6.48
## 4 southwest    39.5      64          8799.        5.69
```

To create new columns, the `mutate` function is used.  For example, if we wanted a column of the person's annual charges divided by their age


```r
health_insurance %>% 
  mutate(charges_over_age = charges/age) %>% 
  select(age, charges, charges_over_age) %>% 
  head(5)
```

```
## # A tibble: 5 x 3
##     age charges charges_over_age
##   <dbl>   <dbl>            <dbl>
## 1    19  16885.            889. 
## 2    18   1726.             95.9
## 3    28   4449.            159. 
## 4    33  21984.            666. 
## 5    32   3867.            121.
```

We can create as many new columns as we want.


```r
health_insurance %>% 
  mutate(age_squared  = age^2,
         age_cubed = age^3,
         age_fourth = age^4) %>% 
  head(5)
```

```
## # A tibble: 5 x 10
##     age sex     bmi children smoker region charges age_squared age_cubed
##   <dbl> <fct> <dbl>    <dbl> <fct>  <fct>    <dbl>       <dbl>     <dbl>
## 1    19 fema~  27.9        0 yes    south~  16885.         361      6859
## 2    18 male   33.8        1 no     south~   1726.         324      5832
## 3    28 male   33          3 no     south~   4449.         784     21952
## 4    33 male   22.7        0 no     north~  21984.        1089     35937
## 5    32 male   28.9        0 no     north~   3867.        1024     32768
## # ... with 1 more variable: age_fourth <dbl>
```

The `CASE WHEN` function is quite similar to SQL.  For example, we can create a column which is `0` when `age < 50`, `1` when `50 <= age <= 70`, and `2` when `age > 70`.


```r
health_insurance %>% 
  mutate(age_bucket = case_when(age < 50 ~ 0,
                                age <= 70 ~ 1,
                                age > 70 ~ 2)) %>% 
  select(age, age_bucket)
```

```
## # A tibble: 1,338 x 2
##      age age_bucket
##    <dbl>      <dbl>
##  1    19          0
##  2    18          0
##  3    28          0
##  4    33          0
##  5    32          0
##  6    31          0
##  7    46          0
##  8    37          0
##  9    37          0
## 10    60          1
## # ... with 1,328 more rows
```

SQL translation:


```sql
SELECT CASE WHEN AGE < 50 THEN 0
       ELSE WHEN AGE <= 70 THEN 1
       ELSE 2
FROM health_insurance
```

## Exercises

The data `actuary_salaries` contains the salaries of actuaries collected from the DW Simpson survey.  Use this data to answer the exercises below.


```r
actuary_salaries %>% glimpse()
```

```
## Observations: 138
## Variables: 6
## $ industry    <chr> "Casualty", "Casualty", "Casualty", "Casualty", "C...
## $ exams       <chr> "1 Exam", "2 Exams", "3 Exams", "4 Exams", "1 Exam...
## $ experience  <dbl> 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5,...
## $ salary      <chr> "48 - 65", "50 - 71", "54 - 77", "58 - 82", "54 - ...
## $ salary_low  <dbl> 48, 50, 54, 58, 54, 57, 62, 63, 65, 70, 72, 85, 55...
## $ salary_high <chr> "65", "71", "77", "82", "72", "81", "87", "91", "9...
```

1.  How many industries are represented?
2.  The `salary_high` column is a character type when it should be numeric.  Change this column to numeric.
3.  What are the highest and lowest salaries for an actuary in Health with 5 exams passed?
4.  Create a new column called `salary_mid` which has the middle of the `salary_low` and `salary_high` columns.
5.  When grouping by industry, what is the highest `salary_mid`?  What about `salary_high`?  What is the lowest `salary_low`?
6.  There is a mistake when `salary_low == 11`.  Find and fix this mistake, and then rerun the code from the previous task.
7.  Create a new column, called `n_exams`, which is an integer.  Use 7 for ASA/ACAS and 10 for FSA/FCAS.  Use the code below as a starting point and fill in the `_` spaces


```r
actuary_salaries <- actuary_salaries %>% 
  mutate(n_exams = case_when(exams == "FSA" ~ _,
                             exams == "ASA" ~ _,
                             exams == "FCAS" ~ _,
                             exams == "ACAS" ~ _,
                             TRUE ~ as.numeric(substr(exams,_,_)))) 
```

8. Create a column called `social_life`, which is equal to `n_exams`/`experience`.  What is the average (mean) `social_life` by industry?  Bonus question: what is wrong with using this as a statistical measure?


## Answers to exercises

1.  How many industries are represented?


```r
actuary_salaries %>% count(industry)
```

```
## # A tibble: 4 x 2
##   industry     n
##   <chr>    <int>
## 1 Casualty    45
## 2 Health      31
## 3 Life        31
## 4 Pension     31
```

2.  The `salary_high` column is a character type when it should be numeric.  Change this column to numeric.


```r
#method 1
actuary_salaries <- actuary_salaries %>% mutate(salary_high = as.numeric(salary_high))

#method 2
actuary_salaries <- actuary_salaries %>% modify_at("salary_high", as.numeric)
```

3.  What are the highest and lowest salaries for an actuary in Health with 5 exams passed?


```r
actuary_salaries %>% 
  filter(industry == "Health", exams == 5) %>% 
  summarise(highest = max(salary_high),
            lowest = min(salary_low))
```

```
## # A tibble: 1 x 2
##   highest lowest
##     <dbl>  <dbl>
## 1     126     68
```


4.  Create a new column called `salary_mid` which has the middle of the `salary_low` and `salary_high` columns.


```r
actuary_salaries <- actuary_salaries %>% 
  mutate(salary_mid = (salary_low + salary_high)/2)
```


5.  When grouping by industry, what is the highest `salary_mid`?  What about `salary_high`?  What is the lowest `salary_low`?


```r
actuary_salaries %>% 
  group_by(industry) %>% 
  summarise(max_salary_mid = max(salary_mid),
            max_salary_high = max(salary_high),
            low_salary_low = min(salary_low))
```

```
## # A tibble: 4 x 4
##   industry max_salary_mid max_salary_high low_salary_low
##   <chr>             <dbl>           <dbl>          <dbl>
## 1 Casualty           302.             447             11
## 2 Health             272.             390             49
## 3 Life               244              364             51
## 4 Pension            224.             329             44
```

6.  There is a mistake when `salary_low == 11`.  Find and fix this mistake, and then rerun the code from the previous task.


```r
actuary_salaries <- actuary_salaries %>% 
  mutate(salary_low = ifelse(salary_low == 11, yes = 114, no = salary_low),
         salary_high = ifelse(salary_high == 66, yes = 166, no = salary_high))

#the minimum salary low is now 48
actuary_salaries %>% 
  group_by(industry) %>% 
  summarise(max_salary_mid = max(salary_mid),
            max_salary_high = max(salary_high),
            low_salary_low = min(salary_low))
```

```
## # A tibble: 4 x 4
##   industry max_salary_mid max_salary_high low_salary_low
##   <chr>             <dbl>           <dbl>          <dbl>
## 1 Casualty           302.             447             48
## 2 Health             272.             390             49
## 3 Life               244              364             51
## 4 Pension            224.             329             44
```

7.  Create a new column, called `n_exams`, which is an integer.  Use 7 for ASA/ACAS and 10 for FSA/FCAS.

Use the code below as a starting point and fill in the `_` spaces


```r
actuary_salaries <- actuary_salaries %>% 
  mutate(n_exams = case_when(exams == "FSA" ~ _,
                             exams == "ASA" ~ _,
                             exams == "FCAS" ~ _,
                             exams == "ACAS" ~ _,
                             TRUE ~ as.numeric(substr(exams,_,_)))) 
```



```r
actuary_salaries <- actuary_salaries %>% 
  mutate(n_exams = case_when(exams == "FSA" ~ 10,
                             exams == "ASA" ~ 7,
                             exams == "FCAS" ~ 10,
                             exams == "ACAS" ~ 7,
                             TRUE ~ as.numeric(substr(exams,1,2)))) 
```

```
## Warning in eval_tidy(pair$rhs, env = default_env): NAs introduced by
## coercion
```

```r
actuary_salaries %>% count(n_exams)
```

```
## # A tibble: 8 x 2
##   n_exams     n
##     <dbl> <int>
## 1       1    12
## 2       2    17
## 3       3    19
## 4       4    21
## 5       5    17
## 6       6     5
## 7       7    29
## 8      10    18
```

8. Create a column called `social_life`, which is equal to `n_exams`/`experience`.  What is the average (mean) `social_life` by industry?  Bonus question: what is wrong with using this as a statistical measure?


```r
actuary_salaries %>% 
  mutate(social_life = n_exams/experience) %>% 
  group_by(industry) %>% 
  summarise(avg_social_life = mean(social_life))
```

```
## # A tibble: 4 x 2
##   industry avg_social_life
##   <chr>              <dbl>
## 1 Casualty           0.985
## 2 Health             1.06 
## 3 Life               1.06 
## 4 Pension            1.00
```

```r
#this is not REALLY an average as the number of people, or number of actuaries, are not taken into consideration.  To correctly take the average, we would need use a weighted average like sum(number_actuaries*social_life)/sum(number_actuaries)
```


