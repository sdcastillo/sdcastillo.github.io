library(shiny)
library(zoo)
library(quantmod)
library(forecast)
library(lubridate)
library(ggplot2)
library(dplyr)
library(readr)
library(reticulate)
Sys.setenv(RETICULATE_UV_ENABLED = "0")
# 2. Tell reticulate the full path to your real Python 3.13.2
# 1. Disable the broken uv temp stuff
# 2. Tell reticulate the full path to your real Python 3.13.2
reticulate::use_python("C:/Users/casti/AppData/Local/Programs/Python/Python313/python.exe", required = TRUE)

# 2. Install the Python packages the first time (only once)
#    Uncomment the two lines below if you haven't installed them yet
# py_install("yfinance", pip = TRUE)
# py_install("pandas", pip = TRUE)

library(reticulate)
# py_install("yfinance", pip = TRUE)   # uncomment only once
# py_install("pandas", pip = TRUE)

# Execute safely
#py_run_string(python_code)

# Bring into R
buffett_dividends_10y <- read_csv("buffett_dividends_10y.csv")
buffett_yield_summary <- read_csv("buffett_yield_summary.csv") |> rename(divident_yield_percentage =`Dividend_Yield_%`)

names(buffett_yield_summary)

# Clean dates
library(dplyr)
library(lubridate)
buffett_dividends_10y <- buffett_dividends_10y %>%
  mutate(Ex_Dividend_Date = as.Date(Ex_Dividend_Date)) %>%
  arrange(Ticker, Ex_Dividend_Date)

buffett_yield_summary <- buffett_yield_summary %>% arrange(desc(Dividend_Yield_%))

# Preview
print(head(buffett_yield_summary, 15))

# 4. Execute the Python code
py_run_string(python_code)

# 5. Bring the two pandas dataframes into R as proper R data frames
buffett_dividends_10y   <- py$dividends_10y   %>% as.data.frame()
buffett_yield_summary   <- py$yield_summary   %>% as.data.frame()

buffett_dividends_10y <- buffett_dividends_10y %>%
  mutate(Ex_Dividend_Date = as.Date(Ex_Dividend_Date))

buffett_yield_summary |> head()

# Function to fit ARIMA model, detect largest residuals, and create plot
detect_anom = function(cur_symb = "META", 
                       alpha = 0.05, 
                       start.date = "2014-01-01",
                       end.date = "2025-02-01"){  
  
  tryCatch({
    # Download stock data
    getSymbols(cur_symb, from = start.date, to = end.date, auto.assign = TRUE, env = .GlobalEnv)
    cur_data = get(cur_symb, envir = .GlobalEnv)[, 6]
    
    # Create date sequence matching actual data length
    dates = index(cur_data)
    
    # Fit model to the log of the adjusted closing price
    model = auto.arima(log(as.numeric(cur_data)))
    estimate = fitted(model)
    
    # Outliers are classified by those above the sensitivity level
    anom_index = which(residuals(model) > alpha) 
    
    if(length(anom_index) > 0){
      anom_dates = dates[anom_index]
      
      mydata = data.frame(date = dates, value = as.numeric(cur_data))
      points = data.frame(date = anom_dates, value = as.numeric(cur_data)[anom_index])
      
      point.size = pmax(residuals(model)[anom_index] * 100, 2)
      
      # Create plot
      ggplot_1 = 
        ggplot(mydata, aes(date, value)) +
        geom_line(col = "chartreuse4") + 
        geom_point(data = points, aes(date, value), size = point.size, col = "red", alpha = 0.5) + 
        geom_text(data = points, aes(date, value), hjust = 0, vjust = -0.5, 
                  label = format(points$date, "%Y-%m-%d"), size = 3) + 
        ggtitle(paste(cur_symb, "adjusted closing price")) +
        xlab("Date") + 
        ylab("Adjusted Close (USD)") + 
        theme_linedraw() + 
        theme(axis.text = element_text(size = 12),
              axis.title = element_text(size = 14, face = "bold"))
    } else {
      mydata = data.frame(date = dates, value = as.numeric(cur_data))
      ggplot_1 = 
        ggplot(mydata, aes(date, value)) +
        geom_line(col = "chartreuse4") + 
        ggtitle(paste(cur_symb, "adjusted closing price - No anomalies detected")) +
        xlab("Date") + 
        ylab("Adjusted Close (USD)") + 
        theme_linedraw()
      
      anom_dates = character(0)
    }
    
    output = list(date = anom_dates, plot = ggplot_1, model = model)  
    return(output)
    
  }, error = function(e){
    return(list(date = character(0), 
                plot = ggplot() + ggtitle(paste("Error:", e$message)),
                model = NULL))
  })
}

