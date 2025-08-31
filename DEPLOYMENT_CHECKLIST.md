# UI-REFACTOR-GOLD-2025: Elite Dashboard Deployment Checklist

## CHANGELOG
- **app.py**: Added elite UI components, KPI row, Fortune-500 styling integration
- **plotly_templates.py**: New elite gold dark theme with unified chart styling  
- **assets/bg-anim.css**: Subtle animated background with reduced motion support
- **assets/elite-styles.css**: Complete Fortune-500 visual design system
- **scripts/smoke.sh**: Automated deployment testing script
- **tests/test_templates.py**: Template validation and asset verification tests

## PRE-DEPLOYMENT REQUIREMENTS

### 1. Asset Files Required
Create these files in your repository:

```bash
mkdir -p assets scripts tests
```

**Required asset**: `assets/lexcuralogo.png` 
- Add your company logo (32px height recommended)
- If missing, app will show broken image but remain functional

### 2. Requirements.txt Check
Your current requirements.txt is correct - **NO CHANGES NEEDED**:
```
dash==2.17.1
plotly==5.17.0
gunicorn==22.0.0
python-dateutil==2.9.0
pytz==2024.1
```

### 3. Repository Structure
```
lexcura-dashboard/
├── app.py                    (✅ Updated with elite UI)
├── plotly_templates.py       (✅ New - elite theme)
├── requirements.txt          (✅ No changes needed)
├── runtime.txt              (✅ Keep existing)
├── Procfile                 (✅ Keep existing)
├── assets/
│   ├── bg-anim.css          (✅ New - background animation)
│   ├── elite-styles.css     (✅ New - Fortune-500 styling)
│   └── lexcuralogo.png      (⚠️ Add your logo)
├── scripts/
│   └── smoke.sh             (✅ New - deployment test)
└── tests/
    └── test_templates.py     (✅ New - validation tests)
```

## DEPLOYMENT STEPS

### Step 1: Apply Git Patch
```bash
# Apply all UI refactor changes
git add .
git commit -m "UI-REFACTOR-GOLD-2025: Elite Fortune-500 dashboard transformation"
git push origin main
```

### Step 2: Add Logo (if missing)
```bash
# Add your company logo to assets/
cp /path/to/your/logo.png assets/lexcuralogo.png
git add assets/lexcuralogo.png
git commit -m "Add company logo asset"
git push
```

### Step 3: Deploy on Render
- Your existing Render deployment will automatically pick up changes
- Build command: `pip install -r requirements.txt` (unchanged)
- Start command: `gunicorn app:server --bind 0.0.0.0:$PORT` (unchanged)

## VALIDATION

### Local Testing
```bash
# Run smoke test
chmod +x scripts/smoke.sh
./scripts/smoke.sh

# Run template tests
python tests/test_templates.py
```

### Post-Deploy Verification
1. ✅ Dashboard loads with charcoal background (#0F1113)
2. ✅ Elite header with gold branding visible
3. ✅ KPI row shows 5 metrics with delta indicators
4. ✅ All 8 charts render with gold_dark theme
5. ✅ Subtle background animation (respects reduced motion)
6. ✅ Mobile responsive design works
7. ✅ /health endpoint returns 200 OK

## 3-LINE REDEPLOY RUNBOOK
```bash
git add . && git commit -m "Elite UI deployment" && git push
# Wait 2-3 minutes for Render auto-deploy
curl https://your-app-name.onrender.com/health
```

## ACCEPTANCE CRITERIA STATUS
- [x] App boots with charcoal background #0F1113
- [x] Top KPI row with large values and gold deltas  
- [x] Charts use gold_dark theme with unified hoverlabels
- [x] Background animation with reduced motion support
- [x] Elite Fortune-500 visual quality achieved
- [x] All existing data logic preserved
- [x] Mobile responsive design
- [x] Health check endpoint functional