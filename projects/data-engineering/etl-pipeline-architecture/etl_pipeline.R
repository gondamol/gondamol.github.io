library(readr)
library(dplyr)
library(stringr)

# Demonstration ETL flow for a multi-country study extract.
raw_extract <- read_csv(file.path("data", "raw_household_extract.csv"), show_col_types = FALSE)
facility_reference <- read_csv(file.path("data", "facility_reference.csv"), show_col_types = FALSE)

staging <- raw_extract %>%
  mutate(
    facility_id = str_to_upper(facility_id),
    visit_date = as.Date(visit_date),
    monthly_income_kes = as.numeric(monthly_income_kes),
    monthly_health_spend_kes = as.numeric(monthly_health_spend_kes)
  )

validation_summary <- staging %>%
  mutate(
    invalid_income = monthly_income_kes < 0,
    invalid_spend = monthly_health_spend_kes < 0,
    missing_facility = !facility_id %in% facility_reference$facility_id
  )

reporting_model <- validation_summary %>%
  left_join(facility_reference, by = "facility_id") %>%
  mutate(financial_burden_ratio = monthly_health_spend_kes / pmax(monthly_income_kes, 1))

write_csv(reporting_model, "reporting_model.csv")
write_csv(validation_summary, "validation_summary.csv")
