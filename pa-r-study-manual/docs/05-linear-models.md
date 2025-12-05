---
output:
  html_document: default
  pdf_document: default
---




# Introduction to modeling

About 40-50% of the exam grade is based on modeling.  The goal is to be able to predict an unknown quantity.  In actuarial applications, this tends to be claims that occur in the future, death, injury, accidents, policy lapse, hurricanes, or some other insurable event.

## Modeling vocabulary

Modeling notation is sloppy because there are many words that mean the same thing.

The number of observations will be denoted by $n$.  When we refer to the size of a data set, we are referring to $n$.  Each row of the data is called an *observation* or *record*.  Observations tend to be people, cars, buildings, or other insurable things.  These are always independent in that they do not influence one another.  Because the Prometric computers have limited power, $n$ tends to be less than 100,000.

Each observation has known attributes called *variables*, *features*, or *predictors*.  We use $p$ to refer the number of input variables that are used in the model.  

The *target*, *response*, *label*, *dependant variable*, or *outcome* variable is the unknown quantity that is being predicted.  We use $Y$ for this.  This can be either a whole number, in which case we are performing *regression*, or a category, in which case we are performing *classification*.  

For example, say that you are a health insurance company that wants to set the premiums for a group of people.  The premiums for people who are likely to incur high health costs need to be higher than those who are likely to be low-cost.  Older people tend to use more of their health benefits than younger people, but there are always exceptions for those who are very physically active and healthy.  Those who have an unhealthy Body Mass Index (BMI) tend to have higher costs than those who have a healthy BMI, but this has less of an impact on younger people.  **In short, we want to be able to predict a person's future health costs by taking into account many of their attributes at once**.

This can be done in the `health_insurance` data by fitting a model to predict the annual health costs of a person.  The target variable is `y = charges`, and the predictor variables are `age`, `sex`, `bmi`, `children`, `smoker` and `region`.  These six variables mean that $p = 6$.  The data is collected from 1,338 patients, which means that $n = 1,338$.   

## Modeling notation

Scalar numbers are denoted by ordinary variables (i.e., $x = 2$, $z = 4$), and vectors are denoted by bold-faced letters 

$$\mathbf{a} = \begin{pmatrix} a_1 \\ a_2 \\ a_3 \end{pmatrix}$$

We organize these variables into matrices.  Take an example with $p$ = 2 columns and 3 observations.  The matrix is said to be $3 \times 2$ (read as "3-by-2") matrix.

$$
\mathbf{X} = \begin{pmatrix}x_{11} & x_{21}\\
x_{21} & x_{22}\\
x_{31} & x_{32}
\end{pmatrix}
$$

In the health care costs example, $y_1$ would be the costs of the first patient, $y_2$ the costs of the second patient, and so forth.  The variables $x_{11}$ and $x_{12}$ might represent the first patient's age and sex respectively, where $x_{i1}$ is the patient's age, and $x_{i2} = 1$ if the ith patient is male and 0 if female.

Modeling is about using $X$ to predict $Y$. We call this "y-hat", or simply the *prediction*.  This is based on a function of the data $X$.

$$\hat{Y} = f(X)$$

This is almost never going to happen perfectly, and so there is always an error term, $\epsilon$.  This can be made smaller, but is never exactly zero.  

$$
\hat{Y} + \epsilon = f(X) + \epsilon
$$

In other words, $\epsilon = y - \hat{y}$.  We call this the *residual*.  When we predict a person's health care costs, this is the difference between the predicted costs (which we had created the year before) and the actual costs that the patient experienced (of that current year).

Another way of saying this is in terms of expected value: the model $f(X)$ estimates the expected value of the target $E[Y|X]$.  That is, once we condition on the data $X$, we can make a guess as to what we expect $Y$ to be "close to".  There are many ways of measuring "closeness", as we will see.  

## Ordinary Least Squares (OLS)

Also known as *simple linear regression*, OLS predicts the target as a weighted sum of the variables.

We find a $\mathbf{\beta}$ so that 

$$
\hat{Y} = E[Y] =  \beta_0 + \beta_1 X_1 + \beta_2 X_2 + ... + \beta_p X_p
$$

Each $y_i$ is a *linear combination* of $x_{i1}, ..., x_{ip}$, plus a constant $\beta_0$ which is called the *intercept* term.  

In the one-dimensional case, this creates a line connecting the points.  In higher dimensions, this creates a hyperplane.

<img src="05-linear-models_files/figure-html/unnamed-chunk-2-1.png" width="672" />

The red line shows the *expected value* of the target, as the target $\hat{Y}$ is actually a random variable.  For each of the data points, the model assumes a Gaussian distribution. If there is just a single predictor, $x$, then the mean is $\beta_0 + \beta_1 x$.

<img src="C:/Users/sam.castillo/Desktop/PA-MAS-R-Study-Manual/images/conditional_response.jpg" width="200%" style="display: block; margin: auto;" />

The question then is **how can we choose the best values of** $\beta?$  First of all, we need to define what we mean by "best".  Ideally, we will choose these values which will create close predictions of $Y$ on new, unseen data.  

To solve for $\mathbf{\beta}$, we first need to define a *loss function*.  This allows us to compare how well a model is fitting the data.  The most commonly used loss function is the residual sum of squares (RSS), also called the *squared error loss* or the L2 norm.  When RSS is small, then the predictions are close to the actual values and the model is a good fit.  When RSS is large, the model is a poor fit.

$$
\text{RSS} = \sum_i(y_i - \hat{y})^2
$$

When you replace $\hat{y_i}$ in the above equation with $\beta_0 + \beta_1 x_1 + ... + \beta_p x_p$, take the derivative with respect to $\beta$, set equal to zero, and solve, we can find the optimal values.  This turns the problem of statistics into a problem of numeric optimization, which computers can do quickly.  

You might be asking: why does this need to be the squared error?  Why not the absolute error, or the cubed error?  Technically, these could be used as well but the betas would not be the maximum likelihood parameters.  In fact, using the absolute error results in the model predicting the *median* as opposed to the *mean*.  Two reasons why RSS is popular are:  

- It provides the same solution if we assume that the distribution of $Y|X$ is Guassian and maximize the likelihood function.  This method is used for GLMs, in the next chapter.
- It is computationally easier, and computers used to have a difficult time optimizing for MAE

>What does it mean when a log transform is applied to $Y$?  I remember from my statistics course on regression that this was done.  

This is done so that the variance is closer to being constant.  For example, if the units are in dollars, then it is very common for the values to fluctuate more for higher values than for lower values.  Consider a stock price, for instance.  If the stock is \$50 per share, then it will go up or down less than if it is \$1000 per share.  The log of 50, however, is about 3.9 and the log of 1000 is only 6.9, and so this difference is smaller.  In other words, the variance is smaller.

Transforming the target means that instead of the model predicting $E[Y]$, it predicts $E[log(Y)]$.  A common mistake is to then the take the exponent in an attempt to "undo" this transform, but $e^{E[log(Y)]}$ is not the same as $E[Y]$.

## Regression vs. classification

Regression modeling is when the target is a number.  Binary classification is when there are two outcomes, such as "Yes/No", "True/False", or "0/1".  Multi-class regression is when there are more than two categories such as "Red, Yellow, Green" or "A, B, C, D, E".  There are many other types of regression that are not covered on this exam such as ordinal regression, where the outcome is an ordered category, or time-series regression, where the data is time-dependent.

## Regression metrics

For any model, the goal is always to reduce an error metric.  This is a way of measuring how well the model can explain the target.  The phrases "reducing error", "improving performance", or "making a better fit" are synonymous with reducing the error.  The word "better" means "lower error" and "worse" means "higher error".

The choice of error metric has a big difference on the outcome.  When explaining a model to a businessperson, using simpler metrics such as R-Squared and Accuracy is convenient.  When training the model, however, using a more nuanced metric is almost always better.

These are the regression metrics that are most likely to appear on Exam PA.  Memorizing these formulas for AIC and BIC is not necessary as they are in the R documentation by typing `?AIC` or `?BIC` into the R console.

<img src="C:/Users/sam.castillo/Desktop/PA-MAS-R-Study-Manual/images/regression_metrics.png" width="1300%" style="display: block; margin: auto;" />

## Example

In our health insurance data, we can predict a person's health costs based on their age, body mass index, and gender.  Intuitively, we expect that these costs would increase as a person's age increases, would be different for men than for women, and would be higher for those who have a less healthy BMI.  We create a linear model using `bmi`, `age`, and `sex` as an inputs.

The `formula` controls which variables are included.  There are a few shortcuts for using R formulas.  

| Formula | Meaning  | 
|-------|---------|
| `charges` ~ `bmi` + `age` | Use `age` and `bmi` to predict `charges` |
| `charges` ~ `bmi` + `age` + `bmi`*`age` | Use `age`,`bmi` as well as an interaction to predict `charges` |
| `charges` ~ (`bmi > 20`) + `age` | Use an indicator variable for `bmi > 20` `age` to predict `charges` |
| log(`charges`) ~ log(`bmi`) + log(`age`) | Use the logs of `age` and `bmi` to predict  log(`charges`) |
| `charges` ~ . | Use all variables to predict `charges`|


>While you can use formulas to create new variables, the exam questions tend to have you do this in the data itself.  For example, if taking the log transform of a `bmi`, you would add a column `log_bmi` to the data and remove the original `bmi` column.

Below we fit a simple linear model to predict charges.


```r
library(ExamPAData)
library(tidyverse)

model <- lm(data = health_insurance, formula = charges ~ bmi + age + sex)
```

The `summary` function gives details about the model.  First, the `Estimate`, gives you the coefficients.  The `Std. Error` is the error of the estimate for the coefficient.  Higher standard error means greater uncertainty.  This is relative to the average value of that variable.  The `p value` tells you how "big" this error really is based on standard deviations.  A small p-value (`Pr (>|t|))`) means that we can safely reject the null hypothesis that says the cofficient is equal to zero.

The little `*`, `**`, `***` tell you the significance level.  A variable with a `***` means that the probability of getting a coefficient of that size given that the data was randomly generated is less than 0.001.  The `**` has a significance level of 0.01, and `*` of 0.05.


