# 🚀 Portfolio Deployment Guide

Quick reference for building and deploying your revamped portfolio.

## ⚡ Quick Start

```bash
# 1. Preview locally (auto-reload on changes)
quarto preview

# 2. Build the site
quarto render

# 3. Deploy to GitHub Pages
quarto publish gh-pages
```

## 📋 Pre-Deployment Checklist

### **Content Review**
- [ ] Update personal information (email, LinkedIn, GitHub URLs)
- [ ] Replace placeholder social media highlights with actual content
- [ ] Add real publication details in `research/publications.qmd`
- [ ] Verify all project impact metrics are accurate
- [ ] Update CV dates and experiences to match reality
- [ ] Add your actual education details

### **Visual Assets**
- [ ] Replace `profile.jpg` with your professional photo
- [ ] Add project screenshots if available
- [ ] Create favicon (optional)

### **Links & References**
- [ ] Test all internal links work correctly
- [ ] Verify external links (GitHub, LinkedIn, etc.)
- [ ] Ensure email links are correct
- [ ] Check that all `[View Details →](#)` placeholders are updated

### **Responsive Design**
- [ ] Test on mobile devices
- [ ] Test on tablets
- [ ] Test on different desktop sizes
- [ ] Check all pages for proper layout

## 🔧 Configuration Updates

### **1. Update Site URLs in `_quarto.yml`**
```yaml
website:
  site-url: "https://gondamol.github.io"  # Your actual URL
```

### **2. Verify Social Links**
Replace all instances of placeholder URLs:
- LinkedIn: `https://linkedin.com/in/amollow`
- GitHub: `https://github.com/gondamol`
- Twitter: `https://twitter.com/nwerre`
- Kaggle: `https://kaggle.com/nwerre`
- Email: `nichodemuswerre@gmail.com`

### **3. Google Analytics (Optional)**
Add to `_quarto.yml`:
```yaml
website:
  google-analytics: "G-XXXXXXXXXX"
```

## 📊 Thesis Dashboard Data

The thesis dashboard (`research/thesis.qmd`) currently uses **simulated data**. To use real data:

### **Option 1: Update R Code**
Replace the `set.seed(123)` simulation code with your actual data import:

```r
# Replace simulation with real data
facilities <- read_csv("data/facility_data.csv")
```

### **Option 2: Keep Simulation (Recommended for Demo)**
The current simulation is perfect for demonstration purposes. It shows:
- Interactive visualizations
- Dashboard capabilities
- Technical skills

Add a note that data is simulated for privacy.

## 🎨 Customization

### **Brand Colors**
Edit `custom.scss` to match your preferred colors:
```scss
$primary: #2C5282;      // Main brand color
$secondary: #38B2AC;    // Accent color
```

### **Profile Photo**
Replace `profile.jpg` in the root directory with your photo:
- Recommended size: 400x400px
- Format: JPG or PNG
- Professional headshot recommended

## 🔍 SEO Optimization

### **Meta Descriptions**
Each page has been configured with descriptions. Verify they're accurate:
- Homepage highlights "Senior Research Data Manager" positioning
- Projects page emphasizes real-world impact
- CV page shows 7+ years experience

### **Social Media Cards**
When shared on social media, your portfolio will show:
- Title: "Nichodemus Amollo | Senior Research Data Manager"
- Description: Automatically pulled from page metadata
- Image: Your profile photo

## 📱 Social Media Strategy

### **LinkedIn Post Template**
```
🎉 Excited to share my revamped portfolio!

As a Senior Research Data Manager with 7+ years experience, I've:
✅ Managed 500K+ health records (99.5% quality)
✅ Designed 50+ data collection systems
✅ Trained 500+ researchers in R and data management
✅ Identified KES 20M+ in cost savings

Check out my projects in:
🏥 Health Data Analytics
🗄️ Data Management
📋 Survey Design
📊 Interactive Dashboards

[Your Portfolio URL]

#DataScience #HealthAnalytics #DataManagement #GlobalHealth
```

