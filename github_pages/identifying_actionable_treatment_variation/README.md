# Identifying-Actionable-Treatment-Variation-in-Episodes-of-Low-Back-Pain

## [Link to the model file](http://htmlpreview.github.io/?https://github.com/sdcastillo/Identifying-Actionable-Treatment-Variation-in-Episodes-of-Low-Back-Pain/blob/master/Patient%20Pathways%20Fitted%20Model%20(1).html)

## Some Background

Low back pain impacts 84% of adults at some point in their lives, and the U.S. approximately $90 billion is spent annually in treatment.  Although there is an abundance of clinical best-practice resource, there is still significant variation in practice pattern.  The goal of this project was to identify opportunities where medical providers could pull "levers" to create healthier patient outcomes while reducing total medical expenditure.

## Data Overview

The data consisted of ~33,000 treatment episodes of low back pain from 2015-2016.  The key statistic is that the top 5% of episodes accounted for more than 50% of total cost, while all of these top 5% included a surgical procedure at some point.  These patients were isolated to be considered clinically homogeneous, in that they were all of approximately equal health and condition status.  

## Objective 

The underlying question was *why for two patients with roughly equal low back pain conditions, can one end up having surgery which runs into hundeds of thousands of dollars, while another can utilizate non-surgical orthopedic treatments that costs a fraction of this.*  This model supported an analysis examening why two patients with the same low back pain condition could end up undergoing vastly different treatment procedure.

## Methods

1. Patients are isolated to an approximately clinically homogeneous sample.
2. Potentially important, actionable features are identified with the domain knowledge of the clinical team such as whether or not the patient has had an x-ray, the number of physical therapy visits they have on record, and other various medical history characteristics.
3. Adjustments are made to account for class imbalance.
4. A random forest is fit to the bootstrapped sample and then tested on a validation subset of the data.
5.  Feature importance is interpreted from a clinical perspective.
