#!/usr/bin/env Rscript
# Generate multiple visualization project files
# This script creates Quarto documents for various visualization projects

library(here)
library(stringr)

# Create visualizations directory structure
viz_dir <- here("visualizations")
dir.create(viz_dir, showWarnings = FALSE, recursive = TRUE)

# Define visualization projects by category
viz_projects <- list(
  # R ggplot2 projects
  list(
    name = "advanced-ggplot2-patterns",
    title = "Advanced ggplot2 Patterns & Techniques",
    category = "r-ggplot2",
    description = "Exploring advanced ggplot2 techniques including faceting, custom themes, and statistical transformations.",
    packages = c("ggplot2", "dplyr", "patchwork", "viridis")
  ),
  list(
    name = "interactive-plotly-charts",
    title = "Interactive Charts with Plotly",
    category = "r-plotly",
    description = "Creating interactive dashboards and charts using plotly for web-based data exploration.",
    packages = c("plotly", "ggplot2", "dplyr")
  ),
  list(
    name = "leaflet-interactive-maps",
    title = "Interactive Maps with Leaflet",
    category = "r-leaflet",
    description = "Building interactive maps showing spatial data with custom markers, popups, and layers.",
    packages = c("leaflet", "sf", "dplyr")
  ),
  list(
    name = "gganimate-time-series",
    title = "Animated Time Series with gganimate",
    category = "r-gganimate",
    description = "Creating animated visualizations to show data evolution over time.",
    packages = c("gganimate", "ggplot2", "dplyr", "gifski")
  ),
  list(
    name = "network-analysis-visualization",
    title = "Network Analysis & Visualization",
    category = "r-network",
    description = "Visualizing networks and relationships using igraph and ggraph packages.",
    packages = c("igraph", "ggraph", "tidygraph")
  ),
  
  # Python visualization projects
  list(
    name = "matplotlib-advanced-plots",
    title = "Advanced Matplotlib Visualizations",
    category = "python-matplotlib",
    description = "Creating publication-quality plots with Matplotlib including subplots and custom styling.",
    packages = c("matplotlib", "numpy", "pandas")
  ),
  list(
    name = "seaborn-statistical-viz",
    title = "Statistical Visualizations with Seaborn",
    category = "python-seaborn",
    description = "Using Seaborn for statistical plotting including regression analysis and distribution plots.",
    packages = c("seaborn", "matplotlib", "pandas", "numpy")
  ),
  list(
    name = "plotly-python-dashboards",
    title = "Interactive Dashboards with Plotly Python",
    category = "python-plotly",
    description = "Building interactive web dashboards using Plotly and Dash for Python.",
    packages = c("plotly", "dash", "pandas")
  ),
  list(
    name = "bokeh-interactive-viz",
    title = "Interactive Visualizations with Bokeh",
    category = "python-bokeh",
    description = "Creating interactive visualizations for modern web browsers using Bokeh.",
    packages = c("bokeh", "pandas", "numpy")
  ),
  
  # D3.js projects
  list(
    name = "d3-bar-charts",
    title = "D3.js Bar Charts & Histograms",
    category = "d3-basic",
    description = "Building interactive bar charts and histograms with D3.js for web visualization.",
    packages = c("D3.js", "HTML", "CSS", "JavaScript")
  ),
  list(
    name = "d3-network-graphs",
    title = "D3.js Network & Force-Directed Graphs",
    category = "d3-advanced",
    description = "Creating interactive network visualizations and force-directed graphs with D3.js.",
    packages = c("D3.js", "JavaScript")
  ),
  list(
    name = "d3-map-visualizations",
    title = "D3.js Geographic Visualizations",
    category = "d3-maps",
    description = "Mapping and geographic data visualization using D3.js and GeoJSON.",
    packages = c("D3.js", "TopoJSON", "GeoJSON")
  ),
  
  # Combined R/Python projects
  list(
    name = "multi-language-dashboard",
    title = "Multi-Language Data Dashboard",
    category = "multi-language",
    description = "Creating dashboards that combine R Shiny and Python Dash components.",
    packages = c("R Shiny", "Python Dash", "reticulate")
  )
)

# Function to create a visualization project file
create_viz_project <- function(project) {
  content <- paste0('---
title: "', project$title, '"
subtitle: "', project$description, '"
format:
  html:
    toc: true
    code-fold: show
    code-tools: true
---

::: {.hero-banner}
# **', project$title, '**

', project$description, '
:::

## Overview

This project demonstrates advanced visualization techniques using **', 
paste(project$packages, collapse = ", "), '**.

## Visualizations

### Example Visualization 1

```{r}
#| echo: true
#| eval: false
#| warning: false
#| message: false

library(ggplot2)
library(dplyr)

# Create sample data
data <- data.frame(
  x = 1:100,
  y = cumsum(rnorm(100))
)

# Create visualization
ggplot(data, aes(x = x, y = y)) +
  geom_line(color = "#667eea", size = 1.2) +
  theme_minimal() +
  labs(
    title = "Sample Time Series Visualization",
    x = "Time",
    y = "Value"
  )
```

### Example Visualization 2

```{r}
#| echo: true
#| eval: false

# Additional visualization code here
```

## Key Techniques

- **Technique 1**: Description of visualization technique
- **Technique 2**: Description of advanced feature
- **Technique 3**: Description of customization option

## Code Repository

All code for this project is available on [GitHub](https://github.com/gondamol/portfolio).

## Related Projects

- [View All Visualizations](/visualizations/index.html)
- [Explore TidyTuesday Projects](/tidy-tuesday/index.html)

---
')

  file_path <- file.path(viz_dir, paste0(project$name, ".qmd"))
  writeLines(content, file_path)
  cat("Created:", file_path, "\n")
}

# Generate all visualization projects
cat("Generating visualization projects...\n")
for (project in viz_projects) {
  create_viz_project(project)
}

cat("Done! Generated", length(viz_projects), "visualization projects.\n")

