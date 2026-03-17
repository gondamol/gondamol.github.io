library(readr)
library(dplyr)

facility_kpis <- read_csv(file.path("data", "facility_kpis.csv"), show_col_types = FALSE) %>%
  mutate(
    alert_flag = reimbursement_lag_days > 45 | stockout_risk_pct > 0.6
  )

write_csv(facility_kpis, "facility_kpis_enriched.csv")
