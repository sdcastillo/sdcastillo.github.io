# R programming

There are already many great R tutorials available.  To save time, this book will cover the absolute essentials.  The book "R for Data Science" provides one such introduction.

https://r4ds.had.co.nz/

## Notebook chunks

On the Exam, you will start with an .Rmd (R Markdown) template.  The way that this book writes code is in the [R Notebook](https://bookdown.org/yihui/rmarkdown/notebook.html). Learning markdown is useful for other web development and documentation tasks as well.

Code is organized into chunks.  To run everything in a chunk quickly, press `CTRL + SHIFT + ENTER`.  To create a new chunk, use `CTRL + ALT + I`.

## Basic operations

The usual math operations apply.


```r
#addition
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
#multiplication
2*2
```

```
## [1] 4
```

```r
#division
4/2
```

```
## [1] 2
```

```r
#exponentiation
2^3
```

```
## [1] 8
```

There are two assignment operators: `=` and `<-`.  The latter is preferred because it is specific to assigning a variable to a value.  The "=" operator is also used for assigning values in functions (see the functions section).  In R, the shortcut `ALT + -` creates a `<-`.


```r
#variable assignment
x = 2
y <- 2

#equality
4 == 2 #False
```

```
## [1] FALSE
```

```r
5 == 5 #true
```

```
## [1] TRUE
```

```r
3.14 > 3 #true
```

```
## [1] TRUE
```

```r
3.14 >= 3 #true
```

```
## [1] TRUE
```

Vectors can be added just like numbers.  The `c` stands for "concatenate", which creates vectors.


```r
x <- c(1,2)
y <- c(3,4)
x + y
```

```
## [1] 4 6
```

```r
x*y
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
z/2
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

Lists are like vectors but can take any type of object type.  I already mentioned `numeric` types.  There are also `character` (string) types, `factor` types, and `boolean` types.


```r
character <- "The"
character_vector <- c("The", "Quick")
```

Factors are characters that expect only specific values.  A character can take on any value.  A factor is only allowed a finite number of values.  This reduces the memory size.

The below factor has only one "level", which is the list of assigned values.


```r
factor = as.factor(character)
levels(factor)
```

```
## [1] "The"
```

The levels of a factor are by default in R in alphabetical order (Q comes alphabetically before T).


```r
factor_vector <- as.factor(character_vector)
levels(factor_vector)
```

```
## [1] "Quick" "The"
```

Booleans are just True and False values.  R understands `T` or `TRUE` in the same way.  When doing math, bools are converted to 0/1 values where 1 is equivalent to TRUE and 0 FALSE.


```r
bool_true <- T
bool_false <- F
bool_true*bool_false
```

```
## [1] 0
```

Vectors work in the same way.


```r
bool_vect <- c(T,T, F)
sum(bool_vect)
```

```
## [1] 2
```

Vectors are indexed using `[]`.


```r
abc <- c("a", "b", "c")
abc[1]
```

```
## [1] "a"
```

```r
abc[2]
```

```
## [1] "b"
```

```r
abc[c(1,3)]
```

```
## [1] "a" "c"
```

```r
abc[c(1,2)]
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
abc[-c(2,3)]
```

```
## [1] "a"
```


## Lists

Lists are vectors that can hold mixed object types.  Vectors need to be all of the same type.


```r
ls <- list(T, "Character", 3.14)
ls
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
ls <- list(bool = T, character = "character", numeric = 3.14)
ls
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
ls$numeric
```

```
## [1] 3.14
```

```r
ls$numeric + 5
```

```
## [1] 8.14
```

Lists can also be indexed using `[]`.


```r
ls[1]
```

```
## $bool
## [1] TRUE
```

```r
ls[2]
```

```
## $character
## [1] "character"
```


Lists can contain vectors, other lists, and any other object.


```r
everything <- list(vector = c(1,2,3), character = c("a", "b", "c"), list = ls)
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

You only need to understand the very basics of functions for this exam.  Still, understanding functions helps you to understand *everything* in R, since R is a functional [programming language](http://adv-r.had.co.nz/Functional-programming.html), unlike Python, C, VBA, Java which are all object-oriented, or SQL which isn't really a language but a series of set-operations.

Functions do things.  The convention is to name a function as a verb.  The function `make_rainbows()` would create a rainbow.  The function `summarise_vectors` would summarise vectors.  Functions may or may not have an input and output.  

If you need to do something in R, there is a high probability that someone has already written a function to do it.  That being said, creating simple functions is quite useful.

**A function that does not return anything**


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

When returning something, the `return` statement is optional.


```r
add_together <- function(x, y){
  x + y
}

add_together(2,5)
```

```
## [1] 7
```

```r
add_together <- function(x, y){
  return(x + y)
}

add_together(2,5)
```

```
## [1] 7
```

Functions can work with vectors.


```r
x_vector <- c(1,2,3)
y_vector <- c(4,5,6)
add_together(x_vector, y_vector)
```

```
## [1] 5 7 9
```

## Data frames

R is an old programming language.  The original `data.frame` object has been updated with the newer and better `tibble` (like the word "table").  **Tibbles are really lists of vectors, where each column is a vector**.  


```r
library(tibble) #the tibble library has functions for making tibbles
data <- tibble(age = c(25, 35), has_fsa = c(F, T))

data
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
data$age
```

```
## [1] 25 35
```

To find the number of rows and columns, use `dim`.


```r
dim(data)
```

```
## [1] 2 2
```

To fine a summary, use `summary`


```r
summary(data)
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

The pipe operator `%>%` is a way of making code more readable and easier to edit. The way that we are taught to do functional composition is by nesting, which is slow to read and write.

In five seconds, tell me what the below code is doing.


```r
log(sqrt(exp(log2(sqrt((max(c(3, 4, 16))))))))
```

```
## [1] 1
```

Did you get the answer of 1?  If so, you are good at reading parenthesis.  This requires starting from the inner-most nested brackets and moving outwards from right to left.

The math notation would be slightly easier to read, but still painful.

$$log(\sqrt{e^{log_2(\sqrt{max(3,4,16)})}})$$

Here is the same algebra using the pipe.  To read this, replace the `%>%` with the word `THEN`.


```r
library(dplyr) #the pipe is from the dplyr library
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
#max(c(3, 4, 16) THEN   #The max of 3, 4, and 16 is 16
#  sqrt() THEN          #The square root of 16 is 4
#  log2() THEN          #The log in base 2 of 4 is 2
#  exp() THEN           #the exponent of 2 is e^2
#  sqrt() THEN          #the square root of e^2 is e
#  log()                #the natural logarithm of e is 1
```

You may not be convinced by this simple example using numbers; however, once we get to data manipulations in the next section the advantage of piping will become obvious.

To quickly produce pipes, use `CTRL + SHIFT + M`.  By highlighting only certain sections, we can run the code in steps as if we were using a debugger.  This makes testing out code much faster.


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

Those familiar with Python's Pandas will be see that `%>%` is quite similar to ".".
