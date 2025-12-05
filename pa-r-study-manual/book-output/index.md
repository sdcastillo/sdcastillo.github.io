--- 
title: "The Predictive Analytics R Study Manual"
author: 
- "Sam Castillo"
date: "2019-10-29"
site: bookdown::bookdown_site
output: bookdown::gitbook
documentclass: book
bibliography: [book.bib, packages.bib]
biblio-style: apalike
link-citations: yes
github-repo: rstudio/bookdown-demo
description: "This will help you pass these exams"
---
# Welcome {#intro}

This book prepares you for the SOA's Predictive Analytics (PA) Exam.  

**Note:** This book is still being written and this is only a preview.

Many candidates start with prior knowledge about parts of this exam.  Very few are learning all of these topics for the first time. **This book allows you to skip the redundant sections and just focus on the new material.**  If you are new to this whole business of machine learning and R programming, great!  Every page will be useful.  

**Features**

- All data sets used are packaged in a single R library
- Clean, easy-to-read, efficient R code
- Explanations of the statistical concepts
- Tips on taking the exam
- Two **original** practice exams

# The Exam

You will have 5 hours and 15 minutes to use RStudio and Excel to fill out a report in Word on a Prometric computer.  The syllabus uses fancy language to describe the topics covered on the exam, making it sound more difficult than it should be.  A good analogy is a job description that has many complex-sounding tasks, when in reality the day-to-day operations of the employee are far simpler.

https://www.soa.org/globalassets/assets/files/edu/2019/2019-12-exam-pa-syllabus.pdf

A non-technical translation is as follows:

**Writing in Microsoft Word (30-40%)**

- Write in professional language
- Type more than 50 words-per-minute

**Manipulating Data in R (15-25%)**

- Quickly clean data sets
- Find data errors planted by the SOA
- Perform queries (aggregations, summaries, transformations)

**Making decisions based on machine learning and statistics knowledge (40-50%)**

- Understand several algorithms from a high level and be able to interpret and explain results in english
- Read R documentation about models and use this to make decisions

# Preface - What is Machine Learning?

All of use are already familiar with how to learn - by learning from our mistakes.  By repeating what is successful and avoiding what results in failure, we learn by doing, by experience, or trial-and-error.  Some study methods work well, but other methods do not.  We all know that memorizing answers without understanding concepts is an ineffective method, and that doing many practice problems is better than doing only a few.  These ideas apply to how computers learn as much as they do to how humans learn.

Take the example of preparing for an actuarial exam.  We can clearly state our objective: get as many correct answers as possible! We want to correctly predict the solution to every problem.  Said another way, we are trying to minimize the error, the percentage of incorrect problems.  Later on, we will see how choosing the objective function changes how models are fit.

The "data" are the practice problems, and the “label” is the answer (A,B,C,D,E).  We want to build a “mental model” that reads the question and predicts the answer.  The SOA suggests 100 hours per hour of exam, which means that actuaries train on hundreds of problems before the real exam.  We don’t have access to the questions that will be on the exam ahead of time, and so this represents “validation” or “holdout” data.  In the chapter on cross-validation, we will see how computers use hold-out sets to test model performance.

The more practice problems that we do, the larger the training data set, and the better our "mental model" becomes.  When we see new problems, ones which have not appeared in the practice exams, we often have a difficult time.  Problems which we have seen before are easier, and we have more confidence in our answers.  Statistics tells us that as the sample size increases, model performance tends to increase.  More difficult concepts tend to require more practice, and more complex machine learning problems require more data.

We typically save time by only doing odd-numbered problems.  This insures that we still get the same proportion of each type of question while doing fewer problems.  If we are unsure of a question, we will often seek a second opinion, or ask an online forum for help.  Later on, we will see how “down-sampling”, “bagging”, and “boosting” are all similar concepts.
