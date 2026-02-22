# Test script to verify tidytuesdayR works and explore datasets

library(tidytuesdayR)
library(tidyverse)

cat("Testing tidytuesdayR package...\n\n")

# Test 1: Mental Health dataset (2016-08-16)
cat("1. Loading Mental Health in Tech dataset (2016-08-16)...\n")
tryCatch({
  tuesdata_mh <- tt_load('2016-08-16')
  cat("   ✓ Success! Available datasets:", paste(names(tuesdata_mh), collapse = ", "), "\n")
  cat("   Rows:", nrow(tuesdata_mh[[1]]), "\n")
  cat("   Columns:", paste(names(tuesdata_mh[[1]])[1:5], collapse = ", "), "...\n\n")
}, error = function(e) {
  cat("   ✗ Error:", e$message, "\n\n")
})

# Test 2: Global Mortality (2018-04-16)
cat("2. Loading Global Mortality dataset (2018-04-16)...\n")
tryCatch({
  tuesdata_mort <- tt_load('2018-04-16')
  cat("   ✓ Success! Available datasets:", paste(names(tuesdata_mort), collapse = ", "), "\n")
  cat("   Rows:", nrow(tuesdata_mort[[1]]), "\n\n")
}, error = function(e) {
  cat("   ✗ Error:", e$message, "\n\n")
})

# Test 3: Carbon Emissions (2024-05-21)
cat("3. Loading Carbon Emissions dataset (2024-05-21)...\n")
tryCatch({
  tuesdata_co2 <- tt_load('2024-05-21')
  cat("   ✓ Success! Available datasets:", paste(names(tuesdata_co2), collapse = ", "), "\n")
  cat("   Rows:", nrow(tuesdata_co2[[1]]), "\n\n")
}, error = function(e) {
  cat("   ✗ Error:", e$message, "\n\n")
})

cat("Testing complete!\n")
