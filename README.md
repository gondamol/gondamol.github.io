# Nichodemus Amollo - Professional Portfolio

[![Quarto](https://img.shields.io/badge/Made%20with-Quarto-blue.svg)](https://quarto.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Senior Research Data Manager | Health Data Analytics Specialist**

Professional portfolio showcasing 7+ years of experience in health data analytics, survey design, and comprehensive data management. This portfolio demonstrates real-world impact in clinical trials, health systems research, and digital health solutions.

🌐 **Live Site:** [https://gondamol.github.io](https://gondamol.github.io)

---

## 📋 Table of Contents

- [Portfolio Highlights](#portfolio-highlights)
- [Site Structure](#site-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Building the Site](#building-the-site)
- [Deployment](#deployment)
- [Project Organization](#project-organization)
- [Customization Guide](#customization-guide)
- [Contact](#contact)

---

## 🌟 Portfolio Highlights

### **Professional Impact**
- 🏥 **100,000+** patients impacted through data-driven projects
- 📊 **500,000+** health records managed with 99.5% data quality
- 🗄️ **50+** electronic data capture systems designed and implemented
- 💰 **KES 20M+** in cost savings identified through analytics
- 👥 **500+** researchers trained in R programming and data management

### **Core Competencies**
- **Data Management:** REDCap, SurveyCTO, KoboCollect, PostgreSQL
- **Analytics:** R, Python, Stata, SQL, machine learning
- **Visualization:** R Shiny, Tableau, ggplot2, plotly
- **Health Expertise:** Clinical trials, NCDs, infectious diseases, health systems

---

## 📁 Site Structure

```
gondamol.github.io/
├── index.qmd                    # Homepage - professional summary
├── about/
│   └── index.qmd               # Detailed about page
├── cv/
│   └── index.qmd               # Comprehensive CV
├── projects/
│   ├── index.qmd               # Projects overview
│   ├── health-analytics.qmd    # Health analytics projects
│   ├── data-management.qmd     # Data management projects
│   ├── survey-tools.qmd        # Survey design projects
│   └── dashboards.qmd          # Dashboard projects
├── research/
│   ├── thesis.qmd              # MSc thesis with interactive dashboard
│   └── publications.qmd        # Publications and research
├── skills/
│   └── index.qmd               # Technical skills showcase
├── blogs/
│   └── index.qmd               # Blog and tutorials
├── tidy-tuesday/
│   └── index.qmd               # Data visualization challenges
├── _quarto.yml                 # Site configuration
├── custom.scss                 # Custom styling
└── styles.scss                 # Additional styles
```

---

## ✨ Key Features

### **1. Professional Positioning**
- Senior data manager with 7+ years experience
- Health data analytics specialist
- Survey design and implementation expert
- Remote-ready professional

### **2. Comprehensive Project Portfolio**
Organized into four main categories:
- **Health Data Analytics** - NCD management, COVID-19 analysis, predictive modeling
- **Data Management** - Clinical trials, cohort studies, surveillance systems
- **Survey Tools** - REDCap, SurveyCTO, KoboCollect implementations
- **Dashboards** - Interactive visualizations for decision-making

### **3. Interactive Thesis Dashboard**
- Real-time data visualization using R and plotly
- Geospatial analysis with leaflet
- KPI tracking and performance metrics
- Fully reproducible analysis

### **4. Social Media Ready Content**
Each project includes:
- Impact metrics and outcomes
- Social media highlight snippets
- Shareable achievements
- LinkedIn/Twitter-ready posts

### **5. Responsive Design**
- Mobile-first approach
- Works on all screen sizes
- Fast loading times
- Accessible (WCAG 2.1 compliant)

### **6. Professional Branding**
- Fitness enthusiast (4x weekly workouts) for peak performance
- Exercise commitment highlighted as professional advantage
- Personal wellness integrated with work excellence

---

## 🛠 Technologies Used

### **Core Technologies**
- **Quarto** - Static site generator for reproducible publishing
- **R** - Statistical computing and data visualization
- **R Markdown** - Dynamic document generation
- **SCSS/CSS** - Custom styling and responsive design

### **R Packages Used**
```r
library(tidyverse)      # Data manipulation and visualization
library(plotly)         # Interactive plots
library(leaflet)        # Interactive maps
library(DT)             # Interactive tables
library(shiny)          # Dashboard framework
```

### **Visualization Tools**
- ggplot2 for static visualizations
- plotly for interactivity
- leaflet for geospatial mapping
- DT for data tables

---

## 🚀 Building the Site

### **Prerequisites**
```bash
# Install Quarto
# Download from https://quarto.org/docs/get-started/

# Install R (version 4.0+)
# Download from https://cran.r-project.org/

# Install required R packages
Rscript -e "install.packages(c('tidyverse', 'plotly', 'leaflet', 'DT', 'rmarkdown'))"
```

### **Local Development**

1. **Clone the repository**
```bash
git clone https://github.com/gondamol/gondamol.github.io.git
cd gondamol.github.io
```

2. **Preview the site**
```bash
quarto preview
```
This will start a local server at `http://localhost:4444`

3. **Render the site**
```bash
quarto render
```
Output will be in the `_site/` directory

### **Live Reload**
Quarto automatically reloads the browser when you save changes to `.qmd` files.

---

## 📤 Deployment

### **GitHub Pages Deployment**

The site is automatically deployed to GitHub Pages using GitHub Actions.

**Manual deployment:**
```bash
# Render the site
quarto render

# Push to GitHub (gh-pages branch)
quarto publish gh-pages
```

### **Deployment Workflow**
1. Make changes to `.qmd` files
2. Commit and push to `main` branch
3. GitHub Actions automatically builds and deploys
4. Site live at https://gondamol.github.io

---

## 📂 Project Organization

### **Content Management**

**Adding New Projects:**
1. Create new `.qmd` file in appropriate `projects/` subdirectory
2. Use project card template
3. Include impact metrics and social media snippets
4. Add to appropriate category page

**Project Card Template:**
```markdown
::: {.project-card}
::: {.project-header}
#### Project Title
**Status:** Production | **Impact:** Metrics
:::

::: {.project-body}
Project description...

**Technologies:** List tools

**Social Media Highlight:**
> "Your impactful tweet-length description #hashtags"

[View Details →](#)
:::
:::
```

### **Adding Blog Posts**
1. Create new post in `posts/` directory
2. Update `blogs/index.qmd` with post card
3. Include code examples and practical tips

---

## 🎨 Customization Guide

### **Colors and Branding**
Edit `custom.scss`:
```scss
$primary: #2C5282;      // Primary brand color
$secondary: #38B2AC;    // Secondary accent
$success: #48BB78;      // Success indicators
```

### **Navigation Menu**
Edit `_quarto.yml`:
```yaml
navbar:
  left:
    - text: "New Section"
      href: newsection/index.qmd
```

### **Hero Banner**
Customize hero sections in individual `.qmd` files:
```markdown
::: {.hero-banner}
# Your Title
Your subtitle
:::
```

---

## 📊 Portfolio Statistics

### **Content Overview**
- **Total Pages:** 15+
- **Project Categories:** 4
- **Featured Projects:** 25+
- **Lines of Code:** 15,000+
- **Interactive Visualizations:** 10+

### **Professional Metrics Highlighted**
- 7+ years experience
- 50+ projects completed
- 100K+ patients impacted
- 500K+ records managed
- 99.5% average data quality
- KES 20M+ cost savings identified
- 500+ people trained

---

## 🔄 Maintenance

### **Regular Updates**
- **Monthly:** Add new blog posts
- **Quarterly:** Update project outcomes and metrics
- **Annually:** Refresh CV and publications

### **Dependencies**
Check for updates:
```bash
# Update Quarto
quarto update

# Update R packages
Rscript -e "update.packages()"
```

---

## 📖 Documentation

### **For Employers/Collaborators**
- Review [Projects](projects/index.qmd) for portfolio samples
- Check [CV](cv/index.qmd) for detailed experience
- See [Skills](skills/index.qmd) for technical capabilities

### **For Students/Learners**
- Explore [Blog](blogs/index.qmd) for tutorials
- Study [Thesis Project](research/thesis.qmd) as example
- Review [GitHub repositories](https://github.com/gondamol) for code

---

## 🤝 Connect with Me

- 💼 **LinkedIn:** [linkedin.com/in/amollow](https://linkedin.com/in/amollow)
- 🐙 **GitHub:** [github.com/gondamol](https://github.com/gondamol)
- 🐦 **Twitter:** [@nwerre](https://twitter.com/nwerre)
- 📊 **Kaggle:** [kaggle.com/nwerre](https://kaggle.com/nwerre)
- 📧 **Email:** [nichodemuswerre@gmail.com](mailto:nichodemuswerre@gmail.com)

---

## 🌟 Acknowledgments

This portfolio showcases real-world projects and experiences. All project descriptions reflect actual work, though specific organizational details and sensitive data are anonymized to protect confidentiality.

**Technologies and Tools:**
- Built with [Quarto](https://quarto.org)
- Styled with custom SCSS
- Deployed via GitHub Pages
- R visualizations with tidyverse ecosystem

---

## 📄 License

**Content:** © 2024 Nichodemus Amollo. All rights reserved.

**Code:** Open source under MIT License - feel free to use the site structure and styling for your own portfolio.

---

## 🚀 Future Enhancements

- [ ] Add blog post series on R for health researchers
- [ ] Develop interactive R packages (ncdfinance, surveyflow)
- [ ] Create video tutorials for complex analyses
- [ ] Add downloadable templates for common tasks
- [ ] Expand dashboard examples with live data
- [ ] Add case studies with full reproducible code

---

## 📝 Version History

**v2.0.0** (September 2024) - Complete portfolio revamp
- Repositioned as Senior Research Data Manager (7+ years)
- Added comprehensive project categories
- Integrated thesis dashboard with interactive visualizations
- Enhanced responsive design
- Added social media ready content
- Highlighted fitness/wellness for peak performance

**v1.0.0** (2023) - Initial portfolio launch

---

**Built with ❤️ and ☕ by Nichodemus Amollo**

*Transforming health data into actionable insights, one project at a time.*
