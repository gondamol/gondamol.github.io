## ADDED Requirements

### Requirement: Health Research Blog Post Collection

The portfolio SHALL include a collection of comprehensive blog posts focused on health research methodologies and data science best practices that serve as educational resources and demonstrate domain expertise.

#### Scenario: Reproducible research blog post

- **WHEN** a visitor navigates to post 22 (reproducible-research-public-health)
- **THEN** they SHALL see comprehensive content covering:
  - Why reproducibility matters in public health
  - Tools and workflows (Git, R Markdown, Docker, renv)
  - Step-by-step examples and practical guidance
  - Resources for learning more
  - Code examples with proper syntax highlighting

#### Scenario: R programming tutorial blog post

- **WHEN** a visitor navigates to post 23 (r-for-health-researchers)
- **THEN** they SHALL see a complete beginner's guide covering:
  - R and RStudio setup instructions
  - Data manipulation with tidyverse
  - Statistical analysis for health research
  - Survival analysis and epidemiology packages
  - 30-day learning plan
  - Practical code examples that run in standard R environments

#### Scenario: Mobile data collection blog post

- **WHEN** a visitor navigates to post 24 (mobile-data-collection)
- **THEN** they SHALL see comprehensive guidance covering:
  - Mobile data collection platforms (ODK, KoboToolbox, CommCare, SurveyCTO)
  - Form design best practices and XLSForm syntax
  - Real-world implementation examples
  - Cost estimation and troubleshooting
  - Quality assurance strategies

#### Scenario: Dashboard visualization blog post

- **WHEN** a visitor navigates to post 25 (health-dashboard-visualization)
- **THEN** they SHALL see best practices and examples covering:
  - Dashboard design principles for health data
  - Chart selection guide for different data types
  - Color psychology and accessibility
  - Tools comparison (R Shiny, Flexdashboard, Tableau, Power BI)
  - Complete code examples with R and Python

### Requirement: Consistent Blog Post Structure

Each blog post SHALL follow a consistent structure and formatting that aligns with the portfolio's professional brand and technical conventions.

#### Scenario: YAML frontmatter requirements

- **WHEN** a blog post is created
- **THEN** it SHALL include YAML frontmatter with:
  - `title` - descriptive title
  - `subtitle` - explanatory subtitle
  - `author` - "Nichodemus Amollo"
  - `date` - publication date in YYYY-MM-DD format
  - `categories` - relevant categories as array

#### Scenario: Code syntax highlighting

- **WHEN** a blog post includes code examples
- **THEN** code blocks SHALL:
  - Use proper language identifiers (r, python, bash, yaml, markdown, etc.)
  - Follow tidyverse style guide for R code
  - Include comments explaining key steps
  - Be executable in standard environments

#### Scenario: Educational content structure

- **WHEN** a blog post provides tutorial or educational content
- **THEN** it SHALL include:
  - Clear section headings with hierarchy
  - Practical examples and use cases
  - Links to additional resources
  - Related posts cross-references
  - Tags for discoverability

### Requirement: SEO and Discoverability

Blog posts SHALL be optimized for search engine discoverability and include metadata that helps the target audience find relevant content.

#### Scenario: Descriptive titles and subtitles

- **WHEN** a blog post is created
- **THEN** titles SHALL:
  - Be descriptive and include key terms
  - Appeal to target audience (health researchers, data scientists)
  - Be under 70 characters for SEO
- **AND** subtitles SHALL provide additional context

#### Scenario: Category tagging

- **WHEN** a blog post is tagged with categories
- **THEN** categories SHALL:
  - Accurately describe the content domain
  - Be consistent with existing category taxonomy
  - Include relevant technical terms for searchability
  - Example categories: "Public Health", "R Programming", "Data Visualization", "Mobile Technology", "Research Methods"

#### Scenario: Internal linking

- **WHEN** a blog post references related content
- **THEN** it SHALL include:
  - Links to related blog posts
  - Links to relevant portfolio projects
  - Consistent link formatting with relative paths
  - Clear link text describing destination


