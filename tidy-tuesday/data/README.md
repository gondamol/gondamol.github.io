# TidyTuesday Data Directory

This directory stores datasets for TidyTuesday analyses.

## 📁 Structure

```
data/
├── 2024-01-02/          # Date-based folders
│   ├── dataset1.csv
│   └── README.md
├── 2024-01-09/
│   └── dataset2.csv
└── README.md            # This file
```

## 📥 How to Get Data

### Method 1: Using tidytuesdayR Package (Recommended)

```r
# Install once
install.packages("tidytuesdayR")

# Load data for a specific week
library(tidytuesdayR)
tuesdata <- tt_load('2024-01-02')

# Access datasets
df <- tuesdata$dataset_name

# Save locally (optional)
write_csv(df, "data/2024-01-02/dataset_name.csv")
```

### Method 2: Direct Download

```r
# Read directly from GitHub
df <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-01-02/dataset.csv')

# Save locally
write_csv(df, "data/2024-01-02/dataset.csv")
```

### Method 3: Manual Download

1. Go to [TidyTuesday GitHub](https://github.com/rfordatascience/tidytuesday)
2. Navigate to `data/YYYY/YYYY-MM-DD/`
3. Download CSV files
4. Save to `tidy-tuesday/data/YYYY-MM-DD/`

## 🚫 Git Ignore

Large data files are ignored by git (see `.gitignore`). Only small datasets (<1MB) are committed.

## 📊 Data Sources

All data comes from the [TidyTuesday GitHub repository](https://github.com/rfordatascience/tidytuesday).

Each week's data includes:
- CSV files
- Data dictionary
- Source information
- Suggested questions

## 🔄 Workflow

1. **Tuesday**: New dataset posted
2. **Download**: Use tidytuesdayR or direct download
3. **Analyze**: Create analysis in `tidy-tuesday/YYYY-MM-DD-topic.qmd`
4. **Publish**: Add to `index.qmd` and render

## 💡 Tips

- **Cache data locally** for reproducibility
- **Document data sources** in your analysis
- **Check data dictionary** before starting
- **Join the community** on Twitter with #TidyTuesday
