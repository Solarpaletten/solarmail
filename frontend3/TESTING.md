# 🧪 Testing Guide - Sprint 0.4.2

## Overview

This guide covers testing the API integration between Frontend (Next.js) and Backend (FastAPI).

---

## Prerequisites

**Backend must be running:**
```bash
cd backend/api
uvicorn main:app --reload --port 8000
```

**Frontend must be running:**
```bash
cd frontend
npm run dev
```

---

## Manual Testing Checklist

### 1. API Connection Status ✅

**Test:** Verify API status badge in header
- **Expected:** Green badge showing "Online" when backend is running
- **Expected:** Red badge showing "Offline" when backend is stopped

**Steps:**
1. Start backend → Check badge is green
2. Stop backend → Check badge turns red (within 30 seconds)
3. Restart backend → Check badge turns green

---

### 2. Email List Component ✅

**Test:** Verify emails are loaded from API

**Steps:**
1. Open http://localhost:3000/dashboard
2. Check "Recent Emails" section
3. **Expected:** Real emails from database (not mock data)
4. **Expected:** Each email shows: sender, subject, preview, date
5. **Expected:** Loading spinner appears briefly on initial load

**Error Test:**
1. Stop backend
2. Refresh page
3. **Expected:** Error message with "Try Again" button appears
4. Start backend
5. Click "Try Again"
6. **Expected:** Emails load successfully

---

### 3. AI Analyzer Component ✅

**Test:** Verify AI analysis works

**Steps:**
1. Check "AI Analysis" panel on dashboard
2. **Expected:** Analysis of first email showing:
   - Sentiment (positive/neutral/negative) with score
   - Priority (high/medium/low) with score
   - Category with confidence
   - Detected entities (persons, organizations, topics)
   - Keywords
3. **Expected:** Progress bars animate to show scores
4. **Expected:** Model name and processing time shown (if available)

**Error Test:**
1. Stop backend
2. Refresh page
3. **Expected:** Error message appears
4. Start backend and retry
5. **Expected:** Analysis loads

---

### 4. Statistics Cards ✅

**Test:** Verify stats are calculated from API data

**Steps:**
1. Check 4 stat cards at top of dashboard
2. **Expected:** "Total Emails" shows actual count from API
3. **Expected:** Other stats show calculated values
4. **Expected:** Numbers update when emails change

---

### 5. Error Handling ✅

**Test Scenarios:**

**Scenario A: Backend Offline**
1. Stop backend
2. Try to access dashboard
3. **Expected:** Errors display with retry buttons
4. **Expected:** No app crashes or blank screens

**Scenario B: Network Timeout**
1. Simulate slow network (browser DevTools)
2. **Expected:** Loading states appear
3. **Expected:** Timeout error after 10 seconds

**Scenario C: Invalid API Response**
1. Modify API to return invalid data (optional)
2. **Expected:** Graceful error handling
3. **Expected:** User sees error message

---

## Automated Testing

### Running Unit Tests

```bash
cd frontend
npm test
```

### Test Coverage

Run tests with coverage report:
```bash
npm test -- --coverage
```

### API Tests

Test API client directly:
```bash
npm test tests/api.test.ts
```

**Expected Results:**
- ✅ Health check passes
- ✅ Email fetching works
- ✅ Email analysis works
- ✅ Sync operations work
- ✅ Error handling works

---

## E2E Testing (Manual)

### Full User Flow Test

**Scenario:** New user visits dashboard

1. **Initial Load**
   - Dashboard loads within 3 seconds
   - API status shows "Online"
   - Loading spinners appear briefly

2. **Data Display**
   - Stats cards show real numbers
   - Email list displays 10 recent emails
   - AI analysis shows for first email

3. **Interaction**
   - Hover over email cards → shadow effect
   - Click email → (future: detail view)

4. **Error Recovery**
   - Stop backend
   - Wait 30 seconds
   - API status changes to "Offline"
   - Error messages appear
   - Start backend
   - Click "Try Again" buttons
   - Data loads successfully

---

## Performance Testing

### Load Time Benchmarks

**Target Metrics:**
- Initial page load: < 3 seconds
- API health check: < 500ms
- Email list fetch: < 2 seconds
- Email analysis: < 3 seconds
- Stats calculation: < 1 second

### Testing Load Times

Use browser DevTools (Network tab):
1. Open DevTools → Network tab
2. Refresh page
3. Check timing for API calls

---

## Browser Testing

Test in multiple browsers:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (if on Mac)

---

## Mobile Testing

Test responsive design:
1. Open DevTools → Toggle device toolbar
2. Test on mobile sizes (375px, 768px, 1024px)
3. **Expected:** Layout adjusts properly
4. **Expected:** All features work on mobile

---

## API Endpoint Testing

### Using curl

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
```

**Get Emails:**
```bash
curl http://localhost:8000/api/v1/emails?limit=5
```

**Analyze Email:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"subject": "Test", "body": "This is a test email"}'
```

**Sync Status:**
```bash
curl "http://localhost:8000/api/v1/sync/status?email=test@example.com"
```

---

## Common Issues & Solutions

### Issue: "Failed to fetch"

**Solution:**
- Check backend is running on port 8000
- Check CORS is enabled in backend
- Verify NEXT_PUBLIC_API_URL in .env.local

### Issue: "Network error"

**Solution:**
- Check firewall settings
- Verify backend is accessible: `curl http://localhost:8000/api/v1/health`
- Check console for detailed errors

### Issue: API status always shows "Offline"

**Solution:**
- Check /api/v1/health endpoint exists
- Verify API version path is correct
- Check browser console for errors

### Issue: Loading spinners never disappear

**Solution:**
- Check backend API is returning valid JSON
- Check for JavaScript errors in console
- Verify API endpoints match backend routes

---

## Test Checklist Summary

```
API Integration:
[ ] API status badge works
[ ] Health check succeeds
[ ] Emails load from API
[ ] AI analysis works
[ ] Stats display correctly

Error Handling:
[ ] Network errors handled
[ ] Timeouts handled
[ ] Invalid responses handled
[ ] Retry functionality works

UI/UX:
[ ] Loading states display
[ ] Error messages clear
[ ] Retry buttons work
[ ] Responsive design works

Performance:
[ ] Page loads < 3 seconds
[ ] API calls complete < 2 seconds
[ ] No memory leaks
[ ] Smooth animations
```

---

## Reporting Issues

When reporting bugs, include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Browser console errors
5. Network tab screenshots
6. Backend logs (if available)

---

**Sprint 0.4.2 Testing Complete!** ✅

All integration tests should pass before merging to main.