```r
summary(model)
```

```
## 
## Call:
## lm(formula = charges ~ bmi + age + sex, data = health_insurance)
## 
## Residuals:
##    Min     1Q Median     3Q    Max 
## -14974  -7073  -5072   6953  47348 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept) -6986.82    1761.04  -3.967 7.65e-05 ***
## bmi           327.54      51.37   6.377 2.49e-10 ***
## age           243.19      22.28  10.917  < 2e-16 ***
## sexmale      1344.46     622.66   2.159    0.031 *  
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 11370 on 1334 degrees of freedom
## Multiple R-squared:  0.1203,	Adjusted R-squared:  0.1183 
## F-statistic: 60.78 on 3 and 1334 DF,  p-value: < 2.2e-16
```

>For this exam, variable selection tends to be based on the 0.05 significance level (single star `*`).

When evaluating model performance, you should not rely on the `summary` alone as this is based on the training data.  To look at performance, test the model on validation data.  This can be done by either using a hold out set, or using cross-validation, which is even better.

Let's create an 80% training set and 20% testing set.  You don't need to worry about understanding this code as the exam will always give this to you.


```r
set.seed(1)
library(caret)
#create a train/test split
index <- createDataPartition(y = health_insurance$charges, 
                             p = 0.8, list = F) %>% as.numeric()
train <-  health_insurance %>% slice(index)
test <- health_insurance %>% slice(-index)
```

Train the model on the `train` and test on `test`.  


```r
model <- lm(data = train, formula = charges ~ bmi + age)
pred = predict(model, test)
```

Let's look at the Root Mean Squared Error (RMSE).  


```r
get_rmse <- function(y, y_hat){
  sqrt(mean((y - y_hat)^2))
}

get_rmse(pred, test$charges)
```

```
## [1] 11421.96
```

And the Mean Absolute Error as well.


```r
get_mae <- function(y, y_hat){
  sqrt(mean(abs(y - y_hat)))
}

get_mae(pred, test$charges)
```

```
## [1] 94.32336
```

The above metrics do not tell us if this is a good model or not by themselves.  We need a comparison.  The fastest check is to compare against a prediction of the mean.  In other words, all values of the `y_hat` are the average of `charges`, which is about \$13,000.


```r
get_rmse(mean(test$charges), test$charges)
```

```
## [1] 12574.97
```

```r
get_mae(mean(test$charges), test$charges)
```

```
## [1] 96.63604
```

The RMSE and MAE are both **higher** (worse) when using just the mean, which is what we expect.  **If you ever fit a model and get an error which is worse than the average prediction, something must be wrong.**

The next test is to see if any assumptions have been violated.  

First, is there a pattern in the residuals?  If there is, this means that the model is missing key information.  For the model below, this is a **yes**, **which means that this is a bad model**.  Because this is just for illustration, we are going to continue using it.  


```r
plot(model, which = 1)
```

