---
title: "Anomaly Detection for Bitcoin"
layout: post
excerpt: "When most people think of modeling, the main emphasis is on usually on making predictions or data mining.  Anomaly detection is a third major use"
categories:
  - Time Series
  - R Shiny
  - ARIMA
tags:
  - R
  - Data Visualization
  - R
  - Excel
  - R Shiny
  - ggplot2
last_modified_at: 2018-01-04T12:43:31-05:00
---

When most people think of modeling, the main emphasis is on usually on making predictions or or data mining.  Anomaly detection, or outlier classification, is a third major use for many types of models.  In a nutshell, this process involves fitting a model, calculating error for each point, and then creating a classification rule to determine which points are outliers. 

This [Shiny application]() identifies anomalous behavior in the Bitcoin Price Index [(BTC-USD)](https://finance.yahoo.com/quote/BTCUSD=X/)

![useful image]({{ site.url }}/assets/css/anomaly_detection/bitcoin_app_screenshot.PNG)

![useful image]({{ site.url }}/assets/css/anomaly_detection/with_confidence_bands.png)

![useful image]({{ site.url }}/assets/css/anomaly_detection/BTC_transformation_labeled.PNG)






