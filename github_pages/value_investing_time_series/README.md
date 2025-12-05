# Time-Series-Stock-Anomaly-Detection


https://samdc.shinyapps.io/value-investing-app/

This app identifies sudden shifts in stock prices by fitting ARIMA models.  Once a model has been fit, outlying price jumps are
 determined by the absolute value of the standardized residuals of the model.  A sensitivity threshold is determined by the user.
  Any stock listed on U.S. exchanges can be tested for extreme deviations for as long as it has been available.  For each 
abnormal date detected, additional stock information for a two-month window around this date is provided.

Specific examples to try are:

-	Apple (AAPL) from 2013-05-06 to 2013-11-14 as they release their third quarter results after the release of the iphone 5.
-	Goldman Sachs (GS) from 2008-01 to 2009-01 during the worst of the recession
-	S&P 500 Index (S&P) from 2016-05-10 to 2016-12-30 right after the November election

The time series is first transformed with a natural logarithm to stabilize the variance, and then an ARFIMA model is fitted with the 
`auto.arima` function from the `forecast` package.  A fractional differencing algorithm produces an approximately stationary time series to then
fit with an ARMA model. This is found by looking over all possible combinations of AR and MA coefficients and ranking by AIC and BIC.

