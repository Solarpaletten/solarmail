# 🛠️ Sprint 0.4.2 Integration Instructions

**For:** Leanid (Архитектор)  
**Sprint:** 0.4.2 - API Integration  
**Date:** October 26, 2025

---

## 📋 Overview

This guide provides step-by-step instructions to integrate Sprint 0.4.2 changes into the SolarMail repository.

---

## 🎯 Changes Summary

**Files to Add:**
- `lib/errors.ts` (New)
- `components/ui/api-status-badge.tsx` (New)
- `components/ui/loading-spinner.tsx` (New)
- `components/ui/error-display.tsx` (New)
- `tests/api.test.ts` (New)
- `tests/TESTING.md` (New)
- `SPRINT_0.4.2_REPORT.md` (New)

**Files to Update:**
- `lib/api.ts` (Complete rewrite)
- `components/layout/header.tsx` (Add API status badge)
- `components/mail/mail-list.tsx` (Use real API data)
- `components/mail/analyzer-view.tsx` (Use real API data)
- `components/mail/stats-cards.tsx` (Use real API data)
- `app/dashboard/page.tsx` (Minor updates)
- `README_FRONTEND.md` (Updated for v0.4.2)

---

## 🚀 Integration Steps

### **Step 1: Backup Current State**

```bash
cd /path/to/solarmail

# Create backup branch
git checkout -b backup-pre-0.4.2
git push origin backup-pre-0.4.2

# Return to main
git checkout main
```

### **Step 2: Create Feature Branch**

```bash
# Create new feature branch
git checkout -b feature/sprint-0.4.2-api-integration

# Verify current branch
git branch
```

### **Step 3: Copy New Files**

```bash
cd frontend

# Create new directories if needed
mkdir -p tests

# Copy new files (from provided archive)
cp /path/to/sprint-0.4.2/lib/errors.ts lib/
cp /path/to/sprint-0.4.2/components/ui/api-status-badge.tsx components/ui/
cp /path/to/sprint-0.4.2/components/ui/loading-spinner.tsx components/ui/
cp /path/to/sprint-0.4.2/components/ui/error-display.tsx components/ui/
cp /path/to/sprint-0.4.2/tests/api.test.ts tests/
cp /path/to/sprint-0.4.2/tests/TESTING.md tests/
cp /path/to/sprint-0.4.2/SPRINT_0.4.2_REPORT.md .
```

### **Step 4: Update Existing Files**

```bash
# Replace updated files
cp /path/to/sprint-0.4.2/lib/api.ts lib/
cp /path/to/sprint-0.4.2/components/layout/header.tsx components/layout/
cp /path/to/sprint-0.4.2/components/mail/mail-list.tsx components/mail/
cp /path/to/sprint-0.4.2/components/mail/analyzer-view.tsx components/mail/
cp /path/to/sprint-0.4.2/components/mail/stats-cards.tsx components/mail/
cp /path/to/sprint-0.4.2/app/dashboard/page.tsx app/dashboard/
cp /path/to/sprint-0.4.2/README_FRONTEND.md .
```

### **Step 5: Install Dependencies** (if any new)

```bash
# Check if package.json changed
# If yes, install dependencies:
npm install
```

### **Step 6: Test Locally**

#### **6.1: Start Backend**

```bash
# In separate terminal
cd ../backend/api
uvicorn main:app --reload --port 8000

# Verify backend is running
curl http://localhost:8000/api/v1/health
```

#### **6.2: Start Frontend**

```bash
cd frontend

# Create .env.local if not exists
cp .env.example .env.local

# Start dev server
npm run dev
```

#### **6.3: Manual Testing**

Open browser: `http://localhost:3000`

**Check:**
- ✅ API status badge in header shows "Online" (green)
- ✅ Dashboard loads without errors
- ✅ Email list displays real emails from backend
- ✅ AI analysis panel shows real analysis
- ✅ Stats cards display real numbers
- ✅ No console errors

**Test Error Handling:**
- Stop backend
- Refresh page
- ✅ API status badge turns "Offline" (red)
- ✅ Error messages appear with "Try Again" buttons
- ✅ No app crashes

**Test Recovery:**
- Start backend
- Click "Try Again" buttons
- ✅ Data loads successfully
- ✅ API status badge turns "Online" (green)

---

## 🧪 Run Tests

```bash
cd frontend

# Run all tests
npm test

# Run API tests specifically
npm test tests/api.test.ts

# Expected: All tests pass
```

---

## 📝 Git Commit

### **Step 7: Stage Changes**

```bash
cd /path/to/solarmail

# Check status
git status

# Stage new files
git add frontend/lib/errors.ts
git add frontend/components/ui/api-status-badge.tsx
git add frontend/components/ui/loading-spinner.tsx
git add frontend/components/ui/error-display.tsx
git add frontend/tests/api.test.ts
git add frontend/tests/TESTING.md
git add frontend/SPRINT_0.4.2_REPORT.md

# Stage updated files
git add frontend/lib/api.ts
git add frontend/components/layout/header.tsx
git add frontend/components/mail/mail-list.tsx
git add frontend/components/mail/analyzer-view.tsx
git add frontend/components/mail/stats-cards.tsx
git add frontend/app/dashboard/page.tsx
git add frontend/README_FRONTEND.md

# Verify staged files
git diff --staged --name-only
```

### **Step 8: Commit**

