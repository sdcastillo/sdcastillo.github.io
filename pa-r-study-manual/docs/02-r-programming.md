# R programming

This chapter covers the bare minimum of R programming needed for Exam PA. The book 
"R for Data Science" provides more detail.

https://r4ds.had.co.nz/

## Notebook chunks

On the Exam, you will start with an .Rmd (R Markdown) template, which organize 
code into [R Notebooks](https://bookdown.org/yihui/rmarkdown/notebook.html). 
Within each notebook, code is organized into chunks.  


```r
# This is a chunk
```

Your time is valuable.  Throughout this book, I will include useful keyboard shortcuts.

>**Shortcut:** To run everything in a chunk quickly, press `CTRL + SHIFT + ENTER`. 
To create a new chunk, use `CTRL + ALT + I`.

## Basic operations

The usual math operations apply.


```r
# Addition
1 + 2 
```

```
## [1] 3
```

```r
3 - 2
```

```
## [1] 1
```

```r
# Multiplication
2 * 2
```

```
## [1] 4
```

```r
# Division
4 / 2
```

```
## [1] 2
```

```r
# Exponentiation
2^3
```

```
## [1] 8
```

There are two assignment operators: `=` and `<-`.  The latter is preferred because 
it is specific to assigning a variable to a value.  The `=` operator is also used 
for specifying arguments in functions (see the functions section).  

> **Shortcut:** `ALT + -` creates a `<-`..


```r
# Variable assignment
y <- 2

# Equality
4 == 2
```

```
## [1] FALSE
```

```r
5 == 5
```

```
## [1] TRUE
```

```r
3.14 > 3
```

```
## [1] TRUE
```

```r
3.14 >= 3
```

```
## [1] TRUE
```

Vectors can be added just like numbers.  The `c` stands for "concatenate", which
creates vectors.


```r
x <- c(1, 2)
y <- c(3, 4)
x + y
```

```
## [1] 4 6
```

```r
x * y
```

```
## [1] 3 8
```

```r
z <- x + y
z^2
```

```
## [1] 16 36
```

```r
z / 2
```

```
## [1] 2 3
```

```r
z + 3
```

```
## [1] 7 9
```

I already mentioned `numeric` types. There are also `character` (string) types, 
`factor` types, and `boolean` types.


```r
character <- "The"
character_vector <- c("The", "Quick")
```

Character vectors can be combined with the `paste()` function.


```r
a <- "The"
b <- "Quick"
c <- "Brown"
d <- "Fox"
paste(a, b, c, d)
```

```
## [1] "The Quick Brown Fox"
```

Factors look like character vectors but can only contain a finite number of predefined 
values.

The below factor has only one "level", which is the list of assigned values.


```r
factor <- as.factor(character)
levels(factor)
```

```
## [1] "The"
```

The levels of a factor are by default in R in alphabetical order (Q comes alphabetically 
before T).


```r
factor_vector <- as.factor(character_vector)
levels(factor_vector)
```

```
## [1] "Quick" "The"
```

**In building linear models, the order of the factors matters.**  In GLMs, the 
"reference level" or "base level" should always be the level which has the most
observations.  This will be covered in the section on linear models.

Booleans are just `TRUE` and `FALSE` values.  R understands `T` or `TRUE` in the 
same way, but the latter is preferred.  When doing math, bools are converted to 
0/1 values where 1 is equivalent to TRUE and 0 FALSE.


```r
bool_true <- TRUE
bool_false <- FALSE
bool_true * bool_false
```

```
## [1] 0
```

Booleans are automatically converted into 0/1 values when there is a math operation.


```r
bool_true + 1
```

```
## [1] 2
```

Vectors work in the same way.


```r
bool_vect <- c(TRUE, TRUE, FALSE)
sum(bool_vect)
```

```
## [1] 2
```

Vectors are indexed using `[`. If you are only extracting a single element, you
should use `[[` for clarity.


```r
abc <- c("a", "b", "c")
abc[[1]]
```

```
## [1] "a"
```

```r
abc[[2]]
```

```
## [1] "b"
```

```r
abc[c(1, 3)]
```

```
## [1] "a" "c"
```

```r
abc[c(1, 2)]
```

```
## [1] "a" "b"
```

```r
abc[-2]
```

```
## [1] "a" "c"
```

```r
abc[-c(2, 3)]
```

```
## [1] "a"
```


## Lists

Lists are vectors that can hold mixed object types.


```r
my_list <- list(TRUE, "Character", 3.14)
my_list
```

```
## [[1]]
## [1] TRUE
## 
## [[2]]
## [1] "Character"
## 
## [[3]]
## [1] 3.14
```

Lists can be named.


```r
my_list <- list(bool = TRUE, character = "character", numeric = 3.14)
my_list
```

```
## $bool
## [1] TRUE
## 
## $character
## [1] "character"
## 
## $numeric
## [1] 3.14
```

The `$` operator indexes lists.


```r
my_list$numeric
```

```
## [1] 3.14
```

```r
my_list$numeric + 5
```

```
## [1] 8.14
```

Lists can also be indexed using `[[`.


```r
my_list[[1]]
```

```
## [1] TRUE
```

```r
my_list[[2]]
```

```
## [1] "character"
```


Lists can contain vectors, other lists, and any other object.


```r
everything <- list(vector = c(1, 2, 3), 
                   character = c("a", "b", "c"), 
                   list = my_list)
everything
```

```
## $vector
## [1] 1 2 3
## 
## $character
## [1] "a" "b" "c"
## 
## $list
## $list$bool
## [1] TRUE
## 
## $list$character
## [1] "character"
## 
## $list$numeric
## [1] 3.14
```

To find out the type of an object, use `class` or `str` or `summary`.


```r
class(x)
```

```
## [1] "numeric"
```

```r
class(everything)
```

```
## [1] "list"
```

```r
str(everything)
```

```
## List of 3
##  $ vector   : num [1:3] 1 2 3
##  $ character: chr [1:3] "a" "b" "c"
##  $ list     :List of 3
##   ..$ bool     : logi TRUE
##   ..$ character: chr "character"
##   ..$ numeric  : num 3.14
```

```r
summary(everything)
```

```
##           Length Class  Mode     
## vector    3      -none- numeric  
## character 3      -none- character
## list      3      -none- list
```


## Functions

You only need to understand the very basics of functions.  The big picture, though, is that
understanding functions helps you to understand *everything* in R, since R is a 
functional [programming language](http://adv-r.had.co.nz/Functional-programming.html), 
unlike Python, C, VBA, Java which are all object-oriented, or SQL which isn't 
really a language but a series of set-operations.

Functions do things.  The convention is to name a function as a verb.  The function
`make_rainbows()` would create a rainbow.  The function `summarise_vectors()` 
would summarise vectors.  Functions may or may not have an input and output.  

If you need to do something in R, there is a high probability that someone has 
already written a function to do it.  That being said, creating simple functions 
is quite useful.

Here is an example that has a side effect of printing the input:


```r
greet_me <- function(my_name){
  print(paste0("Hello, ", my_name))
}

greet_me("Future Actuary")
```

```
## [1] "Hello, Future Actuary"
```

**A function that returns something**

When returning the last evaluated expression, the `return` statement is optional.
In fact, it is discouraged by convention.


```r
add_together <- function(x, y) {
  x + y
}

add_together(2, 5)
```

```
## [1] 7
```

```r
add_together <- function(x, y) {
  # Works, but bad practice
  return(x + y)
}

add_together(2, 5)
```

```
## [1] 7
```

Binary operations in R are vectorized. In other words, they are applied element-wise.


```r
x_vector <- c(1, 2, 3)
y_vector <- c(4, 5, 6)
add_together(x_vector, y_vector)
```

```
## [1] 5 7 9
```

Many functions in R actually return lists!  This is why R objects can be indexed 
with dollar sign.


```r
library(ExamPAData)
model <- lm(charges ~ age, data = health_insurance)
model$coefficients
```

```
## (Intercept)         age 
##   3165.8850    257.7226
```

Here's a function that returns a list.


```r
sum_multiply <- function(x,y) {
  sum <- x + y
  product <- x * y
  list("Sum" = sum, "Product" = product)
}

result <- sum_multiply(2, 3)
result$Sum
```

```
## [1] 5
```

```r
result$Product
```

```
## [1] 6
```

## Data frames

You can think of a data frame as a table that is implemented as a list of vectors.


```r
df <- data.frame(
  age = c(25, 35),
  has_fsa = c(FALSE, TRUE)
)
df
```

```
##   age has_fsa
## 1  25   FALSE
## 2  35    TRUE
```

You can also work with tibbles, which are data frames but have nicer printing:


```r
# The tidyverse library has functions for making tibbles
library(tidyverse) 
```

```
## -- Attaching packages ------------------------------------------------------------------------------------- tidyverse 1.3.0 --
```

```
## v ggplot2 3.2.1     v purrr   0.3.3
## v tibble  2.1.3     v dplyr   0.8.3
## v tidyr   1.0.0     v stringr 1.4.0
## v readr   1.3.1     v forcats 0.4.0
```

```
## -- Conflicts ---------------------------------------------------------------------------------------- tidyverse_conflicts() --
## x dplyr::filter() masks stats::filter()
## x dplyr::lag()    masks stats::lag()
```

```r
df <- tibble(
  age = c(25, 35), has_fsa = c(FALSE, TRUE)
)
df
```

```
## # A tibble: 2 x 2
##     age has_fsa
##   <dbl> <lgl>  
## 1    25 FALSE  
## 2    35 TRUE
```

To index columns in a tibble, the same "$" is used as indexing a list.


```r
df$age
```

```
## [1] 25 35
```

To find the number of rows and columns, use `dim`.


```r
dim(df)
```

```
## [1] 2 2
```

To find a summary, use `summary`


```r
summary(df)
```

```
##       age        has_fsa       
##  Min.   :25.0   Mode :logical  
##  1st Qu.:27.5   FALSE:1        
##  Median :30.0   TRUE :1        
##  Mean   :30.0                  
##  3rd Qu.:32.5                  
##  Max.   :35.0
```

## Pipes

The pipe operator `%>%` is a way of making code *modular*, meaning that it can 
be written and executed in incremental steps.  Those familiar with Python's Pandas 
will be see that `%>%` is quite similar to ".".  This also makes code easier to 
read.

In five seconds, tell me what the below code is doing.


```r
log(sqrt(exp(log2(sqrt((max(c(3, 4, 16))))))))
```

```
## [1] 1
```

Getting to the answer of 1 requires starting from the inner-most nested brackets
and moving outwards from right to left.

The math notation would be slightly easier to read, but still painful.

$$log(\sqrt{e^{log_2(\sqrt{max(3,4,16)})}})$$

Here is the same algebra using the pipe.  To read this, replace the `%>%` with 
the word `THEN`.


```r
max(c(3, 4, 16)) %>% 
  sqrt() %>% 
  log2() %>% 
  exp() %>% 
  sqrt() %>% 
  log()
```

```
## [1] 1
```

```r
# max(c(3, 4, 16) THEN  # The max of 3, 4, and 16 is 16
#  sqrt() THEN          # The square root of 16 is 4
#  log2() THEN          # The log in base 2 of 4 is 2
#  exp() THEN           # The exponent of 2 is e^2
#  sqrt() THEN          # The square root of e^2 is e
#  log()                # The natural logarithm of e is 1
```

Pipes are exceptionally useful for data manipulations, which is covered in the 
next chapter.

> **Tip:** To quickly produce pipes, use `CTRL + SHIFT + M`.  

By highlighting only certain sections, we can run the code in steps as if we were
using a debugger.  This makes testing out code much faster.


```r
max(c(3, 4, 16))
```

```
## [1] 16
```


```r
max(c(3, 4, 16)) %>% 
  sqrt() 
```

```
## [1] 4
```


```r
max(c(3, 4, 16)) %>% 
  sqrt() %>% 
  log2() 
```

```
## [1] 2
```


```r
max(c(3, 4, 16)) %>% 
  sqrt() %>% 
  log2() %>% 
  exp()
```

```
## [1] 7.389056
```


```r
max(c(3, 4, 16)) %>% 
  sqrt() %>% 
  log2() %>% 
  exp() %>% 
  sqrt() 
```

```
## [1] 2.718282
```


```r
max(c(3, 4, 16)) %>% 
  sqrt() %>% 
  log2() %>% 
  exp() %>% 
  sqrt() %>% 
  log()
```

```
## [1] 1
```

## The SOA's code doesn't use pipes or dplyr, so can I skip learning this?

Yes, if you really want to.  

The advantages to learning pipes, and the reason why this manual uses them are

1) It saves you time. 
2) It will help you in real life data science projects.
3) The majority of the R community uses this style.
4) The SOA actuaries who create the Exam PA content will eventually catch on.
5) Most modern R software is designed around them.  The overall trend is towards greater adoption, as can bee seen from the CRAN download statistics [here](https://hadley.shinyapps.io/cran-downloads/) after filtering to "magrittr" which is the library where the pipe comes from. 

