library(readr)
library(dplyr)

scenario_data <- read_csv(file.path("data", "ncd_financing_scenarios.csv"), show_col_types = FALSE)

scenario_results <- scenario_data %>%
  mutate(
    projected_stockout_reduction = baseline_stockout_days - improved_stockout_days,
    projected_service_gain_pct = round(projected_stockout_reduction / baseline_stockout_days * 100, 1)
  )

write_csv(scenario_results, "scenario_results.csv")
