#!/usr/bin/env python3
"""
Helper script to fix a TidyTuesday project file with proper data generation
based on the project theme.
"""

import re
from pathlib import Path
from typing import Dict, Tuple

# Data generation templates by project theme
DATA_TEMPLATES = {
    "employment": """# Generate employment and health data
set.seed(42)
countries <- c("Kenya", "USA", "Brazil", "India", "South Africa", "Mexico", 
               "Nigeria", "Bangladesh", "Philippines", "Ghana")
years <- 2015:2022

employment_health_data <- expand.grid(
  country = countries,
  year = years,
  stringsAsFactors = FALSE
) %>%
  mutate(
    # Employment rate (% of working age population)
    employment_rate = case_when(
      country %in% c("USA", "Mexico") ~ runif(n(), 55, 65),
      country %in% c("Brazil", "South Africa") ~ runif(n(), 50, 60),
      country %in% c("India", "Bangladesh", "Philippines") ~ runif(n(), 45, 55),
      country %in% c("Kenya", "Nigeria", "Ghana") ~ runif(n(), 40, 50),
      TRUE ~ 50
    ),
    # Health indicators (life expectancy proxy)
    life_expectancy = case_when(
      country == "USA" ~ runif(n(), 76, 79),
      country %in% c("Brazil", "Mexico", "South Africa") ~ runif(n(), 72, 75),
      country %in% c("India", "Bangladesh", "Philippines") ~ runif(n(), 68, 71),
      country %in% c("Kenya", "Nigeria", "Ghana") ~ runif(n(), 60, 65),
      TRUE ~ 70
    ),
    # Unemployment rate
    unemployment_rate = 100 - employment_rate + rnorm(n(), 0, 2),
    # Health expenditure as % of GDP
    health_expenditure_pct = case_when(
      country == "USA" ~ runif(n(), 16, 18),
      country %in% c("Brazil", "South Africa") ~ runif(n(), 8, 10),
      country %in% c("India", "Kenya", "Nigeria") ~ runif(n(), 4, 6),
      TRUE ~ 6
    ),
    # GDP per capita (thousands USD)
    gdp_per_capita = case_when(
      country == "USA" ~ runif(n(), 60, 70),
      country %in% c("Brazil", "Mexico", "South Africa") ~ runif(n(), 8, 12),
      country %in% c("India", "Kenya", "Nigeria", "Ghana") ~ runif(n(), 1.5, 3),
      TRUE ~ 5
    )
  ) %>%
  filter(unemployment_rate > 0, unemployment_rate < 100)""",
    
    "food-security": """# Generate food security data
set.seed(42)
countries <- c("Kenya", "Ethiopia", "India", "Bangladesh", "Nigeria", 
               "Somalia", "Sudan", "Yemen", "Afghanistan", "Haiti",
               "USA", "Brazil", "China", "Mexico", "South Africa")
years <- 2015:2022

food_security_data <- expand.grid(
  country = countries,
  year = years,
  stringsAsFactors = FALSE
) %>%
  mutate(
    # Food Security Index (0-100, higher = more secure)
    food_security_index = case_when(
      country == "USA" ~ runif(n(), 85, 90),
      country %in% c("Brazil", "China", "Mexico", "South Africa") ~ runif(n(), 65, 75),
      country %in% c("India", "Bangladesh") ~ runif(n(), 55, 65),
      country %in% c("Kenya", "Ethiopia", "Nigeria") ~ runif(n(), 40, 50),
      country %in% c("Somalia", "Sudan", "Yemen", "Afghanistan", "Haiti") ~ runif(n(), 25, 35),
      TRUE ~ 50
    ),
    # Undernourishment rate (%)
    undernourishment_rate = 100 - food_security_index + rnorm(n(), 0, 5),
    undernourishment_rate = pmax(0, pmin(100, undernourishment_rate)),
    # Crop production index (2014-2016 = 100)
    crop_production_index = case_when(
      country %in% c("USA", "China", "Brazil") ~ runif(n(), 105, 115),
      country %in% c("India", "Mexico") ~ runif(n(), 100, 110),
      country %in% c("Kenya", "Ethiopia", "Nigeria") ~ runif(n(), 90, 100),
      TRUE ~ 95
    ),
    # Food price volatility
    food_price_volatility = case_when(
      country %in% c("Somalia", "Yemen", "Afghanistan") ~ runif(n(), 25, 35),
      country %in% c("Ethiopia", "Sudan", "Haiti") ~ runif(n(), 15, 25),
      country %in% c("Kenya", "Nigeria", "Bangladesh") ~ runif(n(), 10, 20),
      TRUE ~ runif(n(), 5, 15)
    )
  ) %>%
  arrange(country, year)"""
}

def get_theme_from_filename(filename: str) -> str:
    """Determine theme from filename"""
    filename_lower = filename.lower()
    if "employment" in filename_lower or "health" in filename_lower:
        return "employment"
    elif "food" in filename_lower or "agriculture" in filename_lower or "crop" in filename_lower:
        return "food-security"
    elif "income" in filename_lower or "poverty" in filename_lower or "inequality" in filename_lower:
        return "income"
    elif "climate" in filename_lower or "co2" in filename_lower or "carbon" in filename_lower:
        return "climate"
    elif "health" in filename_lower or "mortality" in filename_lower or "disease" in filename_lower:
        return "health"
    elif "education" in filename_lower:
        return "education"
    elif "gender" in filename_lower:
        return "gender"
    else:
        return "general"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python fix_project_with_data.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    theme = get_theme_from_filename(filename)
    print(f"Theme detected: {theme}")

