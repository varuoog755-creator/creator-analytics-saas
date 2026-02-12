#!/bin/bash
# Creator Analytics - Vercel Deploy Script

echo "🚀 Deploying Creator Analytics to Vercel..."
echo "============================================"

# Check if logged in
if ! vercel whoami &>/dev/null; then
    echo "❌ Please login first:"
    echo "   vercel login"
    exit 1
fi

# Deploy frontend
echo "📦 Deploying frontend..."
cd frontend
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Set environment variables in Vercel dashboard"
echo "2. Deploy backend to Railway/Render/AWS"
echo "3. Update NEXT_PUBLIC_API_URL to point to backend"
