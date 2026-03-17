library(shiny)
library(readr)
library(dplyr)

source("predict.R")

ui <- fluidPage(
  titlePanel("Readmission Risk Triage Demo"),
  sidebarLayout(
    sidebarPanel(
      helpText("Synthetic demonstration interface for portfolio review."),
      actionButton("refresh_demo", "Reload sample records")
    ),
    mainPanel(
      tableOutput("risk_table")
    )
  )
)

server <- function(input, output, session) {
  scored <- reactive({
    input$refresh_demo
    sample_data <- read_csv(file.path("data", "sample_readmissions.csv"), show_col_types = FALSE)
    score_readmissions(sample_data) %>%
      arrange(desc(risk_score)) %>%
      select(patient_id, county, age, prior_admissions_6m, medication_gap_days, risk_score)
  })

  output$risk_table <- renderTable(scored())
}

shinyApp(ui, server)