<div class="figure">
<img src="05-linear-models_files/figure-html/unnamed-chunk-12-1.png" alt="Residuals vs. Fitted" width="672" />
<p class="caption">(\#fig:unnamed-chunk-12)Residuals vs. Fitted</p>
</div>

The normal QQ shows how well the quantiles of the predictions fit to a theoretical normal distribution.  If this is true, then the graph is a straight 45-degree line.  In this model, you can definitely see that this is not the case.  If this were a good model, this distribution would be closer to normal.


```r
plot(model, which = 2)
```

<div class="figure">
<img src="05-linear-models_files/figure-html/unnamed-chunk-13-1.png" alt="Normal Q-Q" width="672" />
<p class="caption">(\#fig:unnamed-chunk-13)Normal Q-Q</p>
</div>

Once you have chosen your model, you should re-train over the entire data set.  This is to make the coefficients more stable because `n` is larger.  Below you can see that the standard error is lower after training over the entire data set.


```r
all_data <- lm(data = health_insurance, 
               formula = charges ~ bmi + age)
testing <- lm(data = test, 
              formula = charges ~ bmi + age)
```


|term        | full_data_std_error| test_data_std_error|
|:-----------|-------------------:|-------------------:|
|(Intercept) |              1744.1|              3824.2|
|bmi         |                51.4|               111.1|
|age         |                22.3|                47.8|

All interpretations should be based on the model which was trained on the entire data set.  Obviously, this only makes a difference if you are interpreting the precise values of the coefficients.  If you are just looking at which variables are included, or at the size and sign of the coefficients, then this would probably not make a difference.


```r
coefficients(model)
```

```
## (Intercept)         bmi         age 
##  -4526.5284    286.8283    228.4372
```

Translating the above into an equation we have

$$\hat{y_i} = -4,526 + 287 \space\text{bmi} + 228\space \text{age}$$

For example, if a patient has `bmi = 27.9` and `age = 19` then predicted value is 

$$\hat{y_1} = 4,526 + (287)(27.9) + (228)(19) = 16,865$$

This model structure implies that each of the variables $x_1, ..., x_p$ each change the predicted $\hat{y}$.  If $x_{ij}$ increases by one unit, then $y_i$ increases by $\beta_j$ units, regardless of what happens to all of the other variables.  This is one of the main assumptions of linear models: *variable indepdendence*.  If the variables are correlated, say, then this assumption will be violated.  

| Readings |  | 
|-------|---------|
| ISLR 2.1 What is statistical learning?|  |
| ISLR 2.2 Assessing model accuracy|  |


# Generalized linear Models (GLMs)

GLMs are a broad category of models.  Ordinary Least Squares and Logistic Regression are both examples of GLMs.

### Assumptions of OLS

We assume that the target is Gaussian with mean equal to the linear predictor.  This can be broken down into two parts:

1. A *random component*: The target variable $Y|X$ is normally distributed with mean $\mu = \mu(X) = E(Y|X)$

2. A link between the target and the covariates (also known as the systemic component) $\mu(X) = X\beta$

This says that each observation follows a normal distribution which has a mean that is equal to the linear predictor.  Another way of saying this is that "after we adjust for the data, the error is normally distributed and the variance is constant."  If $I$ is an n-by-in identity matrix, and $\sigma^2 I$ is the covariance matrix, then

$$
\mathbf{Y|X} \sim N( \mathbf{X \beta}, \mathbf{\sigma^2} I)
$$

### Assumptions of GLMs

Just as the name implies, GLMs are more *general* in that they are more flexible.  We relax these two assumptions by saying that the model is defined by 

1. A random component: $Y|X \sim \text{some exponential family distribution}$

2. A link: between the random component and covariates: 

$$g(\mu(X)) = X\beta$$
where $g$ is called the *link function* and $\mu = E[Y|X]$.

Each observation follows *some type of exonential distrubution* (Gamma, Inverse Gaussian, Poisson, Binomial, etc.) and that distribution has a mean which is related to the linear predictor through the link function.  Additionally, there is a *dispersion* parameter, but that is more more info that is needed here.  For an explanation, see [Ch. 2.2 of CAS Monograph 5](https://contentpreview.s3.us-east-2.amazonaws.com/CAS+Monograph+5+-+Generalized+Linear+Models+for+Insurance+Ratemaking.pdf).

## Advantages and disadvantages

There is usually at least one question on the PA exam which asks you to "list some of the advantages and disadvantages of using this particular model", and so here is one such list.  It is unlikely that the grader will take off points for including too many comments and so a good strategy is to include everything that comes to mind.

**GLM Advantages**

- Easy to interpret
- Can easily be deployed in spreadsheet format
- Handles different response/target distributions
- Is commonly used in insurance ratemaking

**GLM Disadvantages**

- Does not select features (without stepwise selection)
- Strict assumptions around distribution shape and randomness of error terms
- Predictor variables need to be uncorrelated
- Unable to detect non-linearity directly (although this can manually be addressed through feature engineering)
- Sensitive to outliers
- Low predictive power

## GLMs for regression

For regression problems, we try to match the actual distribution to the model's distribution being used in the GLM.  These are the most likely distributions.

<img src="05-linear-models_files/figure-html/unnamed-chunk-17-1.png" width="672" style="display: block; margin: auto;" />

The choice of target distribution should be similar to the actual distribution of $Y$.  For instance, if $Y$ is never less than zero, then using the Gaussian distribution is not ideal because this can allow for negative values.  If the distribution is right-skewed, then the Gamma or Inverse Gaussian may be appropriate because they are also right-skewd. 

<img src="C:/Users/sam.castillo/Desktop/PA-MAS-R-Study-Manual/images/response_distributions.png" width="800%" style="display: block; margin: auto;" />

There are five link functions for a continuous $Y$, although the choice of distribution family will typically rule-out several of these immediately.  The linear predictor (a.k.a., the *systemic component*) is $z$ and the link function is how this connects to the expected value of the resonse.

$$z = X\beta = g(\mu)$$
<img src="C:/Users/sam.castillo/Desktop/PA-MAS-R-Study-Manual/images/link_functions.png" width="200%" style="display: block; margin: auto;" />

If the target distribution *must* have a positive mean, such as in the case of the Inverse Gaussian or Gamma, then the Identity or Inverse links are poor choices because they allow for negative values; the range of the mean is $(-\infty, \infty)$.  The other link functions force the mean to be positive. 

## Interpretation of coefficients

The GLM's interpretation depends on the choice of link function.  

### Identity link

This is the easiest to interpret.  For each one-unit increase in $X_j$, the expected value of the target, $E[Y]$, increases by $\beta_j$, assuming that all other variables are held constant.

### Log link

This is the most popular choice when the results need to be easy to understand.  Simply take the exponent of the coefficients and model turns into a product of numbers being multiplied together.

$$
log(\hat{Y}) = X\beta \Rightarrow \hat{Y} = e^{X \beta}
$$

For a single observation $Y_i$, this is

$$
\text{exp}(\beta_0 + \beta_1 X_{i1} + \beta_2 X_{i2} + ... + \beta_p X_{ip}) = \\
e^{\beta_0} e^{\beta_1 X_{i1}}e^{\beta_2 X_{i2}} ...  e^{\beta_p X_{ip}} = 
R_{i0} R_{i2} R_{i3} ... R_{ip}
$$

$R_{ik}$ is known as the *relativity* of the kth variable.  This terminology is from insurance ratemaking where actuaries need to be able to explain the impact of each variable to insurance regulators.

Another advantage to the log link is that the coefficients can be interpreted as having a percentage change on the target.  Here is an example for a GLM with variables $X_1$ and $X_2$ and a log link function. This holds any continuous target distribution.

| Variable    | $\beta_j$ | $e^{\beta_j} - 1$ | Interpretation                                    | 
|-------------|-------------|----------------------|---------------------------------------------------| 
| (intercept) | 0.100       | 0.105                |                                                   | 
| $X_1$          | 0.400       | 0.492                | 49% increase in $E[Y]$ for each unit increase in $X_1$* | 
| $X_2$          | -0.500      | -0.393               | 39% decrease in $E[Y]$ for each unit increase in $X_2$* | 


If categorical predictors are used, then the interpretation is very similar.  Say that there is one predictor, `COLOR`, which takes on values of `YELLO` (reference level), `RED`, and `BLUE`.  


| Variable    | $\beta_j$ | $e^{\beta_j} - 1$  | Interpretation                                          | 
|-------------|-------------|----------------------|---------------------------------------------------------| 
| (intercept) | 0.100       | 0.105                |                                                         | 
| Color=RED   | 0.400       | 0.492                | 49% increase  in $E[Y]$ for RED cars as opposed to YELLOW cars*| 
| Color=BLUE  | -0.500      | -0.393               | 39% decrease in $E[Y]$ for BLUE cars rather than YELLOW cars*| 

\* Assuming all other variables are held constant.

## Other links

The other link functions are not straight-forward to interpret and so it is unlikely that you would be asked to do so.

# GLMs for classification

For classification, the predicted values need to be a category instead of a number.  Using a discrete target distribution ensures that this will be the case.  The probability of an event occuring is $E[Y] = p$.  Unlike the continuous case, all of the link functions have the same range between 0 and 1 because this is a probability.  

## Binary target

When $Y$ is binary, then the Binomial distribution is the only choice.  If there are multiple categories, then the Multinomial should be used.

## Count target 

When $Y$ is a count, the Poisson distribution is the only choice.  Two examples are counting the number of claims which a policy has in a given year or counting the number of people visiting the ER in a given month.  The key ingredients are 1) some event, and 2) some fixed period of time.

Statistically, the name for this is a Poisson Process, which is a way of describine a serious of discrete events where the average time between events is known, called the "rate" $\lambda$, but the exact timing of events is unknown. For a time interval of length $m$, the expected number of events is $\lambda m$.  

By using a GLM, we can fit a different rate for each observation. In the ER example, each patient would have a different rate.  Those who are unhealthy or who work in risky environments would have a higher rate of ER visits than those are healthy and work in offices.

$$Y_i|X_i \sim \text{Poisson}(\lambda_i m_i)$$


When all observations have the same exposure, $m = 1$.  When the mean of the data is far from the variance, an additional parameter known as the *dispersion parameter* is used.  A classic example is when modeling insurance claim counts which have a lot of zero claims.  Then the model is said to be an "over-dispersed Poisson" or "zero-inflated" model.  

## Link functions

There are four link functions.  The most common are the Logit and Probit, but the Cauchit and Cloglog did appear on the SOA's Hospital Readmissions practice exam in 2019.  The identity link does not make sense for classification because it would result in predictions being outside of $(0,1)$

<img src="C:/Users/sam.castillo/Desktop/PA-MAS-R-Study-Manual/images/discrete_link_functions.png" width="1200%" style="display: block; margin: auto;" />

> The *logit* is also known as the *standard logistic function* or *sigmoid* and is also used in deep learning.

Below we see how the linear predictor (x-axis) gets converted to a probability (y-axis).  

<img src="05-linear-models_files/figure-html/unnamed-chunk-21-1.png" width="672" style="display: block; margin: auto;" />

- <span style="color:green ">Logit: </span> Most commonly used; default in R; canonical link for the binomial distribution.
- <span style="color:purple ">Probit: </span> Sharper curves than the other links which may have best performance for certain data; Inverse CDF of a standard normal distribution makes it easy to explain.
- <span style="color:red ">Cauchit: </span> Very gradual curves may be best for certain data;  CDF for the standard Cauchy distribution which is a t distribution with one degree of freedom.
- <span style="color:#85C1E9">Complimentary Log-Log (cloglog)</span> Asymmetric; Important in survival analysis (not on this exam).


## Interpretation of coefficients

Interpreting the coefficients in classification is trickier than in classification because the result must always be within $(0,1)$.  

### Logit

The link function $log(\frac{p}{1-p})$ is known as the log-odds, where the odds are $\frac{p}{1-p}$.  These come up in gambling, where bets are placed on the odds of some event occuring.  For example: if the probability of a claim is $p = 0.8$, then the probability of no claim is 0.2 and the odds of a claim occuring are 0.8/0.2 = 4.  

The transformation from probability to odds is monotonic.  This is a fancy way of saying that if $p$ increases, then the odds of $p$ increases as well, and vice versa if $p$ decreases.  The log transform is monotonic as well.  

The net result is that when a variable increases the linear predictor, this increases the log odds, and this increases the log of the odds, and vice versa if the linear predictor decreases.  In other words, the signs of the coefficients indicate whether the variable increases or decreases the probability of the event.

### Probit, Cauchit, Cloglog

These link functions are still monotonic and so the signs of the coefficients can be interpreted to mean that the variable has a positive or negative impact on the target.  

More extensive interpretation is not straight-forward.  In the case of the Probit, instead of dealing with the log-odds function, we have the inverse CDF of a standard Normal distribution (a.k.a., a Gaussian distribution with mean 0 and variance 1).  There is no way of taking this inverse directly.

## Example

Using the `auto_claim` data, we predict whether or not a policy has a claim.  This is also known as the *claim frequency*.


```r
auto_claim %>% count(CLM_FLAG)
```

```
## # A tibble: 2 x 2
##   CLM_FLAG     n
##   <chr>    <int>
## 1 No        7556
## 2 Yes       2740
```

About 40% do not have a claim while 60% have at least one claim.


```r
set.seed(42)
index <- createDataPartition(y = auto_claim$CLM_FLAG, 
                             p = 0.8, list = F) %>% as.numeric()
auto_claim <- auto_claim %>% 
  mutate(target = as.factor(ifelse(CLM_FLAG == "Yes", 1,0)))
train <-  auto_claim %>% slice(index)
test <- auto_claim %>% slice(-index)

frequency <- glm(target ~ AGE + GENDER + MARRIED + CAR_USE + 
                   BLUEBOOK + CAR_TYPE + AREA, 
                 data=train, 
                 family = binomial(link="logit"))
```

All of the variables except for the `CAR_TYPE` and `GENDERM` are highly significant.  The car types `SPORTS CAR` and `SUV` appear to be significant, and so if we wanted to make the model simpler we could create indicator variables for `CAR_TYPE == SPORTS CAR` and `CAR_TYPE == SUV`.


```r
frequency %>% summary()
```

```
## 
## Call:
## glm(formula = target ~ AGE + GENDER + MARRIED + CAR_USE + BLUEBOOK + 
##     CAR_TYPE + AREA, family = binomial(link = "logit"), data = train)
## 
## Deviance Residuals: 
##     Min       1Q   Median       3Q      Max  
## -1.8431  -0.8077  -0.5331   0.9575   3.0441  
## 
## Coefficients:
##                      Estimate Std. Error z value Pr(>|z|)    
## (Intercept)        -3.523e-01  2.517e-01  -1.400  0.16160    
## AGE                -2.289e-02  3.223e-03  -7.102 1.23e-12 ***
## GENDERM            -1.124e-02  9.304e-02  -0.121  0.90383    
## MARRIEDYes         -6.028e-01  5.445e-02 -11.071  < 2e-16 ***
## CAR_USEPrivate     -1.008e+00  6.569e-02 -15.350  < 2e-16 ***
## BLUEBOOK           -4.025e-05  4.699e-06  -8.564  < 2e-16 ***
## CAR_TYPEPickup     -6.687e-02  1.390e-01  -0.481  0.63048    
## CAR_TYPESedan      -3.689e-01  1.383e-01  -2.667  0.00765 ** 
## CAR_TYPESports Car  6.159e-01  1.891e-01   3.256  0.00113 ** 
## CAR_TYPESUV         2.982e-01  1.772e-01   1.683  0.09240 .  
## CAR_TYPEVan        -8.983e-03  1.319e-01  -0.068  0.94569    
## AREAUrban           2.128e+00  1.064e-01  19.993  < 2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for binomial family taken to be 1)
## 
##     Null deviance: 9544.3  on 8236  degrees of freedom
## Residual deviance: 8309.6  on 8225  degrees of freedom
## AIC: 8333.6
## 
## Number of Fisher Scoring iterations: 5
```

The signs of the coefficients tell if the probability of having a claim is either increasing or decreasing by each variable.  For example, the likelihood of an accident 

* Decreases as the age of the car increases
* Is lower for men 
* Is higher for sports cars and SUVs

The p-values tell us if the variable is significant.

- `Age`, `MarriedYes`, `CAR_USEPrivate`, `BLUEBOOK`, and `AreaUrban` are significant.
- Certain values of `CAR_TYPE` are significant but others are not.

The output is a predicted probability.  We can see that this is centered around a probability of about 0.3.  


```r
preds <- predict(frequency, newdat=test,type="response")
qplot(preds) 
```

<div class="figure">
<img src="05-linear-models_files/figure-html/unnamed-chunk-25-1.png" alt="Distribution of Predicted Probability" width="480" />
<p class="caption">(\#fig:unnamed-chunk-25)Distribution of Predicted Probability</p>
</div>

In order to convert these values to predicted 0's and 1's, we assign a *cutoff* value so that if $\hat{y}$ is above this threshold we use a 1 and 0 othersise.  The default cutoff is 0.5.  We change this to 0.3 and see that there are 763 policies predicted to have claims.


```r
test <- test %>% mutate(pred_zero_one = as.factor(1*(preds>.3)))
summary(test$pred_zero_one)
```

```
##    0    1 
## 1296  763
```

How do we decide on this cutoff value?  We need to compare cutoff values based on some evaluation metric.  For example, we can use *accuracy*.

$$\text{Accuracy} = \frac{\text{Correct Guesses}}{\text{Total Guesses}}$$

This results in an accuracy of 70%.  But is this good?


```r
test %>% summarise(accuracy = mean(pred_zero_one == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.699
```

Consider what would happen if we just predicted all 0's.  The accuracy is 74%.


```r
test %>% summarise(accuracy = mean(0 == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.734
```

For policies which experience claims the accuracy is 63%.


```r
test %>% 
  filter(target == 1) %>% 
  summarise(accuracy = mean(pred_zero_one == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.631
```

But for policies that don't actually experience claims this is 72%.  


```r
test %>% 
  filter(target == 0) %>% 
  summarise(accuracy = mean(pred_zero_one == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.724
```

How do we know if this is a good model?  We can repeat this process with a different cutoff value and get different accuracy metrics for these groups.  Let's use a cutoff of 0.6.

75%


```r
test <- test %>% mutate(pred_zero_one = as.factor(1*(preds>.6)))
test %>% summarise(accuracy = mean(pred_zero_one == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.752
```

10% for policies with claims and 98% for policies without claims.  


```r
test %>% 
  filter(target == 1) %>% 
  summarise(accuracy = mean(pred_zero_one == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.108
```

```r
test %>% 
  filter(target == 0) %>% 
  summarise(accuracy = mean(pred_zero_one == target))
```

```
## # A tibble: 1 x 1
##   accuracy
##      <dbl>
## 1    0.985
```

The punchline is that the accuracy depends on the cutoff value, and changing the cutoff value changes whether the model is accuracy for the "true = 1" classes (policies with actual claims) vs. the "false = 0" classes (policies without claims).

# Classification metrics

For regression problems, when the output is a whole number, we can use the sum of squares $\text{RSS}$, the r-squared $R^2$, the mean absolute error $\text{MAE}$, and the likelihood.  For classification problems we need to a new set of metrics.

A *confusion matrix* shows is a table that summarises how the model classifies each group.

- No claims and predicted to not have claims - **True Negatives (TN) = 1,489**
- Had claims and predicted to have claims - **True Positives (TP) = 59**
- No claims but predited to have claims - **False Positives (FP) = 22**
- Had claims but predicted not to - **False Negatives (FN) = 489**


```r
confusionMatrix(test$pred_zero_one,factor(test$target))$table
```

```
##           Reference
## Prediction    0    1
##          0 1489  489
##          1   22   59
```

These definitions allow us to measure performance on the different groups.

*Precision* answers the question "out of all of the positive predictions, what percentage were correct?"

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

*Recall* answers the question "out of all of positive examples in the data set, what percentage were correct?"

$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

The choice of using precision vs. recall depends on the relative cost of making a FP or a FN error.  If FP errors are expensive, then use precision; if FN errors are expensive, then use recall.  

**Example A:** the model trying to detect a deadly disease, which only 1 out of every 1,000 patient's survive without early detection.  Then the goal should be to optimize *recall*, because we would want every patient that has the disease to get detected.  

**Example B:** the model is detecting which emails are spam or not.  If an important email is flagged as spam incorrectly, the cost is 5 hours of lost productivity.  In this case, *precision* is the main concern.

In some cases we can compare this "cost" in actual values.  For example, if a federal court is predicting if a criminal will recommit or not, they can agree that "1 out of every 20 guilty individuals going free" in exchange for "90% of those who are guilty being convicted".  When money is involed, a dollar amount can be used: flagging non-spam as spam may cost \$100 whereas missing a spam email may cost \$2.  Then the cost-weighted accuracy is

$$\text{Cost} = (100)(\text{FN}) + (2)(\text{FP})$$

The cutoff value can be tuned in order to find the minimum cost.

Fortunately, all of this is handled in a single function called `confusionMatrix`.


```r
confusionMatrix(test$pred_zero_one,factor(test$target))
```

```
## Confusion Matrix and Statistics
## 
##           Reference
## Prediction    0    1
##          0 1489  489
##          1   22   59
##                                           
##                Accuracy : 0.7518          
##                  95% CI : (0.7326, 0.7704)
##     No Information Rate : 0.7339          
##     P-Value [Acc > NIR] : 0.03366         
##                                           
##                   Kappa : 0.1278          
##                                           
##  Mcnemar's Test P-Value : < 2e-16         
##                                           
##             Sensitivity : 0.9854          
##             Specificity : 0.1077          
##          Pos Pred Value : 0.7528          
##          Neg Pred Value : 0.7284          
##              Prevalence : 0.7339          
##          Detection Rate : 0.7232          
##    Detection Prevalence : 0.9607          
##       Balanced Accuracy : 0.5466          
##                                           
##        'Positive' Class : 0               
## 
```

## Area Under the ROC Curv (AUC)

What if we look at both the true-positive rate (TPR) and false positive rate (FPR) simultaneously?  That is, for each value of the cutoff, we can calculate the TPR and TNR.  

For example, say that we have 10 cutoff values, $\{k_1, k_2, ..., k_{10}\}$.  Then for each value of $k$ we calculate both the true positive rates

$$\text{TPR} = \{\text{TPR}(k_1), \text{TPR}(k_2), .., \text{TPR}(k_{10})\} $$ 

and the true negative rates

$$\{\text{FNR} = \{\text{FNR}(k_1), \text{FNR}(k_2), .., \text{FNR}(k_{10})\}$$

Then we set `x = TPR` and `y = FNR` and graph x against y.  The plot below shows the ROC for the `auto_claims` data.  The Area Under the Curv of 0.6795 is what we would get if we integrated under the curve.


```r
library(pROC)
roc(test$target, preds, plot = T)
```

<div class="figure">
<img src="05-linear-models_files/figure-html/unnamed-chunk-35-1.png" alt="AUC for auto_claim" width="672" />
<p class="caption">(\#fig:unnamed-chunk-35)AUC for auto_claim</p>
</div>

```
## 
## Call:
## roc.default(response = test$target, predictor = preds, plot = T)
## 
## Data: preds in 1511 controls (test$target 0) < 548 cases (test$target 1).
## Area under the curve: 0.7558
```

If we just randomly guess, the AUC would be 0.5, which is represented by the 45-degree line.  A perfect model would maximize the curve to the upper-left corner.

AUC is preferred over Accuracy when there are a lot more "true" classes than "false" classes, which is known as having *class imbalance*.  An example is bank fraud detection: 99.99% of bank transactions are "false" or "0" classes, and so optimizing for accuracy alone will result in a low sensitivity for detecting actual fraud.

## Additional reading

| Title | Source           |
|---------|-----------------|
| An Overview of Classification   | ISL 4.1 |
| [Understanding AUC - ROC Curv](https://towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5#:~:targetText=What%20is%20AUC%20%2D%20ROC%20Curve%3F,capable%20of%20distinguishing%20between%20classes.)| Sarang Narkhede, Towards Data Science   |
| [Precision vs. Recall](https://towardsdatascience.com/precision-vs-recall-386cf9f89488#:~:targetText=Precision%20and%20recall%20are%20two,correctly%20classified%20by%20your%20algorithm.)     | Shruti Saxena, Towards Data Science    |


# Additional GLM topics

So far we have focused on how the target is related to the target.  

## Residuals

Learning from mistakes is the path to improvement.  For GLMs, residual analysis looks for patterns in the errors in order to find ways of improving the model.

### Raw residuals

The word "residual" by itself actually means the "raw residual" in GLM language.  This is the difference in actual vs. predicted values.

$$\text{Raw Residual} = y_i - \hat{y_i}$$

### Deviance residuals

This is not meaningful for GLMs with non-Gaussian distributions.  To adjust for other distributions, we need the concept of *deviance residuals*.

To paraphrase from this paper from the University of Oxford:

stats.ox.ac.uk/pub/bdr/IAUL/ModellingLecture5.pdf

Deviance is a way of assessing the adequacy of a model by comparing it with a more general
model with the maximum number of parameters that can be estimated. It is referred to
as the saturated model. In the saturated model there is basically one parameter per
observation. The deviance assesses the goodness of fit for the model by looking at the
difference between the log-likelihood functions of the saturated model and the model
under investigation, i.e. $l(b_{sat},y) - l(b,y)$. Here sat $b_{sat}$ denotes the maximum likelihood
estimator of the parameter vector of the saturated model, $\beta_{sat}$ , and $b$ is the maximum
likelihood estimator of the parameters of the model under investigation, $\beta$. The maximum likelihood estimator is the estimator that maximises the likelihood function.  **The deviance is defined as**

$$D = 2[l(b_{sat},y) - l(b,y)]$$
The deviance residual uses the deviance of the ith observation $d_i$ and then takes the square root and applies the same sign (aka, the + or - part) of the raw residual.

$$\text{Deviance Residual} = \text{sign}(y_i - \hat{y_i})\sqrt{d_i}$$

## Example

Just as with OLS, there is a `formula` and `data argument`.  In addition, we need to specify the target distribution and link function.


```r
model = glm(formula = charges ~ age + sex + smoker, 
            family = Gamma(link = "log"),
            data = health_insurance)
```

We see that `age`, `sex`, and `smoker` are all significant (p <0.01).  Reading off the coefficient signs, we see that claims

- Increase as age increases
- Are higher for women
- Are higher for smokers


```r
model %>% tidy()
```

```
## # A tibble: 4 x 5
##   term        estimate std.error statistic   p.value
##   <chr>          <dbl>     <dbl>     <dbl>     <dbl>
## 1 (Intercept)   7.82     0.0600     130.   0.       
## 2 age           0.0290   0.00134     21.6  3.40e- 89
## 3 sexmale      -0.0468   0.0377      -1.24 2.15e-  1
## 4 smokeryes     1.50     0.0467      32.1  3.25e-168
```

Below you can see graph of deviance residuals vs. the predicted values. 

**If this were a perfect model, all of these below assumptions would be met:**

- Scattered around zero? 
- Constant variance? 
- No obvious pattern? 


```r
plot(model, which = 3)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-38-1.png" width="672" />

The quantile-quantile (QQ) plot shows the quantiles of the deviance residuals (i.e., after adjusting for the Gamma distribution) against theoretical Gaussian quantiles.  

**In a perfect model, all of these assumptions would be met:**

- Points lie on a straight line?  
- Tails are not significantly above or below line?  Some tail deviation is ok.
- No sudden "jumps"?  This indicates many $Y$'s which have the same value, such as insurance claims which all have the exact value of \$100.00 or $0.00.


```r
plot(model, which = 2)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-39-1.png" width="672" />

## Log transforms of continuous predictors

When a log link is used, taking the natural logs of continuous variables allows for the scale of each predictor to match the scale of the thing that they are predicting, the log of the mean of the response.  In addition, when the distribution of the continuous variable is skewed, taking the log helps to make it more symmetric.

After taking the log of a predictor, the interpretation becomes a *power transform* of the original variable.  

For $\mu$ the mean response,

$$log(\mu) = \beta_0 + \beta_1 log(X)$$
To solve for $\mu$, take the exonent of both sides

$$\mu = e^{\beta_1} e^{\beta_1 log(X)} = e^{\beta_0} X^{\beta_1}$$


## Reference levels

When a categorical variable is used in a GLM, the model actually uses indicator variables for each level.  The default reference level is the order of the R factors.  For the `sex` variable, the order is `female` and then `male`.  This means that the base level is `female` by default.


```r
health_insurance$sex %>% as.factor() %>% levels()
```

```
## [1] "female" "male"
```

Why does this matter?  Statistically, the coefficients are most stable when there are more observations.


```r
health_insurance$sex %>% as.factor() %>% summary()
```

```
## female   male 
##    662    676
```

There is already a function to do this in the `tidyverse` called `fct_infreq`.  Let's quickly fix the `sex` column so that these factor levels are in order of frequency.


```r
health_insurance <- health_insurance %>% 
  mutate(sex = fct_infreq(sex))
```

Now `male` is the base level.


```r
health_insurance$sex %>% as.factor() %>% levels()
```

```
## [1] "male"   "female"
```

## Interactions

An interaction occurs when the effect of a variable on the response is different depending on the level of other variables in the model.

Consider this model:

Let $x_2$ be an indicator variable, which is 1 for some observations and 0 otherwise.  

$$\hat{y_i} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_1 x_2$$

There are now two different linear models dependong on whether `x_1` is 0 or 1.

When $x_1 = 0$,

$$\hat{y_i} = \beta_0  + \beta_2 x_2$$

and when $x_1 = 1$

$$\hat{y_i} = \beta_0 + \beta_1 + \beta_2 x_2 + \beta_3 x_2$$
By rewriting this we can see that the intercept changes from $\beta_0$ to $\beta_0^*$ and the slope changes from $\beta_1$ to $\beta_1^*$

$$
(\beta_0 + \beta_1) + (\beta_2 + \beta_3 ) x_2 \\
 = \beta_0^* + \beta_1^* x_2
$$

The SOA's modules give an example with the using age and gender as below.  This is not a very strong interaction, as the slopes are almost identical across `gender`.


```r
interactions %>% 
  ggplot(aes(age, actual, color = gender)) + 
  geom_line() + 
  labs(title = "Age vs. Actual by Gender", 
       subtitle = "Interactions imply different slopes",
       caption= "data: interactions")
```

<div class="figure">
<img src="05-linear-models_files/figure-html/unnamed-chunk-44-1.png" alt="Example of weak interaction" width="672" />
<p class="caption">(\#fig:unnamed-chunk-44)Example of weak interaction</p>
</div>

Here is a clearer example from the `auto_claim` data. The lines show the slope of a linear model, assuming that only `BLUEBOOK` and `CAR_TYPE` were predictors in the model.  You can see that the slope for Sedans and Sports Cars is higher than for Vans and Panel Trucks.  


```r
auto_claim %>% 
  sample_frac(0.2) %>% 
  ggplot(aes(log(CLM_AMT), log(BLUEBOOK), color = CAR_TYPE)) + 
  geom_point(alpha = 0.3) + 
  geom_smooth(method = "lm", se = F) + 
  labs(title = "Kelly Bluebook Value vs Claim Amount")
```

<div class="figure">
<img src="05-linear-models_files/figure-html/unnamed-chunk-45-1.png" alt="Example of strong interaction" width="672" />
<p class="caption">(\#fig:unnamed-chunk-45)Example of strong interaction</p>
</div>

Any time that the effect that one variable has on the response is different depending on the value of other variables we say that there is an interaction.  We can also use an hypothesis test with a GLM to check this.  Simply include an interaction term and see if the coefficient is zero at the desired significance level.


## Offsets

In certain situations, it is convenient to include a constant term in the linear predictor.  This is the same as including a variable that has a coefficient equal to 1.  We call this an *offset*.

$$g(\mu) = \beta_0 + \beta_1 X_1 + ... + \beta_p X_p + \text{offset}$$

## Tweedie regression

While this topic is briefly mentioned on the modules, the only R libraries which support Tweedie Regression (`statmod` and `tweedie`) are not on the syllabus, and so there is no way that the SOA could ask you to build a tweedie model. This means that you can be safely skip this section.

## Combinations of Link Functions and Target Distributions

What is an example of when to use a log link with a guassian response?  What about a Gamma family with an inverse link?  What about an inverse Gaussian response and an inverse square link?  As these questions illustrate, there are many combinations of link and response family.  In the real world, a model never fits perfectly, and so often these choices come down to the judgement of the modeler - which model is the best fit and meets the business objectives?

However, there is one way that we can know for certain which link and response family is the best, and that is if we generate the data ourselves.  

Recall that a GLM has two parts:

1. A **random component**: $Y|X \sim \text{some exponential family distribution}$

2. A **link function**: between the random component and the covariates: $g(\mu(X)) = X\beta$ where $\mu = E[Y|X]$

**Following this recipe, we can simulate data from any combination of link function and response family.  This helps us to understand the GLM framework very clearly.**

### Gaussian Response with Log Link

We create a function that takes in data $x$ and returns a guassian random variable that has mean equal to the inverse link, which in the case of a log link is the exponent.  We add 10 to $x$ so that the values will always be positive, as will be described later on.


```r
sim_norm <- function(x) {
  rnorm(1, mean = exp(10 + x), sd = 1)
}
```

The values of $X$ do not need to be normal.  The above assumption is merely that the mean of the response $Y$ is related to $X$ through the link function, `mean = exp(10 + x)`, and that the distribution is normal.  This has been accomplished with `rnorm` already.  For illustration, here we use $X$'s from a uniform distribution.


```r
data <- tibble(x = runif(500)) %>% 
  mutate(y = x %>% map_dbl(sim_norm))
```

We already know what the answer is: a gaussian response with a log link.  We fit a GLM and see a perfect fit.


```r
glm <- glm(y ~ x, family = gaussian(link = "log"), data = data)

summary(glm)
```

```
## 
## Call:
## glm(formula = y ~ x, family = gaussian(link = "log"), data = data)
## 
## Deviance Residuals: 
##      Min        1Q    Median        3Q       Max  
## -3.05488  -0.73818  -0.01268   0.71014   2.93377  
## 
## Coefficients:
##              Estimate Std. Error t value Pr(>|t|)    
## (Intercept) 1.000e+01  2.981e-06 3354536   <2e-16 ***
## x           1.000e+00  4.383e-06  228152   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for gaussian family taken to be 1.061249)
## 
##     Null deviance: 5.817e+10  on 499  degrees of freedom
## Residual deviance: 5.285e+02  on 498  degrees of freedom
## AIC: 1452.7
## 
## Number of Fisher Scoring iterations: 2
```

```r
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-48-1.png" width="672" />

### Gaussian Response with Inverse Link

The same steps are repeated except the link function is now the inverse, `mean = 1/x`.  We see that some values of $Y$ are negative, which is ok.


```r
sim_norm <- function(x) {
  rnorm(1, mean = 1/x, 1)
}

data <- tibble(x = runif(500)) %>% 
  mutate(y = x %>% map_dbl(sim_norm))
summary(data)
```

```
##        x                  y          
##  Min.   :0.002351   Min.   : -1.392  
##  1st Qu.:0.278258   1st Qu.:  1.149  
##  Median :0.528553   Median :  2.287  
##  Mean   :0.509957   Mean   :  6.875  
##  3rd Qu.:0.760526   3rd Qu.:  4.014  
##  Max.   :0.999992   Max.   :425.760
```


```r
glm <- glm(y ~ x, family = gaussian(link = "inverse"), data = data)

summary(glm)
```

```
## 
## Call:
## glm(formula = y ~ x, family = gaussian(link = "inverse"), data = data)
## 
## Deviance Residuals: 
##      Min        1Q    Median        3Q       Max  
## -3.11464  -0.77276  -0.02954   0.70110   2.50767  
## 
## Coefficients:
##              Estimate Std. Error t value Pr(>|t|)    
## (Intercept) 1.605e-06  1.238e-05    0.13    0.897    
## x           9.983e-01  4.032e-03  247.58   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for gaussian family taken to be 1.080454)
## 
##     Null deviance: 383534.20  on 499  degrees of freedom
## Residual deviance:    538.07  on 498  degrees of freedom
## AIC: 1461.6
## 
## Number of Fisher Scoring iterations: 4
```

```r
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-50-1.png" width="672" />

### Gaussian Response with Identity Link

And now the link is the identity, `mean = x`.


```r
sim_norm <- function(x) {
  rnorm(1, mean = x, 1)
}

data <- tibble(x = rnorm(500)) %>% 
  mutate(y = x %>% map_dbl(sim_norm))

glm <- glm(y ~ x, family = gaussian(link = "identity"), data = data)

summary(glm)
```

```
## 
## Call:
## glm(formula = y ~ x, family = gaussian(link = "identity"), data = data)
## 
## Deviance Residuals: 
##     Min       1Q   Median       3Q      Max  
## -2.8731  -0.6460   0.0225   0.6519   3.3242  
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  0.02411    0.04503   0.535    0.593    
## x            1.01347    0.04599  22.035   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for gaussian family taken to be 1.0125)
## 
##     Null deviance: 995.82  on 499  degrees of freedom
## Residual deviance: 504.23  on 498  degrees of freedom
## AIC: 1429.1
## 
## Number of Fisher Scoring iterations: 2
```

```r
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-51-1.png" width="672" />

### Gaussian Response with Log Link and Negative Values

By Gaussian response we say that the *mean* of the response is Gaussian.  The range of a normal random variable is $(-\infty, +\infty)$, which means that negative values are always possible.  Now, if the mean is a large positive number, than negative values are much less likely but still possible:  about 95% of the observations will be within 2 standard deviations of the mean.

We see below that there are some $Y$ values which are negative.


```r
sim_norm <- function(x) {
  rnorm(1, mean = exp(x), sd = 1)
}

data <- tibble(x = runif(500)) %>% 
  mutate(y = x %>% map_dbl(sim_norm))
summary(data)
```

```
##        x                   y         
##  Min.   :0.0002768   Min.   :-1.505  
##  1st Qu.:0.2282455   1st Qu.: 0.947  
##  Median :0.5205783   Median : 1.660  
##  Mean   :0.5081372   Mean   : 1.680  
##  3rd Qu.:0.7499811   3rd Qu.: 2.424  
##  Max.   :0.9984118   Max.   : 4.707
```

We can also see this from the histogram.


```r
data %>% ggplot(aes(y)) + geom_density( fill = 1, alpha = 0.3)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-53-1.png" width="672" style="display: block; margin: auto;" />

If we try to fit a GLM with a log link, there is an error.  


```r
glm <- glm(y ~ x, family = gaussian(link = "log"), data = data)
```

`Error in eval(family$initialize) : cannot find valid starting values: please specify some`

This is because the domain of the natural logarithm only includes positive numbers, and we just tried to take the log of negative numbers.

Our initial reaction might be to add some constant to each $Y$, say 10 for instance, so that they are all positive.  This does produce a model which is a good fit.


```r
glm <- glm(y + 10 ~ x, family = gaussian(link = "log"), data = data)
summary(glm)
```

```
## 
## Call:
## glm(formula = y + 10 ~ x, family = gaussian(link = "log"), data = data)
## 
## Deviance Residuals: 
##      Min        1Q    Median        3Q       Max  
## -3.14633  -0.63601  -0.01264   0.70930   2.87307  
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept) 2.386801   0.007862  303.58   <2e-16 ***
## x           0.138190   0.012846   10.76   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for gaussian family taken to be 1.017812)
## 
##     Null deviance: 624.76  on 499  degrees of freedom
## Residual deviance: 506.87  on 498  degrees of freedom
## AIC: 1431.8
## 
## Number of Fisher Scoring iterations: 4
```

```r
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-55-1.png" width="672" />

We see that on average, the predictions are 10 higher than the target.  This is no surprise since $E[Y + 10] = E[Y] + 10$.


```r
y <- data$y 
y_hat <- predict(glm, type = "response")
mean(y_hat) - mean(y)
```

```
## [1] 9.999967
```

But we see that the actual predictions are bad.  If we were to loot at the R-squared, MAE, RMSE, or any other metric it would tell us the same story.  This is because our GLM assumption is **not** that $Y$ is related to the link function of $X$, but that the **mean** of $Y$ is.


```r
tibble(y = y, y_hat = y_hat - 10) %>% ggplot(aes(y, y_hat)) + geom_point()
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-57-1.png" width="672" />

One solution is to adjust the $X$ which the model is based on.  Add a constant term to $X$ so that the mean of $Y$ is larger, and hence $Y$ is non zero.  While is a viable approach in the case of only one predictor variable, with more predictors this would not be easy to do.


```r
data <- tibble(x = runif(500) + 10) %>% 
  mutate(y = x %>% map_dbl(sim_norm))
summary(data)
```

```
##        x               y        
##  Min.   :10.00   Min.   :22040  
##  1st Qu.:10.27   1st Qu.:28835  
##  Median :10.50   Median :36402  
##  Mean   :10.50   Mean   :37838  
##  3rd Qu.:10.75   3rd Qu.:46688  
##  Max.   :11.00   Max.   :59756
```

```r
glm <- glm(y ~ x, family = gaussian(link = "log"), data = data)
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-58-1.png" width="672" />

A better approach may be to use an inverse link even though the data was generated from a log link.  This is a good illustration of the saying "all models are wrong, but some are useful" in that the statistical assumption of the model is not correct but the model still works.


```r
data <- tibble(x = runif(500)) %>% 
  mutate(y = x %>% map_dbl(sim_norm))
glm <- glm(y ~ x, family = gaussian(link = "inverse"), data = data)
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-59-1.png" width="672" />

```r
summary(glm)
```

```
## 
## Call:
## glm(formula = y ~ x, family = gaussian(link = "inverse"), data = data)
## 
## Deviance Residuals: 
##      Min        1Q    Median        3Q       Max  
## -2.63660  -0.71949  -0.02573   0.70123   2.68053  
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  0.87559    0.04503   19.44   <2e-16 ***
## x           -0.53090    0.05703   -9.31   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## (Dispersion parameter for gaussian family taken to be 1.104314)
## 
##     Null deviance: 662.67  on 499  degrees of freedom
## Residual deviance: 549.95  on 498  degrees of freedom
## AIC: 1472.5
## 
## Number of Fisher Scoring iterations: 6
```

### Gamma Response with Log Link

The gamma distribution with rate parameter $\alpha$ and scale parameter $\theta$ is density.

$$f(y) = \frac{(y/\theta)^\alpha}{x \Gamma(\alpha)}e^{-x/\theta}$$

The mean is $\alpha\theta$.

Let's use a gamma with shape 2 and scale 0.5, which has mean 1.  


```r
gammas <- rgamma(500, shape=2, scale = 0.5)
mean(gammas)
```

```
## [1] 1.018104
```

We then generate random gamma values.  Because the mean now depends on two paramters instead of one, which was just $\mu$ in the Guassian case, we need to use a slightly different approach to simulate the random values.  The link function here is seen in `exp(x)`.


```r
#random component
x <- runif(1000, min=0, max=100)

#relate Y to X with a log link function
y <- gammas*exp(x)

data <- tibble(x = x, y  = y)
summary(data)
```

```
##        x                 y            
##  Min.   : 0.1447   Min.   :0.000e+00  
##  1st Qu.:25.0189   1st Qu.:4.231e+10  
##  Median :49.2899   Median :1.476e+21  
##  Mean   :50.0386   Mean   :2.544e+41  
##  3rd Qu.:76.4823   3rd Qu.:8.476e+32  
##  Max.   :99.8365   Max.   :2.595e+43
```

As expected, the residual plots are all perfect because the model is perfect.


```r
glm <- glm(y ~ x, family = Gamma(link = "log"), data = data)
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-62-1.png" width="672" />

If we had tried using an inverse instead of the log, the residual plots would look much worse.


```r
glm <- glm(y ~ x, family = Gamma(link = "inverse"), data = data)
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

```
## Warning in sqrt(crit * p * (1 - hh)/hh): NaNs produced

## Warning in sqrt(crit * p * (1 - hh)/hh): NaNs produced
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-63-1.png" width="672" />


### Gamma with Inverse Link

With the inverse link, the mean has a factor `1/(x + 1)`.  Note that we need to add 1 to x to avoid dividing by zero.


```r
#relate Y to X with a log link function
y <- gammas*1/(x + 1)

data <- tibble(x = x, y  = y)
summary(data)
```

```
##        x                 y            
##  Min.   : 0.1447   Min.   :0.0005573  
##  1st Qu.:25.0189   1st Qu.:0.0095364  
##  Median :49.2899   Median :0.0177203  
##  Mean   :50.0386   Mean   :0.0454184  
##  3rd Qu.:76.4823   3rd Qu.:0.0383153  
##  Max.   :99.8365   Max.   :1.5248073
```


```r
glm <- glm(y ~ x, family = Gamma(link = "inverse"), data = data)
par(mfrow = c(2,2))
plot(glm, cex = 0.4)
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-65-1.png" width="672" />

# GLM variable selection

## Stepwise subset selection

In theory, we could test all possible combinations of variables and interaction terms.  This includes all $p$ models with one predictor, all p-choose-2 models with two predictors, all p-choose-3 models with three predictors, and so forth.  Then we take whichever model has the best performance as the final model.

This "brute force" approach is statistically ineffective: the more variables which are searched, the higher the chance of finding models that overfit.

A subtler method, known as *stepwise selection*, reduces the chances of overfitting by only looking at the most promising models.  

**Forward Stepwise Selection:**

1. Start with no predictors in the model;
2. Evaluate all $p$ models which use only one predictor and choose the one with the best performance (highest $R^2$ or lowest $\text{RSS}$);
3. Repeat the process when adding one additional predictor, and continue until there is a model with one predictor, a model with two predictors, a model with three predictors, and so forth until there are $p$ models;
4. Select the single best model which has the best $\text{AIC}$,$\text{BIC}$, or adjusted $R^2$.

**Backward Stepwise Selection:**

1. Start with a model that contains all predictors;
2. Create a model which removes all predictors;
3. Choose the best model which removes all-but-one predictor;
4. Choose the best model which removes all-but-two predictors;
5. Continue until there are $p$ models;
6. Select the single best model which has the best $\text{AIC}$,$\text{BIC}$, or adjusted $R^2$.

**Both Forward & Backward Selection:**

A hybrid approach is to consider use both forward and backward selection.  This is done by creating two lists of variables at each step, one from forward and one from backward selection.  Then variables from *both* lists are tested to see if adding or subtracting from the current model would improve the fit or not.  ISLR does not mention this directly, however, by default the `stepAIC` function uses a default of `both`.

>**Tip**: Always load the `MASS` library before `dplyr` or `tidyverse`.  Otherwise there will be conflicts as there are functions named `select()` and `filter()` in both.  Alternatively, specify the library in the function call with `dplyr::select()`.

| Readings |  | 
|-------|---------|
| [CAS Monograph 5 Chapter 2](https://contentpreview.s3.us-east-2.amazonaws.com/CAS+Monograph+5+-+Generalized+Linear+Models+for+Insurance+Ratemaking.pdf) |  |


## Penalized Linear Models

One of the main weaknesses of the GLM, including all linear models in this chapter, is that the features need to be selected by hand.  Stepwise selection helps to improve this process, but fails when the inputs are correlated and often has a strong dependence on seemingly arbitrary choices of evaluation metrics such as using AIC or BIC and forward or backwise directions.  

The Bias Variance Tradoff is about finding the lowest error by changing the flexibility of the model. Penalization methods use a parameter to control for this flexibility directly.  

Earlier on we said that the linear model minimizes the sum of square terms, known as the residual sum of squares (RSS)

$$
\text{RSS} = \sum_i(y_i - \hat{y})^2 = \sum_i(y_i - \beta_0 - \sum_{j = 1}^p\beta_j x_{ij})^2
$$

This loss function can be modified so that models which include more (and larger) coefficients are considered as worse.  In other words, when there are more $\beta$'s, or $\beta$'s which are larger, the RSS is higher.

## Ridge Regression

Ridge regression adds a penalty term which is proportional to the square of the sum of the coefficients.  This is known as the "L2" norm.

$$
\sum_i(y_i - \beta_0 - \sum_{j = 1}^p\beta_j x_{ij})^2 + \lambda \sum_{j = 1}^p\beta_j^2
$$

This $\lambda$ controls how much of a penalty is imposed on the size of the coefficients.  When $\lambda$ is high, simpler models are treated more favorably because the $\sum_{j = 1}^p\beta_j^2$ carries more weight.  Conversely, then $\lambda$ is low, complex models are more favored.  When $\lambda = 0$, we have an ordinary GLM.

## Lasso

The official name is the Least Absolute Shrinkage and Selection Operator, but the common name is just "the lasso".  Just as with Ridge regression, we want to favor simpler models; however, we also want to *select* variables.  This is the same as forcing some coefficients to be equal to 0.

Instead of taking the square of the coefficients (L2 norm), we take the absolute value (L1 norm).  

$$
\sum_i(y_i - \beta_0 - \sum_{j = 1}^p\beta_j x_{ij})^2 + \lambda \sum_{j = 1}^p|\beta_j|
$$

In ISLR, Hastie et al show that this results in coefficients being forced to be exactly 0.  This is extremely useful because it means that by changing $\lambda$, we can select how many variables to use in the model.

**Note**: While any response family is possible with penalized regression, in R, only the Gaussian family is possible in the library `glmnet`, and so this is the only type of question that the SOA can ask.

## Elastic Net

The Elastic Net uses a penalty term which is between the L1 and L2 norms. The penalty term is a weighted average using the mixing parameter $0 \leq \alpha \leq 1$. The loss fucntion is then

$$\text{RSS} + (1 - \alpha)/2 \sum_{j = 1}^{p}\beta_j^2 + \alpha \sum_{j = 1}^p |\beta_j|$$
When $\alpha = 1$ is turns into a Lasso; when $\alpha = 1$ this is the Ridge model. 

Luckily, none of this needs to be memorized.  On the exam, read the documentation in R to refresh your memory.  For the Elastic Net, the function is `glmnet`, and so running `?glmnet` will give you this info.

>**Shortcut**: When using complicated functions on the exam, use `?function_name` to get the documentation.

## Advantages and disadvantages

**Elastic Net/Lasso/Ridge Advantages**

- All benefits from GLMS
- Automatic variable selection for Lasso; smaller coefficients for Ridge
- Better predictive power than GLM

**Elastic Net/Lasso/Ridge Disadvantages**

- All cons of GLMs

| Readings |  | 
|-------|---------|
| ISLR 6.1 Subset Selection  | |
| ISLR 6.2 Shrinkage Methods|  |




## Example: Ridge Regression



We will use the `glmnet` package in order to perform ridge regression and
the lasso. The main function in this package is `glmnet()`, which can be used
to fit ridge regression models, lasso models, and more. This function has
slightly different syntax from other model-fitting functions that we have
encountered thus far in this book. In particular, we must pass in an $x$
matrix as well as a $y$ vector, and we do not use the $y \sim x$ syntax.

Before proceeding, let's first ensure that the missing values have
been removed from the data, as described in the previous lab.


```r
Hitters = na.omit(Hitters)
```

We will now perform ridge regression and the lasso in order to predict `Salary` on
the `Hitters` data. Let's set up our data:


```r
x = model.matrix(Salary~., Hitters)[,-1] # trim off the first column
                                         # leaving only the predictors
y = Hitters %>%
  select(Salary) %>%
  unlist() %>%
  as.numeric()
```

The `model.matrix()` function is particularly useful for creating $x$; not only
does it produce a matrix corresponding to the 19 predictors but it also
automatically transforms any qualitative variables into dummy variables.
The latter property is important because `glmnet()` can only take numerical,
quantitative inputs.

The `glmnet()` function has an alpha argument that determines what type
of model is fit. If `alpha = 0` then a ridge regression model is fit, and if `alpha = 1`
then a lasso model is fit. We first fit a ridge regression model:


```r
grid = 10^seq(10, -2, length = 100)
ridge_mod = glmnet(x, y, alpha = 0, lambda = grid)
```

By default the `glmnet()` function performs ridge regression for an automatically
selected range of $\lambda$ values. However, here we have chosen to implement
the function over a grid of values ranging from $\lambda = 10^10$ to $\lambda = 10^{-2}$, essentially covering the full range of scenarios from the null model containing
only the intercept, to the least squares fit. 

As we will see, we can also compute
model fits for a particular value of $\lambda$ that is not one of the original
grid values. Note that by default, the `glmnet()` function standardizes the
variables so that they are on the same scale. To turn off this default setting,
use the argument `standardize = FALSE`.

Associated with each value of $\lambda$ is a vector of ridge regression coefficients,
stored in a matrix that can be accessed by `coef()`. In this case, it is a $20 \times 100$
matrix, with 20 rows (one for each predictor, plus an intercept) and 100
columns (one for each value of $\lambda$).


```r
dim(coef(ridge_mod))
```

```
## [1]  20 100
```

We expect the coefficient estimates to be much smaller, in terms of $l_2$ norm,
when a large value of $\lambda$ is used, as compared to when a small value of $\lambda$ is
used. These are the coefficients when $\lambda = 11498$, along with their $l_2$ norm:


```r
ridge_mod$lambda[50] #Display 50th lambda value
```

```
## [1] 11497.57
```

```r
coef(ridge_mod)[,50] # Display coefficients associated with 50th lambda value
```

```
##   (Intercept)         AtBat          Hits         HmRun          Runs 
## 407.356050200   0.036957182   0.138180344   0.524629976   0.230701523 
##           RBI         Walks         Years        CAtBat         CHits 
##   0.239841459   0.289618741   1.107702929   0.003131815   0.011653637 
##        CHmRun         CRuns          CRBI        CWalks       LeagueN 
##   0.087545670   0.023379882   0.024138320   0.025015421   0.085028114 
##     DivisionW       PutOuts       Assists        Errors    NewLeagueN 
##  -6.215440973   0.016482577   0.002612988  -0.020502690   0.301433531
```

```r
sqrt(sum(coef(ridge_mod)[-1,50]^2)) # Calculate l2 norm
```

```
## [1] 6.360612
```

In contrast, here are the coefficients when $\lambda = 705$, along with their $l_2$
norm. Note the much larger $l_2$ norm of the coefficients associated with this
smaller value of $\lambda$.


```r
ridge_mod$lambda[60] #Display 60th lambda value
```

```
## [1] 705.4802
```

```r
coef(ridge_mod)[,60] # Display coefficients associated with 60th lambda value
```

```
##  (Intercept)        AtBat         Hits        HmRun         Runs          RBI 
##  54.32519950   0.11211115   0.65622409   1.17980910   0.93769713   0.84718546 
##        Walks        Years       CAtBat        CHits       CHmRun        CRuns 
##   1.31987948   2.59640425   0.01083413   0.04674557   0.33777318   0.09355528 
##         CRBI       CWalks      LeagueN    DivisionW      PutOuts      Assists 
##   0.09780402   0.07189612  13.68370191 -54.65877750   0.11852289   0.01606037 
##       Errors   NewLeagueN 
##  -0.70358655   8.61181213
```

```r
sqrt(sum(coef(ridge_mod)[-1,60]^2)) # Calculate l2 norm
```

```
## [1] 57.11001
```

We can use the `predict()` function for a number of purposes. For instance,
we can obtain the ridge regression coefficients for a new value of $\lambda$, say 50:


```r
predict(ridge_mod, s=50, type="coefficients")[1:20,]
```

```
##   (Intercept)         AtBat          Hits         HmRun          Runs 
##  4.876610e+01 -3.580999e-01  1.969359e+00 -1.278248e+00  1.145892e+00 
##           RBI         Walks         Years        CAtBat         CHits 
##  8.038292e-01  2.716186e+00 -6.218319e+00  5.447837e-03  1.064895e-01 
##        CHmRun         CRuns          CRBI        CWalks       LeagueN 
##  6.244860e-01  2.214985e-01  2.186914e-01 -1.500245e-01  4.592589e+01 
##     DivisionW       PutOuts       Assists        Errors    NewLeagueN 
## -1.182011e+02  2.502322e-01  1.215665e-01 -3.278600e+00 -9.496680e+00
```

We now split the samples into a training set and a test set in order
to estimate the test error of ridge regression and the lasso.


```r
set.seed(1)

train = Hitters %>%
  sample_frac(0.5)

test = Hitters %>%
  setdiff(train)

x_train = model.matrix(Salary~., train)[,-1]
x_test = model.matrix(Salary~., test)[,-1]

y_train = train %>%
  select(Salary) %>%
  unlist() %>%
  as.numeric()

y_test = test %>%
  select(Salary) %>%
  unlist() %>%
  as.numeric()
```

Next we fit a ridge regression model on the training set, and evaluate
its MSE on the test set, using $\lambda = 4$. Note the use of the `predict()`
function again: this time we get predictions for a test set, by replacing
`type="coefficients"` with the `newx` argument.


```r
ridge_mod = glmnet(x_train, y_train, alpha=0, lambda = grid, thresh = 1e-12)
ridge_pred = predict(ridge_mod, s = 4, newx = x_test)
mean((ridge_pred - y_test)^2)
```

```
## [1] 139858.6
```

The test MSE is 101242.7. Note that if we had instead simply fit a model
with just an intercept, we would have predicted each test observation using
the mean of the training observations. In that case, we could compute the
test set MSE like this:


```r
mean((mean(y_train) - y_test)^2)
```

```
## [1] 224692.1
```

We could also get the same result by fitting a ridge regression model with
a very large value of $\lambda$. Note that `1e10` means $10^{10}$.


```r
ridge_pred = predict(ridge_mod, s = 1e10, newx = x_test)
mean((ridge_pred - y_test)^2)
```

```
## [1] 224692.1
```

So fitting a ridge regression model with $\lambda = 4$ leads to a much lower test
MSE than fitting a model with just an intercept. We now check whether
there is any benefit to performing ridge regression with $\lambda = 4$ instead of
just performing least squares regression. Recall that least squares is simply
ridge regression with $\lambda = 0$.

\* Note: In order for `glmnet()` to yield the **exact** least squares coefficients when $\lambda = 0$,
we use the argument `exact=T` when calling the `predict()` function. Otherwise, the
`predict()` function will interpolate over the grid of $\lambda$ values used in fitting the
`glmnet()` model, yielding approximate results. Even when we use `exact = T`, there remains
a slight discrepancy in the third decimal place between the output of `glmnet()` when
$\lambda = 0$ and the output of `lm()`; this is due to numerical approximation on the part of
`glmnet()`.


```r
ridge_pred = predict(ridge_mod, s = 0, x = x_train, y = y_train, newx = x_test, exact = T)
mean((ridge_pred - y_test)^2)
```

```
## [1] 175051.7
```

```r
lm(Salary~., data = train)
```

```
## 
## Call:
## lm(formula = Salary ~ ., data = train)
## 
## Coefficients:
## (Intercept)        AtBat         Hits        HmRun         Runs          RBI  
##   2.398e+02   -1.639e-03   -2.179e+00    6.337e+00    7.139e-01    8.735e-01  
##       Walks        Years       CAtBat        CHits       CHmRun        CRuns  
##   3.594e+00   -1.309e+01   -7.136e-01    3.316e+00    3.407e+00   -5.671e-01  
##        CRBI       CWalks      LeagueN    DivisionW      PutOuts      Assists  
##  -7.525e-01    2.347e-01    1.322e+02   -1.346e+02    2.099e-01    6.229e-01  
##      Errors   NewLeagueN  
##  -4.616e+00   -8.330e+01
```

```r
predict(ridge_mod, s = 0, x = x_train, y = y_train, exact = T, type="coefficients")[1:20,]
```

```
##   (Intercept)         AtBat          Hits         HmRun          Runs 
##  239.83274953   -0.00175359   -2.17853087    6.33694957    0.71369687 
##           RBI         Walks         Years        CAtBat         CHits 
##    0.87329878    3.59421378  -13.09231408   -0.71351092    3.31523605 
##        CHmRun         CRuns          CRBI        CWalks       LeagueN 
##    3.40701392   -0.56709530   -0.75240961    0.23467433  132.15949536 
##     DivisionW       PutOuts       Assists        Errors    NewLeagueN 
## -134.58503816    0.20992473    0.62288126   -4.61583857  -83.29432536
```

It looks like we are indeed improving over regular least-squares! Side note: in general, if we want to fit a (unpenalized) least squares model, then
we should use the `lm()` function, since that function provides more useful
outputs, such as standard errors and $p$-values for the coefficients.

Instead of arbitrarily choosing $\lambda = 4$, it would be better to
use cross-validation to choose the tuning parameter $\lambda$. We can do this using
the built-in cross-validation function, `cv.glmnet()`. By default, the function
performs 10-fold cross-validation, though this can be changed using the
argument `folds`. Note that we set a random seed first so our results will be
reproducible, since the choice of the cross-validation folds is random.


```r
set.seed(1)
cv.out = cv.glmnet(x_train, y_train, alpha = 0) # Fit ridge regression model on training data
plot(cv.out) # Draw plot of training MSE as a function of lambda
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-79-1.png" width="672" />

```r
bestlam = cv.out$lambda.min  # Select lamda that minimizes training MSE
bestlam
```

```
## [1] 326.1406
```

Therefore, we see that the value of $\lambda$ that results in the smallest cross-validation
error is 339.1845 What is the test MSE associated with this value of
$\lambda$?


```r
ridge_pred = predict(ridge_mod, s = bestlam, newx = x_test) # Use best lambda to predict test data
mean((ridge_pred - y_test)^2) # Calculate test MSE
```

```
## [1] 140056.2
```

This represents a further improvement over the test MSE that we got using
$\lambda = 4$. Finally, we refit our ridge regression model on the full data set,
using the value of $\lambda$ chosen by cross-validation, and examine the coefficient
estimates.


```r
out = glmnet(x, y, alpha = 0) # Fit ridge regression model on full dataset
predict(out, type = "coefficients", s = bestlam)[1:20,] # Display coefficients using lambda chosen by CV
```

```
##  (Intercept)        AtBat         Hits        HmRun         Runs          RBI 
##  15.44835008   0.07716945   0.85906253   0.60120339   1.06366687   0.87936073 
##        Walks        Years       CAtBat        CHits       CHmRun        CRuns 
##   1.62437580   1.35296287   0.01134998   0.05746377   0.40678422   0.11455696 
##         CRBI       CWalks      LeagueN    DivisionW      PutOuts      Assists 
##   0.12115916   0.05299953  22.08942749 -79.03490973   0.16618830   0.02941513 
##       Errors   NewLeagueN 
##  -1.36075644   9.12528398
```

As expected, none of the coefficients are exactly zero - ridge regression does not
perform variable selection!

## Example: The Lasso

We saw that ridge regression with a wise choice of $\lambda$ can outperform least
squares as well as the null model on the Hitters data set. We now ask
whether the lasso can yield either a more accurate or a more interpretable
model than ridge regression. In order to fit a lasso model, we once again
use the `glmnet()` function; however, this time we use the argument `alpha=1`.
Other than that change, we proceed just as we did in fitting a ridge model:


```r
lasso_mod = glmnet(x_train, y_train, alpha = 1, lambda = grid) # Fit lasso model on training data
plot(lasso_mod)                                          # Draw plot of coefficients
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-82-1.png" width="672" />

Notice that in the coefficient plot that depending on the choice of tuning
parameter, some of the coefficients are exactly equal to zero. We now
perform cross-validation and compute the associated test error:


```r
set.seed(1)
cv.out = cv.glmnet(x_train, y_train, alpha = 1) # Fit lasso model on training data
plot(cv.out) # Draw plot of training MSE as a function of lambda
```

<img src="05-linear-models_files/figure-html/unnamed-chunk-83-1.png" width="672" />

```r
bestlam = cv.out$lambda.min # Select lamda that minimizes training MSE
lasso_pred = predict(lasso_mod, s = bestlam, newx = x_test) # Use best lambda to predict test data
mean((lasso_pred - y_test)^2) # Calculate test MSE
```

```
## [1] 143273
```

This is substantially lower than the test set MSE of the null model and of
least squares, and very similar to the test MSE of ridge regression with $\lambda$
chosen by cross-validation.

However, the lasso has a substantial advantage over ridge regression in
that the resulting coefficient estimates are sparse. Here we see that 12 of
the 19 coefficient estimates are exactly zero:


```r
out = glmnet(x, y, alpha = 1, lambda = grid) # Fit lasso model on full dataset
lasso_coef = predict(out, type = "coefficients", s = bestlam)[1:20,] # Display coefficients using lambda chosen by CV
lasso_coef
```

```
##   (Intercept)         AtBat          Hits         HmRun          Runs 
##    1.27429897   -0.05490834    2.18012455    0.00000000    0.00000000 
##           RBI         Walks         Years        CAtBat         CHits 
##    0.00000000    2.29189433   -0.33767315    0.00000000    0.00000000 
##        CHmRun         CRuns          CRBI        CWalks       LeagueN 
##    0.02822467    0.21627609    0.41713051    0.00000000   20.28190194 
##     DivisionW       PutOuts       Assists        Errors    NewLeagueN 
## -116.16524424    0.23751978    0.00000000   -0.85604181    0.00000000
```

Selecting only the predictors with non-zero coefficients, we see that the lasso model with $\lambda$
chosen by cross-validation contains only seven variables:


```r
lasso_coef[lasso_coef!=0] # Display only non-zero coefficients
```

```
##   (Intercept)         AtBat          Hits         Walks         Years 
##    1.27429897   -0.05490834    2.18012455    2.29189433   -0.33767315 
##        CHmRun         CRuns          CRBI       LeagueN     DivisionW 
##    0.02822467    0.21627609    0.41713051   20.28190194 -116.16524424 
##       PutOuts        Errors 
##    0.23751978   -0.85604181
```

Practice questions:

 * How do ridge regression and the lasso improve on simple least squares?
 * In what cases would you expect ridge regression outperform the lasso, and vice versa?
 

 
## References

These examples of the Ridge and Lasso are an adaptation of p. 251-255 of "Introduction to
Statistical Learning with Applications in R" by Gareth James, Daniela Witten, Trevor Hastie and Robert
Tibshirani. Adapted by R. Jordan Crouser at Smith College for SDS293: Machine Learning (Spring 2016), and re-implemented in Fall 2016 in `tidyverse` format by Amelia McNamara and R. Jordan Crouser at Smith College.

Used with permission from Jordan Crouser at Smith College.  Additional Thanks to the following contributors on github:

* github.com/jcrouser
* github.com/AmeliaMN
* github.com/mhusseinmidd
* github.com/rudeboybert
* github.com/ijlyttle



