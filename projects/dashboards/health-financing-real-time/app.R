library(shiny)
library(readr)

ui <- fluidPage(
  titlePanel("Health Financing Dashboard Demo"),
  tableOutput("facility_table")
)

server <- function(input, output, session) {
  output$facility_table <- renderTable({
    read_csv(file.path("data", "facility_kpis.csv"), show_col_types = FALSE)
  })
}

shinyApp(ui, server)
