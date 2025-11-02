# Project Context

## Purpose
Professional portfolio and personal website for Nichodemus Amollo, showcasing expertise as a Senior Research Data Manager and Health Data Analytics Specialist with 7+ years of experience in health research, data management, and survey design.

## Tech Stack
- **Quarto** - Static site generator for reproducible scientific publishing
- **R** - Statistical computing and data analysis (tidyverse, ggplot2, plotly, leaflet, DT)
- **R Markdown/Quarto Markdown (.qmd)** - Dynamic document generation
- **SCSS/CSS** - Custom styling (custom.scss, styles.scss)
- **GitHub Pages** - Hosting and deployment
- **Git** - Version control

## Project Conventions

### Content Organization
- **Main sections:** Home, About, Projects, Research, Blog, CV, Skills, Resources, TidyTuesday
- **Project categories:** Health Analytics, Data Management, Survey Tools, Dashboards
- **Blog posts:** Numbered sequentially (01-, 02-, etc.) in `posts/` directory
- **Each blog post:** Individual folder with `index.qmd` file
- **Metadata:** YAML frontmatter with title, subtitle, author, date, categories, image (optional)

### File Naming Conventions
- Quarto documents: `kebab-case.qmd`
- Blog post folders: `##-descriptive-name/` (e.g., `01-data-analytics-roadmap/`)
- Images: `descriptive-name.jpg/png`
- Directories: `lowercase-with-hyphens/`

### Code Style
- **R code:** tidyverse style guide
- **Markdown:** Standard markdown with Quarto extensions
- **YAML:** 2-space indentation
- **Line length:** Prefer 80-100 characters for readability
- **Code blocks:** Use fenced code blocks with language identifiers

### Content Style
- **Professional tone:** Accessible but authoritative
- **Target audience:** Health researchers, data scientists, potential employers
- **Include:** Practical examples, code snippets, real-world applications
- **Highlight:** Impact metrics, technologies used, outcomes achieved
- **Social media ready:** Include shareable snippets and key takeaways

### Git Workflow
- **Main branch:** `main` (production-ready)
- **Commit messages:** Descriptive, present tense (e.g., "Add new blog posts on health research")
- **Deployment:** Automatic via GitHub Pages when pushed to main
- **Local testing:** Use `quarto preview` before committing

## Domain Context

### Health Data Science Focus
- **Clinical trials** - REDCap, data management, monitoring
- **Public health surveillance** - Disease tracking, outbreak detection
- **Non-communicable diseases (NCDs)** - Diabetes, hypertension, cancer
- **Health financial diaries** - Livelihood analysis, financial behavior
- **Mobile data collection** - ODK, KoboToolbox, SurveyCTO
- **Statistical analysis** - R, Stata, epidemiological methods
- **Data visualization** - Dashboards, interactive reports, geospatial analysis

### Target Audience
- **Primary:** Potential employers, collaborators, research institutions
- **Secondary:** Health researchers learning data science, students, data professionals
- **Tertiary:** General audience interested in health data analytics

### Key Themes
- Reproducible research and open science
- Practical, implementable solutions
- Real-world impact and outcomes
- Evidence-based decision making
- Capacity building and training

## Important Constraints

### Technical Constraints
- **Static site only** - No backend/database (GitHub Pages limitation)
- **R environment** - Code examples should run in standard R environments
- **Browser compatibility** - Must work on modern browsers (Chrome, Firefox, Safari, Edge)
- **Mobile responsive** - Content must be readable on all screen sizes
- **Performance** - Fast loading times, optimized images

### Content Constraints
- **Confidentiality** - Anonymize sensitive organizational and patient data
- **Professional standards** - Maintain high quality, accurate information
- **Ethical guidelines** - Follow research ethics and data privacy principles
- **Copyright** - Use only licensed or own images/content

### Deployment Constraints
- **GitHub Pages** - Free tier with public repository
- **Custom domain** - gondamol.github.io
- **Build time** - Quarto render must complete successfully
- **File size** - Keep repository size reasonable (<1GB)

## External Dependencies

### Primary Tools
- **Quarto** - v1.3+ for site generation
- **R** - v4.0+ for statistical computing
- **Git/GitHub** - Version control and hosting

### R Package Dependencies
- tidyverse (data manipulation)
- ggplot2 (visualization)
- plotly (interactive plots)
- leaflet (maps)
- DT (data tables)
- rmarkdown (document generation)
- knitr (code execution)

### External Services
- **GitHub Pages** - Static site hosting
- **GitHub Actions** - CI/CD (if configured)
- **Google Analytics** - Traffic monitoring (if configured)

### Reference Materials
- Quarto documentation: https://quarto.org
- tidyverse style guide: https://style.tidyverse.org/
- R for Data Science: https://r4ds.hadley.nz/

## Portfolio Statistics
- **Content:** 15+ pages, 25+ projects, multiple blog posts
- **Impact metrics:** 100K+ patients, 500K+ records, 500+ trained
- **Experience:** 7+ years in health data management
- **Technical depth:** Advanced R, Python, SQL, data visualization
