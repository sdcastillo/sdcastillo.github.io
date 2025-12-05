# A Mini-Exam Example

A common regret of students who failed exam PA is that they did not start doing practice exams soon enough.  Here is a simple practice exam to help you to understand what concepts that you should focus on learning, to become familiar with the format, and to test your technical skills with R, RStudio, and MS Word.

## Project Statement

ABC Health Insurance company is building a model to predict medical claims.  Using only `age` and `sex` information from the prior year, build a model to predict claims for the next year.  

### Describe the data (1 point)


```r
library(tidyverse)
data <- read_csv("C:/Users/sam.castillo/Desktop/R Manual Data/health_insurance.csv") %>% 
  select(age, sex, charges) %>%  #put this into an r library
  rename(claims = charges)

data %>% summary()
```

```
##       age            sex                claims     
##  Min.   :18.00   Length:1338        Min.   : 1122  
##  1st Qu.:27.00   Class :character   1st Qu.: 4740  
##  Median :39.00   Mode  :character   Median : 9382  
##  Mean   :39.21                      Mean   :13270  
##  3rd Qu.:51.00                      3rd Qu.:16640  
##  Max.   :64.00                      Max.   :63770
```

```r
data %>% dim()
```

```
## [1] 1338    3
```

> The data consists of 1,338 policies with age and sex information.  The objective is to predict future claims.

### Create a histogram of the claims and comment on the shape (1 point)

The distribution of claims is strictly positive and right skewed.


```r
data %>% ggplot(aes(claims)) + geom_histogram()
```

```
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
```

<img src="07-example_files/figure-html/unnamed-chunk-2-1.png" width="672" />

### Fit a linear model (1 point)


```r
model = lm(claims ~ age + sex, data = data)
```

### Describe the relationship between age, sex, and claim costs (1 point)

> We fit a linear model to the claim costs using age and sex as predictor variables.  The coefficient of `age` is 258, indicating that the claim costs increase by $258 for every one-unit increase in the policyholder's age.  The cofficient of 1538 on `sexmale` indicates that on average, men have $1538 higher claims than women do.


```r
coefficients(model)
```

```
## (Intercept)         age     sexmale 
##   2343.6249    258.8651   1538.8314
```

### Write a summary of steps 1-4 in non-technical language (1 point)

> ABC Health is interested in predicting the future claims for a group of policyholders.  We began by collecting data on 1,538 policy holders which recorded their age, sex, and annual claims.  We then created a histogram of the claim costs.  A linear model which shows that claim costs increase as age increases, and are higher for men on average.
