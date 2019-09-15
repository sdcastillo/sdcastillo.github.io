---
title: "Bayesian-XGBoost"
layout: post
excerpt: "Machine learning models learn by looking at examples. In supervised learning, there is a known outcome, or label"
categories:
  - R Tutorial
  - Reproducible Example
tags:
  - XGBoost
  - Gradient Boosting
  - Supervised Learning
  - GBM
last_modified_at: 2019-08-02T12:43:31-05:00
---

Machine learning models learn by looking at examples. In supervised learning, there is a known outcome, or label, and by looking at examples of data across many, many examples, a relationship established between the data and the label. More examples makes it easier for the model to find patterns; fewer examples makes it more difficult to learn, and hence, leads to worse performance.

Often there are only a few examples available for certain groups in the data. In these cases case, all that the model can do is “guess”, or predict an average of the few examples present in the data.

[Prior probabilities](https://en.wikipedia.org/wiki/Prior_probability) help to solve this problem. Instead of relying on the examples present in the data by themselves, and basing the prediction entirely on the data, we can be clever about setting the initial predictions, or “guesses”, based on our own knowledge or intuition. If there are a lot of examples present in the data, more weight is given to the model’s prediction; if there are few examples, more weight is given to the prior probability.
