library(shiny)

shinyUI(fluidPage(
  
  titlePanel("Stock Anomaly Detection"),
  
  sidebarLayout(
    sidebarPanel(
      textInput("ticker", 
                "Stock Ticker Symbol:", 
                value = "AXP"),
      
      dateRangeInput("dateRange",
                     "Date Range:",
                     start = "2020-01-01",
                     end = "2024-12-01",
                     format = "yyyy-mm-dd"),
      
      sliderInput("alpha",
                  "Anomaly Sensitivity (alpha):",
                  min = 0.01,
                  max = 0.5,
                  value = 0.05,
                  step = 0.01),
      
      hr(),
      
      helpText("This app detects anomalies in stock prices using ARIMA modeling."),
      helpText("Higher alpha values = fewer anomalies detected.")
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Anomaly Plot", 
                 plotOutput("distPlot", height = "500px"),
                 hr(),
                 plotOutput("dividendHistoryPlot", height = "400px"),
                 hr(),
                 plotOutput("yieldSummaryPlot", height = "400px")),
        
        tabPanel("Details",
                 uiOutput("selectUI"),
                 plotOutput("quantPlot", height = "500px"))
      )
    )
  )
))