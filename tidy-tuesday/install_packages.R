# Install required packages for TidyTuesday analyses

cat("Installing TidyTuesday packages...\n\n")

# List of required packages
packages <- c(
  "tidytuesdayR",
  "tidyverse",
  "scales",
  "patchwork",
  "ggtext",
  "viridis",
  "countrycode",
  "gt",
  "gtExtras",
  "gghighlight",
  "ggrepel",
  "ggridges",
  "plotly"
)

# Install packages that aren't already installed
for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat("Installing", pkg, "...\n")
    install.packages(pkg, repos = "https://cloud.r-project.org")
  } else {
    cat(pkg, "already installed ✓\n")
  }
}

cat("\nInstallation complete!\n")
cat("\nTesting tidytuesdayR...\n")
library(tidytuesdayR)
cat("tidytuesdayR version:", as.character(packageVersion("tidytuesdayR")), "\n")