```bash
git commit -m "feat: Sprint 0.4.2 - API Integration

- Add real API integration with FastAPI backend
- Implement API client with error handling (lib/api.ts, lib/errors.ts)
- Add API status monitoring (ApiStatusBadge component)
- Implement loading states (LoadingSpinner component)
- Add error display with retry functionality
- Update all components to use real API data:
  - MailList: real emails from backend
  - AnalyzerView: real AI analysis results
  - StatsCards: real statistics
  - Header: API status badge
- Add comprehensive test suite (tests/api.test.ts)
- Add testing documentation (tests/TESTING.md)
- Update README_FRONTEND.md for v0.4.2
- Add Sprint 0.4.2 report

Features:
- ✅ Real-time API connection monitoring
- ✅ Loading spinners during API calls
- ✅ Error handling with retry buttons
- ✅ Type-safe API client
- ✅ Timeout protection (10s)
- ✅ Validation for all inputs

Sprint: 0.4.2
Version: Frontend v0.4.2
Status: API Integration Complete"
```

### **Step 9: Push to GitHub**

```bash
git push origin feature/sprint-0.4.2-api-integration
```

---

## 🔍 Verification

### **On GitHub:**

1. Visit: https://github.com/Solarpaletten/solarmail
2. Check branch: `feature/sprint-0.4.2-api-integration`
3. Verify all files are present:
   - New files: 7 files
   - Updated files: 7 files
4. Review changes in diff view

---

## 📋 Create Pull Request

### **Step 10: Create PR**

1. Go to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Base: `main` ← Compare: `feature/sprint-0.4.2-api-integration`

**PR Title:**
```
feat: Sprint 0.4.2 - API Integration (Frontend ↔ Backend)
```

**PR Description:**

```markdown
## 🎯 Sprint 0.4.2 - API Integration

This PR integrates the Next.js Frontend with the FastAPI Backend, replacing all mock data with real API calls.

### ✅ Changes

**New Features:**
- ✅ Real API integration with comprehensive error handling
- ✅ API status monitoring (live connection indicator)
- ✅ Loading states for all async operations
- ✅ Error display with retry functionality
- ✅ Type-safe API client with validation

**Updated Components:**
- ✅ MailList: displays real emails from backend
- ✅ AnalyzerView: shows real AI analysis results
- ✅ StatsCards: calculates real statistics
- ✅ Header: includes API status badge

**Testing:**
- ✅ Comprehensive API test suite
- ✅ Manual testing guide
- ✅ All tests passing

**Documentation:**
- ✅ Updated README_FRONTEND.md
- ✅ Added SPRINT_0.4.2_REPORT.md
- ✅ Added tests/TESTING.md

### 📊 Files Changed

- **New files:** 7
- **Updated files:** 7
- **Total changes:** ~2,500 lines

### 🧪 Testing

**Manual testing completed:**
- ✅ API connection monitoring works
- ✅ Real data displays correctly
- ✅ Loading states appear
- ✅ Error handling works
- ✅ Retry functionality works

**Automated tests:**
- ✅ All API client tests passing
- ✅ 20+ test cases

### 🚀 Deployment Notes

**Backend must be running on:**
```
http://localhost:8000
```

**Frontend env variable:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 📸 Screenshots

(Attach screenshots showing:)
1. Dashboard with real data
2. API status badge (online/offline)
3. Loading states
4. Error handling

### ✅ Checklist

- [x] Code follows project conventions
- [x] All tests passing
- [x] Documentation updated
- [x] Manual testing completed
- [x] No console errors
- [x] Ready for review

### 👥 Reviewers

@Dashka

---

**Sprint:** 0.4.2  
**Status:** ✅ Ready for Review  
**Version:** Frontend v0.4.2
```

### **Step 11: Request Review**

1. Assign reviewers (Dashka)
2. Add labels: `enhancement`, `sprint-0.4.2`
3. Link to Sprint report in PR

---

## ✅ Post-Merge Checklist

After PR is approved and merged:

```bash
# Switch to main
git checkout main

# Pull latest
git pull origin main

# Verify changes
git log --oneline -5

# Tag release
git tag -a v0.4.2-frontend -m "Frontend v0.4.2 - API Integration"
git push origin v0.4.2-frontend

# Clean up feature branch (optional)
git branch -d feature/sprint-0.4.2-api-integration
```

---

## 🐛 Troubleshooting

### **Issue: Merge Conflicts**

```bash
# Update feature branch with latest main
git checkout feature/sprint-0.4.2-api-integration
git fetch origin
git merge origin/main

# Resolve conflicts
# ... edit conflicted files

git add .
git commit -m "fix: resolve merge conflicts"
git push origin feature/sprint-0.4.2-api-integration
```

### **Issue: Tests Failing**

```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# Clear cache and reinstall
rm -rf node_modules package-lock.json .next
npm install

# Run tests again
npm test
```

### **Issue: Build Errors**

```bash
# Check TypeScript errors
npm run build

# Fix errors and rebuild
```

---

## 📞 Support

If issues arise:
1. Check console for errors
2. Verify backend is running
3. Check `tests/TESTING.md` for troubleshooting
4. Review `SPRINT_0.4.2_REPORT.md` for details
5. Contact Dashka or Claude for support

---

## 🎉 Success Criteria

**Integration is successful when:**
- ✅ All files committed to GitHub
- ✅ Branch pushed successfully
- ✅ Pull request created
- ✅ All tests passing
- ✅ Manual testing completed
- ✅ Documentation reviewed
- ✅ Ready for Dashka's review

---

**Created by:** Claude (AI Engineer)  
**For:** Leanid (Архитектор)  
**Sprint:** 0.4.2 - API Integration  
**Date:** October 26, 2025
