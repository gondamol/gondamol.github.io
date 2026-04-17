library(readr)
library(dplyr)
library(xgboost)

# Train a portfolio-scale demonstration model on a synthetic readmission dataset.
data_path <- file.path("data", "sample_readmissions.csv")
readmissions <- read_csv(data_path, show_col_types = FALSE)

model_data <- readmissions %>%
  mutate(
    sex_male = if_else(sex == "M", 1, 0),
    follow_up_scheduled = if_else(follow_up_scheduled == "yes", 1, 0),
    transport_barrier_flag = if_else(transport_barrier_flag == "yes", 1, 0)
  ) %>%
  select(
    age,
    sex_male,
    prior_admissions_6m,
    length_of_stay_days,
    medication_gap_days,
    comorbidity_score,
    follow_up_scheduled,
    transport_barrier_flag,
    readmitted_30d
  )

features <- as.matrix(select(model_data, -readmitted_30d))
labels <- model_data$readmitted_30d

dtrain <- xgb.DMatrix(data = features, label = labels)

params <- list(
  objective = "binary:logistic",
  eval_metric = "auc",
  eta = 0.1,
  max_depth = 4,
  subsample = 0.9,
  colsample_bytree = 0.9
)

model <- xgb.train(
  params = params,
  data = dtrain,
  nrounds = 50,
  verbose = 0
)

xgb.save(model, "readmission_model.xgb")
write_rds(colnames(features), "feature_names.rds")
