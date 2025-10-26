# ⚡ Frontend3 - Quick Start Guide

**For:** Leanid  
**Time:** 5 minutes  
**Goal:** Test frontend3 and confirm it works

---

## 🚀 Super Quick Start

```bash
# 1. Extract
unzip solarmail-frontend3-v0.4.2-complete.zip

# 2. Replace
cd /path/to/solarmail
mv frontend frontend-backup
mv frontend3 frontend

# 3. Install
cd frontend
npm install

# 4. Configure
cp .env.example .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 5. Start Backend (separate terminal)
cd ../backend/api
uvicorn main:app --reload

# 6. Start Frontend
cd ../frontend
npm run dev

# 7. Open Browser
# http://localhost:3000/dashboard
```

---

## ✅ Check These 3 Things

1. **API Status Badge = Green "Online"** ✅
2. **Email list shows real data** ✅
3. **AI analysis panel works** ✅

---

## ✅ All Good?

```bash
# Yes? Proceed to git
git add frontend/
git commit -m "feat: frontend3 v0.4.2 complete"
git push origin main
```

---

## ❌ Issues?

**Backend not connecting?**
```bash
curl http://localhost:8000/api/v1/health
```

**Frontend errors?**
- Check browser console
- Check `npm install` completed
- Check `.env.local` exists

**Still stuck?**
- Read `FRONTEND3_FINAL_REPORT.md`
- Contact Claude or Dashka

---

**That's it! 🎉**
