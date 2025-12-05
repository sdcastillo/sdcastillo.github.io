---
output:
  html_document: default
  pdf_document: default
---
# Getting started 

## Download the data

For your convenience, all data in this book, including data from prior exams and sample solutions, has been put into a library called `ExamPAData` by the author.  To access, simplly run the below lines of code to download this data.


```r
# Install remotes if it's not yet installed
# install.packages("remotes")
remotes::install_github("sdcastillo/ExamPAData")
```

Once this has run, you can access the data using `library(ExamPAData)`.  To check that this is installed correctly see if the `insurance` data set has loaded.  If this returns "object not found", then the library was not installed.


```r
library(ExamPAData)
summary(insurance)
```

```
##     district       group               age               holders       
##  Min.   :1.00   Length:64          Length:64          Min.   :   3.00  
##  1st Qu.:1.75   Class :character   Class :character   1st Qu.:  46.75  
##  Median :2.50   Mode  :character   Mode  :character   Median : 136.00  
##  Mean   :2.50                                         Mean   : 364.98  
##  3rd Qu.:3.25                                         3rd Qu.: 327.50  
##  Max.   :4.00                                         Max.   :3582.00  
##      claims      
##  Min.   :  0.00  
##  1st Qu.:  9.50  
##  Median : 22.00  
##  Mean   : 49.23  
##  3rd Qu.: 55.50  
##  Max.   :400.00
```

## Download ISLR

This book references the publically-avialable textbook "An Introduction to Statistical Learning", which can be downloaded for free

http://faculty.marshall.usc.edu/gareth-james/ISL/

If you already have R and RStudio installed then skip to "Download the data". 

## New users

Install R:

This is the engine that *runs* the code.  https://cran.r-project.org/mirrors.html

Install RStudio

This is the tool that helps you to *write* the code.  Just as MS Word creates documents, RStudio creates R scripts and other documents.  Download RStudio Desktop (the free edition) and choose a place on your computer to install it.

https://rstudio.com/products/rstudio/download/

Set the R library

R code is organized into libraries.  You want to use the exact same code that will be on the Prometric Computers.  This requires installing older versions of libraries.  Change your R library to the one which was included within the SOA's modules.


```r
.libPaths("PATH_TO_SOAS_LIBRARY/PAlibrary")
```
