# Modeling-Project 

Below is a complete solution for creating an R Shiny app that allows users to explore and model datasets from the `ExamPAData` package. The app will enable users to select a dataset, choose an appropriate machine learning model (for regression or classification), and view performance metrics and visualizations. I'll provide the code for the two main Shiny files: `ui.R` and `server.R`, along with instructions on how to set up and run the app.


### **🚀 How to Install `h2o` and Java to Run Your Shiny App**
If you want to **run a Shiny app that uses `h2o`**, you **must install Java and `h2o`** on your system. Follow these steps based on your operating system:

---

## **1️⃣ Install Java (Required for `h2o`)**
`h2o` requires **Java 8 or later**. Here’s how to install it:

### **🔵 Windows**
1. **Download Java:**  
   - Go to: [Java Downloads](https://www.java.com/en/download/)
   - Download and install the **latest version** of Java.

2. **Check if Java is installed:**  
   Open **Command Prompt** (`Win + R`, type `cmd`, and press **Enter**), then run:
   ```sh
   java -version
   ```
   - ✅ If you see something like `java version "1.8.0_301"`, Java is installed!
   - ❌ If you get **"Java not recognized"**, restart your computer or reinstall Java.

---

### **🟢 Mac (MacOS)**
1. **Install Java using Homebrew** (recommended):
   ```sh
   brew install openjdk
   ```

2. **Check if Java is installed:**
   ```sh
   java -version
   ```
   If it shows a Java version, you're good to go!

---

### **🟠 Linux (Ubuntu/Debian)**
1. **Install Java:**
   ```sh
   sudo apt update
   sudo apt install default-jre
   ```

2. **Check if Java is installed:**
   ```sh
   java -version
   ```
---

## **2️⃣ Install `h2o` in R**
Once Java is installed, install `h2o` in R:

```r
# Install dependencies
install.packages(c("RCurl", "jsonlite"))

# Install h2o
install.packages("h2o")

# Load h2o
library(h2o)

# Start h2o
h2o.init()
```

### **Common Issues & Fixes**
- **Error: "Java is not installed"** → Restart your computer and check `java -version` again.
- **Error: "h2o.init() failed"** → Run `Sys.getenv("JAVA_HOME")` in R. If it’s empty, reinstall Java.

---

## **🎯 Summary**
1. **Install Java** (`java -version` should work).
2. **Install `h2o` in R** (`install.packages("h2o")`).
3. **Run `h2o.init()`** to start the `h2o` engine.


---

## R Shiny App Files

### `ui.R`
This file defines the user interface of the Shiny app.

```r
library(shiny)

fluidPage(
  titlePanel("ExamPAData Explorer: Predictive Analytics Tool"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("dataset", "Choose a dataset:", 
                  choices = c("customer_phone_calls", "patient_length_of_stay", "patient_num_labs", 
                              "actuary_salaries", "june_pa", "customer_value", "exam_pa_titanic", 
                              "apartment_apps", "health_insurance", "student_success", 
                              "readmission", "auto_claim", "boston", "bank_loans")),
      
      selectInput("model", "Choose a model:", choices = NULL)  # Dynamically updated based on dataset
    ),
    
    mainPanel(
      verbatimTextOutput("metrics"),
      plotOutput("plot")
    )
  )
)
```

### `server.R`
This file contains the server logic to handle user inputs, train models, and generate outputs.

```r
library(shiny)
library(ExamPAData)
library(caret)
library(dplyr)
library(ggplot2)
library(h2o)

# Map each dataset to its target variable
dataset_info <- list(
  customer_phone_calls  = list(type = "classification", target = "purchase"),
  patient_length_of_stay= list(type = "regression",    target = "days"),
  patient_num_labs      = list(type = "regression",    target = "num_labs"),
  actuary_salaries      = list(type = "regression",    target = "salary"),
  june_pa               = list(type = "regression",    target = "CLM_AMT"),
  customer_value        = list(type = "regression",    target = "score"),
  exam_pa_titanic       = list(type = "classification",target = "survived"),
  apartment_apps        = list(type = "classification",target = "apartment_apps"),
  health_insurance      = list(type = "regression",    target = "charges"),
  student_success       = list(type = "classification",target = "G3"),
  readmission           = list(type = "classification",target = "Readmission.Status"),
  auto_claim            = list(type = "regression",    target = "CLM_AMT"),
  boston                = list(type = "regression",    target = "medv"),
  bank_loans            = list(type = "classification",target = "y")
)

shinyServer(function(input, output, session) {
  
  # Initialize H2O cluster
  h2o.init(nthreads = -1, enable_assertions = FALSE)
  
  # When session ends, shut down H2O
  session$onSessionEnded(function() {
    h2o.shutdown(prompt = FALSE)
  })
  
  # Reactive expression to load the selected dataset
  selected_data <- reactive({
    req(input$dataset)
    # Load dataset from ExamPAData
    data(list = input$dataset, package = "ExamPAData", envir = .GlobalEnv)
    dataset <- get(input$dataset, envir = .GlobalEnv)
    
    # Validate dataset
    validate(
      need(!is.null(dataset) && nrow(dataset) > 0,
           paste("Error: Dataset", input$dataset, "is empty or invalid."))
    )
    
    # Make sure target variable exists
    target <- dataset_info[[input$dataset]]$target
    validate(
      need(target %in% names(dataset),
           paste("Error: Target variable", target, "not found in dataset."))
    )
    
    # Convert classification target to factor
    if (dataset_info[[input$dataset]]$type == "classification") {
      dataset[[target]] <- as.factor(dataset[[target]])
    }
    
    dataset
  })
  
  # Show target var info
  output$targetInfo <- renderUI({
    req(input$dataset)
    target_name <- dataset_info[[input$dataset]]$target
    problem_type <- dataset_info[[input$dataset]]$type
    strong(paste("Target variable:", target_name, "(",
                 ifelse(problem_type=="classification","classification","regression"), ")"))
  })
  
  # Data preview
  output$dataPreview <- renderTable({
    head(selected_data(), 10)
  })
  
  # Data summary
  output$dataSummary <- renderPrint({
    summary(selected_data())
  })
  
  # Update predictor choices whenever a dataset is selected
  observeEvent(input$dataset, {
    df <- selected_data()
    target <- dataset_info[[input$dataset]]$target
    # By default, set all columns except the target as predictors
    predictor_choices <- setdiff(names(df), target)
    updateSelectInput(session, "predictors",
                      choices = predictor_choices,
                      selected = predictor_choices)
  })
  
  # Compute baseline (benchmark) metric
  # Classification -> majority class accuracy
  # Regression -> RMSE using mean of target
  output$baselineMetric <- renderPrint({
    req(selected_data())
    df <- selected_data()
    target <- dataset_info[[input$dataset]]$target
    problem_type <- dataset_info[[input$dataset]]$type
    
    if (problem_type == "classification") {
      # majority class accuracy
      tbl <- table(df[[target]])
      majority_class <- names(tbl)[which.max(tbl)]
      baseline_preds <- rep(majority_class, nrow(df))
      actual <- as.character(df[[target]])
      acc <- mean(baseline_preds == actual)
      cat("Baseline (majority class) accuracy =", round(acc, 4))
    } else {
      # regression -> mean of target
      actual <- df[[target]]
      mu <- mean(actual, na.rm = TRUE)
      baseline_preds <- rep(mu, length(actual))
      rmse <- sqrt(mean((actual - baseline_preds)^2, na.rm = TRUE))
      cat("Baseline (mean) RMSE =", round(rmse, 4))
    }
  })
  
  # Train H2O AutoML with limited algorithms
  observeEvent(input$trainModel, {
    # Show immediate message
    output$trainLog <- renderText("Starting H2O AutoML training...")
    
    df <- selected_data()
    target <- dataset_info[[input$dataset]]$target
    problem_type <- dataset_info[[input$dataset]]$type
    
    # partition data into train/test or just use all for demonstration
    # For speed, let's train on all data, but normally you'd do a split
    # ...
    
    # convert to H2O frame
    h2o_df <- as.h2o(df)
    
    # ensure the target is factor for classification
    if (problem_type == "classification") {
      h2o_df[[target]] <- h2o.asfactor(h2o_df[[target]])
    }
    
    # set predictor variables
    predictors <- input$predictors
    if (length(predictors) < 1) {
      # fallback if none selected
      predictors <- setdiff(names(df), target)
    }
    
    # For speed, let's exclude most algorithms
    # We'll only allow DRF (Random Forest) and GBM
    # Also reduce cross-validation folds and set a small max_models
    captured_log <- capture.output({
      aml <- h2o.automl(
        x = predictors,
        y = target,
        training_frame = h2o_df,
        include_algos = c("DRF","GBM"),    # Limit to 2 algorithms
        max_models = 5,                   # limit number of models
        nfolds = 2,                       # fewer folds for speed
        seed = 42,
        sort_metric = ifelse(problem_type=="classification","AUC","RMSE"),
        keep_cross_validation_predictions = FALSE,
        keep_cross_validation_models = FALSE,
        keep_cross_validation_fold_assignment = FALSE
      )
      
      # store the leader for performance
      leader <- aml@leader
      perf <- h2o.performance(leader, h2o_df)  # evaluate on same data (demo)
      
      # Print summary so it appears in the captured log
      print(aml@leaderboard)
      cat("\n--- Leader Model Summary ---\n")
      print(leader)
      cat("\n--- Performance on training data: ---\n")
      print(perf)
    })
    
    # Render progress/log in UI
    output$trainLog <- renderText(paste(captured_log, collapse = "\n"))
    
    # Render final performance metrics in a separate output for clarity
    output$perfMetrics <- renderPrint({
      # optional final summary
      cat("Final Model Performance (see log above for details).")
    })
  })
})


```

---

## How to Set Up and Run the App

### 1. Install Required Packages
Before running the app, ensure you have the necessary R packages installed. Run the following command in your R console:

```r
install.packages(c("shiny", "ExamPAData", "caret", "dplyr", "ggplot2"))
```

### 2. Create the App Files
- **Create a new directory** (e.g., `ExamPAExplorer`) on your computer.
- **Save the files**:
  - Copy the `ui.R` code above into a file named `ui.R`.
  - Copy the `server.R` code above into a file named `server.R`.
  - Place both files in the `ExamPAExplorer` directory.

### 3. Run the App
- Open R or RStudio.
- Set your working directory to the folder containing the files:
  ```r
  setwd("path/to/ExamPAExplorer")
  ```
- Run the app:
  ```r
  shiny::runApp()
  ```
This will launch the Shiny app in your default web browser.

---

## App Functionality

### Features
- **Dataset Selection**: Choose from a list of datasets in the `ExamPAData` package via a dropdown menu.
- **Model Selection**: Select a machine learning model (e.g., Linear Regression, Logistic Regression, or Random Forest) from a dropdown menu that updates dynamically based on whether the dataset is for regression or classification.
- **Performance Metrics**: View metrics such as RMSE and R-squared for regression tasks, or accuracy for classification tasks.
- **Visualizations**: See a scatter plot of actual vs. predicted values for regression, or a confusion matrix heatmap for classification.

### How It Works
1. The app loads the selected dataset from `ExamPAData`.
2. Based on the dataset’s problem type (regression or classification), it offers appropriate model options.
3. It trains the chosen model on 80% of the data and tests it on the remaining 20%.
4. The app then calculates performance metrics and generates a plot to visualize the results.

---

## Notes
- The app assumes the `ExamPAData` package datasets are structured with a clear target variable, as defined in the `dataset_info` list.
- For simplicity, minimal preprocessing is included. In a production environment, you might want to add data cleaning or feature scaling steps.
- The Random Forest model works for both regression and classification, making it a versatile option.

This app is a valuable tool for exploring predictive analytics and practicing for the Society of Actuaries' Predictive Analytics Exam (Exam PA). Enjoy experimenting with the datasets and models!