# Creates stock info for "details" page
stockinfo = function(ticker, date){
  tryCatch({
    start.date = ymd(date) - months(1)
    end.date = ymd(date) + months(1)
    
    getSymbols(ticker, from = start.date, to = end.date, auto.assign = TRUE, env = .GlobalEnv)
    chartSeries(get(ticker, envir = .GlobalEnv), 
                name = ticker, 
                theme = "white")
  }, error = function(e){
    plot.new()
    text(0.5, 0.5, paste("Error loading chart:", e$message))
  })
}
# Define server logic
shinyServer(function(input, output, session) {
  
  # Reactive data input
  dataInput <- reactive({
    req(input$ticker, input$dateRange)
    detect_anom(cur_symb = input$ticker,
                alpha = input$alpha,
                start.date = input$dateRange[1],
                end.date = input$dateRange[2])
  })
  
  output$distPlot <- renderPlot({
    dataInput()$plot
  })
  
  # Reactive input selection for anomaly dates
  output$selectUI <- renderUI({
    dates = dataInput()$date
    if(length(dates) > 0){
      selectInput("anomDates", "Select date", as.character(dates))
    } else {
      selectInput("anomDates", "Select date", choices = "No anomalies detected")
    }
  })
  
  output$quantPlot <- renderPlot({
    req(input$anomDates)
    if(input$anomDates != "No anomalies detected"){
      stockinfo(ticker = input$ticker, date = input$anomDates)
    } else {
      plot.new()
      text(0.5, 0.5, "No anomalies to display")
    }
  })
  
  # Chart for dividend history over time
  output$dividendHistoryPlot <- renderPlot({
    req(input$ticker)
    
    # Filter dividends for the selected ticker
    ticker_dividends <- buffett_dividends_10y |>
      filter(Ticker == input$ticker)
    
    if(nrow(ticker_dividends) > 0) {
      ggplot(ticker_dividends, aes(x = Ex_Dividend_Date, y = Amount)) +
        geom_line(col = "steelblue", linewidth = 1) +
        geom_point(col = "steelblue", size = 2) +
        ggtitle(paste(input$ticker, "- Dividend History (2015-Present)")) +
        xlab("Ex-Dividend Date") +
        ylab("Dividend Amount (USD)") +
        theme_linedraw() +
        theme(axis.text = element_text(size = 12),
              axis.title = element_text(size = 14, face = "bold"),
              plot.title = element_text(size = 16, face = "bold"))
    } else {
      ggplot() + 
        ggtitle(paste("No dividend data available for", input$ticker)) +
        theme_linedraw()
    }
  })  # <- Added closing brace here

  # Chart for dividend yield summary comparison
  output$yieldSummaryPlot <- renderPlot({
    ggplot(buffett_yield_summary, aes(x = reorder(Ticker, divident_yield_percentage ), y = divident_yield_percentage )) +
      geom_col(aes(fill = Ticker), show.legend = FALSE) +
      geom_text(aes(label = paste0(divident_yield_percentage , "%")), 
                hjust = -0.1, size = 4) +
      coord_flip() +
      scale_fill_brewer(palette = "Set3") +
      ggtitle("Dividend Yield Comparison (TTM)") +
      xlab("Ticker") +
      ylab("Dividend Yield (%)") +
      ylim(0, max(buffett_yield_summary$divident_yield_percentage ) * 1.15) +
      theme_linedraw() +
      theme(axis.text = element_text(size = 12),
            axis.title = element_text(size = 14, face = "bold"),
            plot.title = element_text(size = 16, face = "bold"))
  })  # <- Added closing brace here
  
})  # <- This closes shinyServer