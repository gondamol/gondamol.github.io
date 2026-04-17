library(readr)
library(dplyr)
library(xgboost)

# Score one or more discharge records using the saved readmission model.
score_readmissions <- function(new_data) {
  model <- xgb.load("readmission_model.xgb")
  feature_names <- read_rds("feature_names.rds")

  scoring_frame <- new_data %>%
    mutate(
      sex_male = if_else(sex == "M", 1, 0),
      follow_up_scheduled = if_else(follow_up_scheduled == "yes", 1, 0),
      transport_barrier_flag = if_else(transport_barrier_flag == "yes", 1, 0)
    ) %>%
    select(all_of(feature_names))

  predictions <- predict(model, as.matrix(scoring_frame))
  bind_cols(new_data, tibble(risk_score = round(predictions, 3)))
}
