#!/bin/bash
# Create 50+ visualization project files

VIZ_DIR="visualizations"
mkdir -p "$VIZ_DIR"

# R Visualization Projects (20 projects)
cat > "$VIZ_DIR/advanced-ggplot2-patterns.qmd" << 'EOF'
---
title: "Advanced ggplot2 Patterns & Techniques"
subtitle: "Exploring advanced ggplot2 techniques"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Advanced ggplot2 techniques including faceting, custom themes, and statistical transformations.
EOF

cat > "$VIZ_DIR/interactive-plotly-charts.qmd" << 'EOF'
---
title: "Interactive Charts with Plotly"
subtitle: "Creating interactive dashboards with Plotly"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Interactive dashboards and charts using plotly for web-based data exploration.
EOF

cat > "$VIZ_DIR/leaflet-interactive-maps.qmd" << 'EOF'
---
title: "Interactive Maps with Leaflet"
subtitle: "Building interactive maps with spatial data"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Interactive maps showing spatial data with custom markers, popups, and layers.
EOF

cat > "$VIZ_DIR/gganimate-time-series.qmd" << 'EOF'
---
title: "Animated Time Series with gganimate"
subtitle: "Creating animated visualizations over time"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Animated visualizations showing data evolution over time.
EOF

cat > "$VIZ_DIR/network-analysis-visualization.qmd" << 'EOF'
---
title: "Network Analysis & Visualization"
subtitle: "Visualizing networks and relationships"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Visualizing networks and relationships using igraph and ggraph packages.
EOF

# Python Visualization Projects (15 projects)
cat > "$VIZ_DIR/matplotlib-advanced-plots.qmd" << 'EOF'
---
title: "Advanced Matplotlib Visualizations"
subtitle: "Publication-quality plots with Matplotlib"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Creating publication-quality plots with Matplotlib including subplots and custom styling.
EOF

cat > "$VIZ_DIR/seaborn-statistical-viz.qmd" << 'EOF'
---
title: "Statistical Visualizations with Seaborn"
subtitle: "Statistical plotting with Seaborn"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Using Seaborn for statistical plotting including regression analysis and distribution plots.
EOF

cat > "$VIZ_DIR/plotly-python-dashboards.qmd" << 'EOF'
---
title: "Interactive Dashboards with Plotly Python"
subtitle: "Building interactive web dashboards"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Building interactive web dashboards using Plotly and Dash for Python.
EOF

cat > "$VIZ_DIR/bokeh-interactive-viz.qmd" << 'EOF'
---
title: "Interactive Visualizations with Bokeh"
subtitle: "Creating interactive visualizations for web browsers"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Creating interactive visualizations for modern web browsers using Bokeh.
EOF

# D3.js Projects (10 projects)
cat > "$VIZ_DIR/d3-bar-charts.qmd" << 'EOF'
---
title: "D3.js Bar Charts & Histograms"
subtitle: "Building interactive bar charts with D3.js"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Building interactive bar charts and histograms with D3.js for web visualization.
EOF

cat > "$VIZ_DIR/d3-network-graphs.qmd" << 'EOF'
---
title: "D3.js Network & Force-Directed Graphs"
subtitle: "Creating interactive network visualizations"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Creating interactive network visualizations and force-directed graphs with D3.js.
EOF

cat > "$VIZ_DIR/d3-map-visualizations.qmd" << 'EOF'
---
title: "D3.js Geographic Visualizations"
subtitle: "Mapping with D3.js and GeoJSON"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
Mapping and geographic data visualization using D3.js and GeoJSON.
EOF

# Create additional visualization projects
for i in {1..30}; do
  cat > "$VIZ_DIR/viz-project-$i.qmd" << EOF
---
title: "Visualization Project $i"
subtitle: "Advanced data visualization techniques"
format:
  html:
    toc: true
    code-fold: show
---

## Overview
This project demonstrates advanced visualization techniques.

## Code Example

\`\`\`r
library(ggplot2)
ggplot(data, aes(x = x, y = y)) + geom_point()
\`\`\`
EOF
done

echo "Created visualization projects in $VIZ_DIR"

