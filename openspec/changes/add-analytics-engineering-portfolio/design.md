## Context

The portfolio needs to evolve from a healthcare-focused showcase to a comprehensive analytics engineering portfolio that demonstrates capabilities across multiple high-value industries while maintaining the strong health data science foundation.

**Current State:**
- Excellent health data projects (clinical trials, surveys, dashboards)
- 25 blog posts on data analytics topics
- R package development in planning (surveyKE)
- Single-domain focus limits broader market appeal

**Target State:**
- Multi-industry analytics engineering showcase
- End-to-end project demonstrations (data → insights → decisions)
- Clear package development strategy
- World-class portfolio features matching top Quarto examples

**Constraints:**
- Static site only (GitHub Pages)
- Must maintain existing URLs (no breaking changes)
- Reasonable build times (< 10 minutes)
- Repository size < 1GB
- All code must be reproducible

## Goals / Non-Goals

### Goals

1. **Demonstrate Full-Stack Analytics Engineering**
   - Complete data pipelines (ingestion, transformation, loading)
   - Multiple visualization frameworks
   - Business impact quantification
   - Executive communication skills

2. **Expand Industry Credibility**
   - Healthcare (existing strength)
   - Finance/Banking (high-value sector)
   - Retail (analytics maturity)
   - Energy (emerging sector)

3. **Establish Reusable Framework**
   - Project template structure
   - Consistent documentation patterns
   - Reproducible workflows
   - ROI calculation methodologies

4. **Professional Package Showcase**
   - Clear development roadmap
   - Integration with portfolio brand
   - Community building potential

### Non-Goals

1. **Not building production systems** - Projects are demonstrations, not deployed services
2. **Not real-time requirements** - Static dashboards acceptable
3. **Not proprietary data** - Use open/synthetic datasets only
4. **Not comprehensive tutorials** - Focus on showcasing, not teaching
5. **Not replacing existing health projects** - Additive, not replacement

## Decisions

### Decision 1: Folder Structure for Analytics Engineering Projects

**Chosen Approach:**

```
projects/analytics-engineering/
├── index.qmd                          # Landing page
├── healthcare-readmission/
│   ├── index.qmd                      # Project overview
│   ├── README.md                      # Technical documentation
│   ├── data/
│   │   ├── raw/                       # Synthetic data
│   │   ├── processed/                 # Transformed data
│   │   └── README.md                  # Data dictionary
│   ├── pipeline/
│   │   ├── 01-extract.py              # Data extraction
│   │   ├── 02-transform.sql           # SQL transformations
│   │   ├── 03-load.py                 # Data loading
│   │   └── requirements.txt
│   ├── dashboard/
│   │   ├── app.R                      # Shiny dashboard
│   │   └── assets/
│   ├── presentation/
│   │   ├── executive-summary.pptx
│   │   └── slides.pdf
│   ├── analysis/
│   │   ├── roi-calculations.xlsx
│   │   └── methodology.md
│   └── outputs/
│       ├── figures/
│       └── reports/
├── banking-fraud-detection/
│   └── [same structure]
├── retail-optimization/
│   └── [same structure]
├── energy-forecasting/
│   └── [same structure]
└── finance-clv-churn/
    └── [same structure]
```

**Rationale:**
- Self-contained projects, easy to navigate
- Consistent structure aids understanding
- Separate concerns (pipeline, dashboard, presentation)
- Ready for GitHub submodule extraction if needed
- Supports reproducibility

**Alternatives Considered:**
- ❌ Flat structure - Too messy with 5 projects
- ❌ Single project with multiple industries - Less clear
- ❌ Separate repositories - Complicates portfolio deployment

### Decision 2: Visualization Framework Strategy

**Chosen Approach: Multi-Framework Showcase**

Each project uses a different framework to demonstrate versatility:

1. **Healthcare** - R Shiny + Flexdashboard (leverages existing R strength)
2. **Banking** - Python Streamlit (modern Python ecosystem)
3. **Retail** - Plotly Dash (interactive web dashboards)
4. **Energy** - React + D3.js (modern JavaScript, impressive visuals)
5. **Finance** - Vue.js + Plotly.js (SPA framework showcase)

