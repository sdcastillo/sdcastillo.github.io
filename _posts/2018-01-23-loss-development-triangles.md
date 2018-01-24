---
title: "Loss Development Triangles"
layout: post
excerpt: "This is a user-defined post excerpt. It should be displayed in place of the auto-generated excerpt or post content on index pages."
categories:
  - Layout
tags:
  - reserving
  - actuarial science
  - R
  - Excel
last_modified_at: 2018-01-04T12:43:31-05:00
---

[Read the expanded article on datascienceplus.com](https://datascienceplus.com/faster-than-excel-painlessly-merge-data-into-actuarial-loss-development-triangles-with-r/)

A frusterating task actuaries frequently encounter is combining data from separate excel files in order to create aggregate loss development triangles.  Using only Excel, the common method is to create links between the excel files which must be updated manually at each new evaluation.  This is prone to human error and is time consuming.  Using a SQL-like script with R we can automate this process to save time and reduce the liklihood of making a mistake.

[For a definition of a loss development triangle and why they are important, see Wikipedia.](https://en.wikipedia.org/wiki/Chain-ladder_method)

Example of conventional, linked triangle:

![useful image]({{ site.url }}/assets/css/labeled triangle.PNG)

**Conventional Excel Method:**
1.  Go into each excel file and calculate the data needed (e.g., paid loss net of deductible).
2.  Go into each excel file and summarise these values with a pivot table.
3.  Go into each excel file and create a link from these pivot tables to an additional file.
4.  Repeat this process for each variable needed (e.g., incurred loss net of deductible, case reserves, etc)

There is zero scalability in the above process: if there were 100 excel files, this above process would be 100 times as time-consuming.

**R Extract Method:**

1. Organize the excel files.
2. Write a script to load the files from Excel into the R working directory.
3. Combine the data first, and then ouput a single triangle file.

This process is completely scalable.

Example of R extract method:

![useful image]({{ site.url }}/assets/css/process_flowchart.PNG)

When it comes to aggregating excel files, R can be faster and more consistent than linking together each of the excel files, and once this script is set in place, making modifications to the data can be done easily by editing a few lines of code.  The only manual labor required in excel was to go into each file and rename the columns to be consistent.

[Download the code and follow along](https://github.com/sdcastillo/Loss-Development-Triangles)
