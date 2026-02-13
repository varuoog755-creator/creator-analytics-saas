#!/bin/bash
# Push Creator Analytics to GitHub & Deploy to Render

set -e

echo "🚀 Creator Analytics - GitHub + Render Deployment"
echo "================================================"

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not installed. Install with:"
    echo "   apt-get install gh"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "🔐 Login to GitHub:"
    echo "   gh auth login"
    echo ""
    echo "Or set GH_TOKEN environment variable:"
    echo "   export GH_TOKEN=your_github_token"
    exit 1
fi

# Create GitHub repo
echo "📦 Creating GitHub repository..."
gh repo create creator-analytics-saas --public --source=. --description "All-in-One Creator Analytics SaaS with ML Predictions"

# Push code
echo "📤 Pushing code to GitHub..."
git push -u origin master

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🎯 Now deploy to Render:"
echo ""
echo "1. Go to: https://dashboard.render.com/blueprints"
echo ""
echo "2. Click 'New Blueprint Instance'"
echo ""
echo "3. Connect your GitHub account"
echo ""
echo "4. Select repository: creator-analytics-saas"
echo ""
echo "5. Select file: backend/render.yaml"
echo ""
echo "6. Click 'Apply'"
echo ""
echo "✅ Render will create:"
echo "   - Web Service (API)"
echo "   - PostgreSQL Database"
echo ""
echo "📝 After deploy, get your API URL:"
echo "   https://creator-analytics-backend.onrender.com"
echo ""
echo "🔗 Deploy frontend to Vercel:"
echo "   cd frontend"
echo "   vercel deploy --prod"
echo ""