**Rationale:**
- Demonstrates polyglot capabilities
- Each framework's strengths highlighted
- Broader appeal to different tech stacks
- Educational value for visitors
- Portfolio differentiation

**Trade-offs:**
- ✅ Versatility demonstration
- ✅ Broader technical credibility
- ❌ Increased complexity/maintenance
- ❌ Longer learning curve
- ❌ More dependencies

**Mitigation:** Start with Shiny and Streamlit (2 familiar frameworks), add others gradually

### Decision 3: Package Development Organization

**Chosen Approach: Hybrid Model**

**Structure:**
```
GitHub Organization: gondamol
├── surveyKE (separate repo)
├── healthFinanceDiary (separate repo)
├── kenyanStats (separate repo)
└── gondamol.github.io (portfolio repo)

Portfolio Integration:
software/
├── index.qmd                # Overview of all packages
├── surveyKE/
│   └── index.qmd            # Package showcase page
├── healthFinanceDiary/
│   └── index.qmd
└── kenyanStats/
    └── index.qmd
```

**Each package repo includes:**
- Standard R package structure
- CI/CD (GitHub Actions)
- pkgdown documentation site
- Test suite
- Vignettes

**Portfolio pages show:**
- Package overview and vision
- Installation instructions
- Quick start examples
- Link to full documentation (pkgdown site)
- Development roadmap
- GitHub repo links

**Rationale:**
- Follows R community best practices
- Packages can be installed independently
- Portfolio as "marketing site"
- Version control independence
- Collaboration-friendly

**Alternatives Considered:**
- ❌ Packages in portfolio repo - Breaks R conventions
- ❌ No portfolio integration - Missed visibility opportunity
- ❌ Only external links - Missed storytelling opportunity

### Decision 4: Data Strategy

**Chosen Approach: Synthetic + Open Data**

For each project:

1. **Start with open datasets** where available
   - Healthcare: CMS public data, MIMIC-III (with license)
   - Finance: Kaggle competitions, synthetic datasets
   - Retail: UCI ML repository, synthetic
   - Energy: Open energy data platforms

2. **Generate realistic synthetic data** when needed
   - Python: Faker, SDV (Synthetic Data Vault)
   - R: synthpop, simstudy
   - Maintain statistical properties
   - Document generation process

3. **Data governance**
   - All datasets < 50MB (GitHub friendly)
   - LICENSE.md for each dataset
   - Clear data dictionary
   - Privacy compliance (no real PII)

**Rationale:**
- Legal compliance
- Reproducibility
- Shareability
- Professional ethics

### Decision 5: ROI Calculation Framework

**Chosen Approach: Standardized Template**

Each project includes:

```yaml
roi_framework:
  problem:
    - Current state metrics
    - Industry benchmarks
    - Cost of problem (quantified)
  
  solution:
    - Proposed intervention
    - Implementation cost
    - Ongoing costs
  
  impact:
    - Key metrics improved
    - Percent improvement
    - Financial value (annualized)
  
  roi_calculation:
    - Total benefit ($)
    - Total cost ($)
    - Net benefit ($)
    - ROI percentage
    - Payback period (months)
    - 5-year NPV
  
  assumptions:
    - List all assumptions
    - Sensitivity analysis
    - Risk factors
```

**Rationale:**
- Consistent, professional format
- Demonstrates business acumen
- Appeals to decision-makers
- Teachable framework

## Risks / Trade-offs

### Risk 1: Scope Creep

**Risk:** 5 comprehensive projects is substantial work

**Mitigation:**
- Phase delivery: 2 projects → 3 more → polish
- Minimum viable projects first
- Templates after 1st project
- Time-box each project (2 weeks max)

### Risk 2: Framework Maintenance

**Risk:** Multiple frameworks = more dependencies to maintain

**Mitigation:**
- Use stable, mature frameworks
- Pin dependency versions
- Automated dependency updates (Dependabot)
- Focus on 2-3 primary frameworks initially

### Risk 3: Build Time

**Risk:** Complex projects might slow Quarto rendering

**Mitigation:**
- Use Quarto freeze for computationally expensive content
- Render dashboards separately, embed via iframe
- Optimize images and assets
- Conditional rendering (dev vs prod)