### **Twitter Thread Starters**
Each project has a "Social Media Highlight" section - use these for Twitter threads!

Example:
```
1/ Just completed analysis of COVID-19 vaccination coverage in Kisumu County 🇰🇪

Used geospatial analysis to identify 12 underserved areas with <40% coverage

Thread on how data-driven decisions saved lives 🧵👇

#DataForGood #PublicHealth
```

## 🐛 Common Issues & Solutions

### **Issue: Quarto not found**
```bash
# Install Quarto from https://quarto.org
# Or use package manager:
brew install quarto  # macOS
```

### **Issue: R packages missing**
```bash
Rscript -e "install.packages(c('tidyverse', 'plotly', 'leaflet', 'DT'))"
```

### **Issue: GitHub Pages not updating**
```bash
# Force rebuild
quarto render
git add .
git commit -m "Force rebuild"
git push origin main

# Or republish
quarto publish gh-pages --no-prompt
```

### **Issue: CSS not loading**
Clear browser cache and hard reload (Ctrl+F5 or Cmd+Shift+R)

## 📈 Analytics & Tracking

### **Key Metrics to Monitor**
After deployment, track:
- Page views on Projects section (should be highest)
- CV downloads/views
- Time spent on thesis dashboard
- Traffic sources (LinkedIn, Twitter, direct)

### **Tools**
- Google Analytics (add to `_quarto.yml`)
- LinkedIn Analytics (for post performance)
- GitHub Pages traffic (repository Insights)

## 🔄 Regular Maintenance

### **Monthly**
- [ ] Add new blog post or project update
- [ ] Update project metrics with latest outcomes
- [ ] Share 2-3 social media posts about your work

### **Quarterly**
- [ ] Review and update CV
- [ ] Add any new certifications or training
- [ ] Update project status (completed, ongoing, new)

### **Annually**
- [ ] Refresh all impact metrics
- [ ] Update professional summary
- [ ] Review and update skills section
- [ ] Archive old projects, highlight recent ones

## 💼 Job Application Tips

When applying for positions, reference specific pages:

**For Senior Data Manager roles:**
> "I've managed 20+ multi-site studies with 99.5% data quality. See my data management projects: [URL]/projects/data-management.qmd"

**For Health Analytics roles:**
> "My COVID-19 vaccination analysis led to policy changes affecting 100K+ people. Details: [URL]/projects/health-analytics.qmd"

**For Remote positions:**
> "I've successfully managed international projects remotely for 5+ years. View my full portfolio: [URL]"

## 🎯 Next Steps After Deployment

1. **Share on LinkedIn** - Announce your new portfolio
2. **Update Resume** - Add portfolio URL
3. **Email Signature** - Include portfolio link
4. **Job Applications** - Reference specific project pages
5. **Networking** - Share with colleagues and mentors
6. **Content Creation** - Start writing blog posts
7. **Project Updates** - Document ongoing work

## 📞 Support & Questions

If you need help:
- Review Quarto documentation: https://quarto.org/docs/
- Check R package documentation for visualization issues
- Test thoroughly before promoting widely

## ✅ Final Checklist Before Going Live

- [ ] All personal information updated
- [ ] Profile photo replaced
- [ ] All links tested and working
- [ ] Mobile responsiveness verified
- [ ] Browser compatibility checked (Chrome, Firefox, Safari)
- [ ] No typos or grammatical errors
- [ ] Social media accounts updated with portfolio link
- [ ] Resume/CV updated with portfolio URL
- [ ] Site previewed by a colleague/friend
- [ ] Analytics configured (if desired)
- [ ] First LinkedIn post drafted and ready

---

## 🎊 You're Ready!

Your portfolio now positions you as a **Senior Research Data Manager** with:
- 7+ years of documented experience
- Real-world project impact
- Comprehensive technical skills
- Social media ready content
- Professional positioning for remote roles

**Deploy with confidence and start sharing your work!**

---

**Need to make changes after deployment?**
Just update the `.qmd` files, run `quarto render`, and push to GitHub. Changes are typically live within 2-5 minutes.

**Good luck! 🚀**
