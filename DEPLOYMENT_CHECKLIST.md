# 503B Compliance Manufacturing Dashboard - Complete Deployment Guide

## Overview
This creates a sophisticated pharmaceutical manufacturing dashboard that replicates the premium aesthetic from your reference image while pulling real-time data from Google Sheets for 503B compliance monitoring.

## Features
- **Real-time Google Sheets integration** for live compliance data
- **Premium dark UI** with gold accents matching your reference
- **503B-specific metrics**: batch records, quality control, environmental monitoring
- **Mobile responsive** design with collapsible sidebar
- **Auto-refresh** every 5 minutes with live data sync

## Quick Start (3 Steps)

### Step 1: Fix Current Deployment Issue
Your current app has a chart error. Make this immediate fix:

```bash
# In your app.py, find create_deadline_chart() and change:
textposition='middle right'  # REMOVE this line
# TO:
textposition='inside'        # ADD this line

git add app.py
git commit -m "Fix chart textposition error"
git push
```

### Step 2: Replace with 503B Dashboard
Replace your current files with the new 503B compliance version:

```bash
# Replace your app.py with the 503B version
cp 503B_compliance_dashboard.py app.py

# Add Google Sheets integration
cp google_sheets.py .

# Update requirements
cp requirements.txt requirements.txt
```

### Step 3: Configure Google Sheets
1. **Create Google Spreadsheet** with the structure shown in GOOGLE_SHEETS_SETUP.md
2. **Set up Service Account** in Google Cloud Console
3. **Add environment variables** in Render:
   - `GOOGLE_SERVICE_ACCOUNT`: Your service account JSON
   - `GOOGLE_SPREADSHEET_ID`: Your spreadsheet ID

## Repository Structure
```
lexcura-dashboard/
├── app.py                     (→ 503B_compliance_dashboard.py)
├── google_sheets.py           (New - Google Sheets integration)
├── requirements.txt           (Updated with gspread)
├── runtime.txt               (Keep existing)
├── Procfile                  (Keep existing)
├── assets/
│   └── (your existing assets)
└── docs/
    ├── GOOGLE_SHEETS_SETUP.md
    └── 503B_DEPLOYMENT_GUIDE.md
```

## Key Differences from Reference Image

**Maintained Aesthetic Elements:**
- Dark charcoal background (#0A0B0D)
- Premium gold accents (#D4AF37, #E8C547)
- Sophisticated card-based layout
- Modern typography with Inter font
- Subtle shadows and gradients
- Professional sidebar navigation

**503B-Specific Adaptations:**
- **KPI Cards**: Total Batches, Quality Pass Rate, Compliance Score, Active Deviations, Inventory Status
- **Charts**: 
  - Production trends (daily batches + yield)
  - Quality radar (critical parameters)
  - Environmental monitoring (cleanroom zones)
  - Deviation trends (compliance tracking)
  - Inventory status (supply chain monitoring)

## Environment Variables for Render

Add these in your Render dashboard under Environment:

```bash
GOOGLE_SERVICE_ACCOUNT={"type":"service_account","project_id":"your-project-id","private_key_id":"abc123","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"503b-dashboard@your-project.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}

GOOGLE_SPREADSHEET_ID=1234567890abcdefghijklmnopqrstuvwxyz
```

## Sample Google Sheets Template

I recommend creating a Google Sheets template with sample 503B data:

**Spreadsheet Name**: "503B Compliance Tracking - [Your Company]"

**Required Sheets**:
1. **Batch Records** - Production batch tracking
2. **Quality Control** - QC test results and specifications  
3. **Inventory** - Raw materials and supplies tracking
4. **Deviations** - Quality deviations and CAPA tracking
5. **Environmental** - Cleanroom monitoring data
6. **Training Records** - Personnel qualification tracking

## Visual Comparison to Reference

**Your Reference Image Features** → **503B Dashboard Implementation**:
- Circular progress gauges → Environmental zone compliance gauges
- Production metrics → Batch production trends  
- Geographic data visualization → Quality parameter radar chart
- Status indicators → Deviation tracking and alerts
- Inventory management → Critical supplies monitoring
- Dark premium aesthetic → Exact color scheme replication

## Deployment Commands

```bash
# Update your repository
git add .
git commit -m "Deploy 503B compliance dashboard with Google Sheets integration"
git push

# Render will auto-deploy in 2-3 minutes
# Visit: https://your-app-name.onrender.com
```

## Testing Checklist

After deployment, verify:
- [ ] Dashboard loads with dark premium UI
- [ ] KPI cards show 503B metrics with gold styling
- [ ] Charts render with pharmaceutical data
- [ ] Google Sheets data syncs (or fallback data displays)
- [ ] Mobile responsive design works
- [ ] Auto-refresh updates every 5 minutes
- [ ] All 503B compliance areas covered

## Next Steps

1. **Immediate**: Fix the current textposition error
2. **Phase 1**: Deploy basic 503B dashboard with fallback data
3. **Phase 2**: Set up Google Sheets integration with your compliance data
4. **Phase 3**: Customize charts and KPIs for your specific 503B requirements

The dashboard will have the exact sophisticated appearance of your reference image while serving pharmaceutical manufacturing compliance needs.