### Risk 4: Credibility of Synthetic Data

**Risk:** Employers may question synthetic projects vs real work

**Mitigation:**
- Clear labeling as "demonstration projects"
- Industry-validated problem definitions
- Realistic scenarios and data patterns
- Complement with real work (health projects)
- Professional presentation quality

### Risk 5: Portfolio Bloat

**Risk:** Too much content overwhelming to visitors

**Mitigation:**
- Clear navigation structure
- Progressive disclosure (overview → details)
- Featured projects on homepage
- Search functionality
- Analytics to track engagement

## Migration Plan

### Phase 1: Foundation (Weeks 1-2)

1. Create analytics-engineering folder structure
2. Develop project template
3. Research industry problems (all 5)
4. Build Healthcare project (familiar domain)
   - Pipeline (Python + SQL)
   - Shiny dashboard
   - Executive presentation
   - ROI calculation
5. Document patterns and lessons learned

### Phase 2: Expansion (Weeks 3-4)

6. Build Banking/Finance project (Streamlit)
7. Refine template based on learnings
8. Add analytics-engineering to main navigation
9. Create landing page with all projects overview

### Phase 3: Scale (Weeks 5-7)

10. Build Retail project (Plotly Dash)
11. Build Energy project (React + D3.js)
12. Build Finance CLV project (Vue.js)
13. Cross-project code review and harmonization

### Phase 4: Enhancement (Weeks 8-9)

14. Package development strategy pages
15. Portfolio enhancements (search, comments, etc.)
16. Performance optimization
17. Documentation polish
18. SEO optimization

### Phase 5: Launch (Week 10)

19. Comprehensive testing
20. Soft launch (selected sharing)
21. Gather feedback
22. Iterate and improve
23. Full launch
24. Social media announcement

## Rollback Plan

If major issues arise:
1. Projects are additive - can be removed without breaking existing site
2. Version control allows reverting to previous state
3. Each project self-contained - can disable individually
4. Quarto freeze means pre-rendered content available
5. Staging branch for testing before main

## Open Questions

1. **Industry Focus Priority?**
   - Current: Healthcare → Banking → Retail → Energy → Finance
   - Alternative: User feedback on which industries to prioritize?
   - **Resolution needed:** Week 1

2. **Dashboard Hosting?**
   - Static HTML exports vs live Shiny/Streamlit apps?
   - If live: ShinyApps.io free tier? Streamlit Cloud?
   - **Resolution needed:** Week 2

3. **Executive Presentations?**
   - PowerPoint → PDF export?
   - Or create web-based presentations (Quarto Reveal.js)?
   - **Resolution needed:** Week 1

4. **Synthetic Data Generation?**
   - Build custom generator tool?
   - Use existing packages?
   - Document methodology where?
   - **Resolution needed:** Week 2

5. **Video Content?**
   - Add project walkthrough videos?
   - Screen recordings of dashboards?
   - Platform: YouTube? Self-hosted?
   - **Resolution needed:** Week 5 (if yes)

6. **Interactive Demos?**
   - Embed live dashboards?
   - Host on external platforms?
   - Cost implications?
   - **Resolution needed:** Week 3

## Success Metrics

### Quantitative

- ✅ 5 complete analytics engineering projects
- ✅ 5 executive presentations
- ✅ 5 ROI calculations documented
- ✅ 3+ visualization frameworks demonstrated
- ✅ 100% projects with reproducible code
- ✅ Portfolio build time < 10 minutes
- ✅ Repository size < 1GB

### Qualitative

- ✅ Professional quality comparable to top portfolios
- ✅ Clear value proposition for each project
- ✅ Consistent branding and design
- ✅ Compelling narratives
- ✅ Easy navigation and discovery

### Engagement (Post-Launch)

- 📊 40% increase in portfolio views (3 months)
- 📊 50% increase in project page engagement
- 📊 30% increase in contact form submissions
- 📊 LinkedIn profile views +50%
- 📊 GitHub repo stars +100

### Professional Impact

- 💼 Interviews from finance/banking/retail sectors
- 💼 Consulting inquiries from new industries
- 💼 Speaking opportunities at analytics conferences
- 💼 Community recognition and citations


