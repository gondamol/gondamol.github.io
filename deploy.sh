#!/bin/bash

# Portfolio Deployment Script
# Automates the workflow of committing source files and publishing to GitHub Pages

set -e  # Exit on error

echo "🚀 Portfolio Deployment Script"
echo "=============================="
echo ""

# Step 1: Check for uncommitted changes
echo "📋 Step 1: Checking git status..."
if ! git diff-index --quiet HEAD --; then
    echo "✅ Found changes to commit"
else
    echo "⚠️  No changes detected. Exiting."
    exit 0
fi

# Step 2: Show what will be committed
echo ""
echo "📝 Step 2: Files that will be committed:"
echo "----------------------------------------"
git status --short
echo ""

# Step 3: Get commit message from user
read -p "💬 Enter commit message (or press Enter for default): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update portfolio content - $(date +%Y-%m-%d)"
fi

# Step 4: Stage only source files (exclude _site/)
echo ""
echo "📦 Step 3: Staging source files..."
git add *.qmd
git add **/*.qmd
git add _quarto.yml
git add styles.scss
git add custom.scss 2>/dev/null || true
git add README.md 2>/dev/null || true

# Make sure _site/ is not staged
git reset HEAD _site/ 2>/dev/null || true

echo "✅ Source files staged"

# Step 5: Commit
echo ""
echo "💾 Step 4: Committing changes..."
git commit -m "$COMMIT_MSG"
echo "✅ Changes committed"

# Step 6: Push to main
echo ""
echo "⬆️  Step 5: Pushing to GitHub main branch..."
git push origin main
echo "✅ Pushed to main branch"

# Step 7: Ask about publishing to GitHub Pages
echo ""
echo "🌐 Step 6: Publish to GitHub Pages?"
echo "This will render your site and deploy it live."
read -p "Proceed with publishing? (y/n): " PUBLISH

if [ "$PUBLISH" = "y" ] || [ "$PUBLISH" = "Y" ]; then
    echo ""
    echo "🎨 Rendering and publishing site..."
    quarto publish gh-pages --no-browser
    echo ""
    echo "✅ Successfully published to GitHub Pages!"
    echo "🌍 Your site will be live at: https://gondamol.github.io"
    echo "⏰ Note: GitHub Pages may take 1-2 minutes to update"
else
    echo ""
    echo "⏸️  Skipped publishing. You can publish later with:"
    echo "   quarto publish gh-pages"
fi

echo ""
echo "🎉 Deployment complete!"
