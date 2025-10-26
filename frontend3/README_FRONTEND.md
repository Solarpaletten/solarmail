# 🌞 SolarMail Frontend

**Version:** 0.4.2  
**Sprint:** API Integration Complete

AI-powered email analysis interface built with Next.js 14, TypeScript, Tailwind CSS, and shadcn/ui.

---

## 🎯 Overview

SolarMail Frontend provides a modern, responsive user interface for managing and analyzing emails with AI-powered insights, fully integrated with FastAPI backend.

### **Key Features:**
- 📊 Real-time email dashboard with live data
- 🧠 AI analysis visualization (sentiment, priority, entities)
- 📧 Email list with smart categorization
- 🔌 Live API connection monitoring
- ⚡ Loading states and error handling
- 🎨 Beautiful, responsive UI with Tailwind CSS
- 🌓 Dark mode support (planned)
- 📱 Mobile-friendly design

---

## 🏗️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui + Radix UI
- **Icons:** Lucide React
- **Date Handling:** date-fns
- **API Integration:** Native Fetch with error handling

---

## 🆕 What's New in v0.4.2

### **API Integration Complete! ✅**

- ✅ Real data from FastAPI backend
- ✅ API connection status indicator
- ✅ Loading states for all async operations
- ✅ Comprehensive error handling
- ✅ Retry functionality
- ✅ Test suite for API client

---

## 📁 Project Structure

```
frontend/
├── app/                           # Next.js 14 App Router
│   ├── dashboard/                # Dashboard page & layout
│   │   ├── layout.tsx           # Dashboard layout with sidebar
│   │   └── page.tsx             # Main dashboard page
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page (redirects to dashboard)
│   └── globals.css              # Global styles & Tailwind
│
├── components/
│   ├── ui/                       # shadcn/ui + custom components
│   │   ├── button.tsx           # Button component
│   │   ├── card.tsx             # Card component
│   │   ├── badge.tsx            # Badge component
│   │   ├── api-status-badge.tsx # 🆕 API status indicator
│   │   ├── loading-spinner.tsx  # 🆕 Loading components
│   │   └── error-display.tsx    # 🆕 Error UI components
│   │
│   ├── layout/                   # Layout components
│   │   ├── header.tsx           # Top navigation bar
│   │   └── sidebar.tsx          # Side navigation menu
│   │
│   └── mail/                     # Email-specific components
│       ├── mail-list.tsx        # Email list view (real data)
│       ├── analyzer-view.tsx    # AI analysis panel (real data)
│       └── stats-cards.tsx      # Statistics cards (real data)
│
├── lib/
│   ├── utils.ts                  # Utility functions
│   ├── api.ts                    # 🆕 API client for backend
│   └── errors.ts                 # 🆕 Custom error types
│
├── tests/                         # 🆕 Test suite
│   ├── api.test.ts               # API client tests
│   └── TESTING.md                # Testing guide
│
├── public/                        # Static assets
├── styles/                        # Additional styles (if needed)
│
├── package.json                   # Dependencies
├── tsconfig.json                  # TypeScript config
├── tailwind.config.ts             # Tailwind configuration
├── next.config.js                 # Next.js configuration
├── .eslintrc.json                 # ESLint rules
├── .prettierrc                    # Prettier config
├── .env.example                   # Environment variables template
├── README_FRONTEND.md             # This file
└── SPRINT_0.4.2_REPORT.md        # 🆕 Sprint report
```

---

## 🚀 Getting Started

### **Prerequisites**
- Node.js 18.0.0 or higher
- npm 9.0.0 or higher
- **Backend API running** on `http://localhost:8000`

### **Installation**

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env.local
   ```

4. **Configure API URL:**
   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Start backend first:**
   ```bash
   # In separate terminal
   cd backend/api
   uvicorn main:app --reload --port 8000
   ```

6. **Run development server:**
   ```bash
   npm run dev
   ```

7. **Open browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

---

## 📦 Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Format code
npm run format

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

---

## 🔌 API Integration

### **API Client**

Located in `lib/api.ts`, provides type-safe methods to interact with backend:

```typescript
import { api } from "@/lib/api";

// Health check
const isOnline = await api.ping();

// Get emails
const emails = await api.getEmails(20);

// Analyze email
const analysis = await api.analyzeEmail(
  "Meeting Tomorrow",
  "Hi team, let's meet at 10 AM..."
);

// Get sync status
const status = await api.getSyncStatus("user@example.com");

// Trigger sync
const result = await api.triggerSync();
```

### **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Backend health status |
| `/api/v1/emails` | GET | Get email list |
| `/api/v1/emails/:id` | GET | Get email by ID |
| `/api/v1/analyze` | POST | Analyze email content |
| `/api/v1/sync/status` | GET | Get sync status |
| `/api/v1/sync/trigger` | POST | Trigger email sync |

### **Error Handling**

The API client includes comprehensive error handling:

```typescript
import { APIError, NetworkError, TimeoutError } from "@/lib/errors";

try {
  const emails = await api.getEmails();
} catch (error) {
  if (error instanceof NetworkError) {
    // Handle network errors
  } else if (error instanceof TimeoutError) {
    // Handle timeouts
  } else if (error instanceof APIError) {
    // Handle API errors
  }
}
```

### **Loading States**

Components use loading spinners during API calls:

```typescript
import { LoadingSpinner } from "@/components/ui/loading-spinner";

if (loading) {
  return <LoadingSpinner size="lg" label="Loading..." />;
}
```

### **API Status Monitor**

The `ApiStatusBadge` component monitors backend connectivity:
- 🟢 Green "Online" when API is reachable
- 🔴 Red "Offline" when API is down
- Auto-checks every 30 seconds

---

## 🎨 UI Components

### **Layout Components**

#### **Header**
Top navigation bar with logo, API status, and action buttons.
```tsx
import { Header } from "@/components/layout/header";
```

#### **Sidebar**
Side navigation menu with links to different sections.
```tsx
import { Sidebar } from "@/components/layout/sidebar";
```

### **Mail Components**

#### **MailList**
Displays list of emails from API with real-time data.
```tsx
import { MailList } from "@/components/mail/mail-list";
```

**Features:**
- Real data from API
- Loading spinner
- Error handling with retry
- Empty state for no emails

#### **AnalyzerView**
Shows AI analysis results from backend.
```tsx
import { AnalyzerView } from "@/components/mail/analyzer-view";
```

**Features:**
- Real-time AI analysis
- Sentiment, priority, category
- Detected entities and keywords
- Progress bars for scores
- Model info and processing time

#### **StatsCards**
Dashboard statistics calculated from API data.
```tsx
import { StatsCards } from "@/components/mail/stats-cards";
```

**Features:**
- Real-time email count
- Calculated statistics
- Trend indicators
- Loading states

### **Utility Components**

#### **ApiStatusBadge**
Connection status indicator.
```tsx
import { ApiStatusBadge } from "@/components/ui/api-status-badge";
```

#### **LoadingSpinner**
Loading state indicator.
```tsx
import { LoadingSpinner } from "@/components/ui/loading-spinner";
```

#### **ErrorDisplay**
Error message with retry functionality.
```tsx
import { ErrorDisplay } from "@/components/ui/error-display";
```

---

## 🧪 Testing

### **Running Tests**

```bash
# Run all tests
npm test

# Run API tests
npm test tests/api.test.ts

# Run with coverage
npm test -- --coverage
```

### **Manual Testing**

See `tests/TESTING.md` for comprehensive testing guide including:
- API integration tests
- Error handling tests
- UI/UX tests
- Performance tests
- E2E test scenarios

---

## 🔧 Configuration

### **Environment Variables**

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### **API Configuration**

The API client automatically uses:
- Base URL from environment or `http://localhost:8000`
- API version path: `/api/v1`
- Timeout: 10 seconds
- Automatic retry: Available via UI

---

## 📱 Pages & Routes

| Route | Description | Status |
|-------|-------------|--------|
| `/` | Home (redirects to dashboard) | ✅ Complete |
| `/dashboard` | Main dashboard view | ✅ Complete |
| `/inbox` | Inbox view | ⏳ Planned |
| `/sent` | Sent emails | ⏳ Planned |
| `/archive` | Archived emails | ⏳ Planned |
| `/trash` | Trash | ⏳ Planned |
| `/settings` | Settings page | ⏳ Planned |

---

## 🎨 Styling & Theming

### **Tailwind Configuration**

Custom colors defined in `tailwind.config.ts`:

```typescript
// SolarMail brand colors
solar: {
  50: '#fffbeb',
  500: '#f59e0b',
  900: '#78350f',
}
```

### **Custom Classes**

```css
.solar-gradient { /* Solar brand gradient */ }
.email-card { /* Email card styling */ }
.analyzer-badge { /* Analysis badge */ }
```

---

## 🚀 Deployment

### **Build for Production**

```bash
npm run build
npm start
```

### **Environment Variables for Production**

```env
NEXT_PUBLIC_API_URL=https://api.solarmail.com
```

### **Vercel Deployment**

1. Push to GitHub
2. Import project in Vercel
3. Configure `NEXT_PUBLIC_API_URL` environment variable
4. Deploy

---

## 📊 Current Features

### ✅ Implemented (v0.4.2)
- [x] Project structure
- [x] Next.js 14 App Router
- [x] TypeScript configuration
- [x] Tailwind CSS + shadcn/ui
- [x] Layout components
- [x] Real API integration
- [x] Email list with real data
- [x] AI analyzer with real analysis
- [x] Statistics cards
- [x] API status monitoring
- [x] Loading states
- [x] Error handling
- [x] Retry functionality
- [x] Test suite

### ⏳ Planned (Sprint 0.4.3+)
- [ ] React Query for caching
- [ ] WebSocket for real-time updates
- [ ] Email detail view
- [ ] Search functionality
- [ ] Filtering by category/priority
- [ ] Pagination
- [ ] Dark mode toggle
- [ ] Settings page
- [ ] Authentication
- [ ] Mobile responsive improvements

---

## 🐛 Troubleshooting

### **Backend Connection Issues**

```bash
# Verify backend is running
curl http://localhost:8000/api/v1/health

# Expected response:
{"status": "healthy", "version": "0.3.2"}
```

### **API Status Always Offline**

1. Check backend is running on port 8000
2. Verify CORS is configured in backend
3. Check `NEXT_PUBLIC_API_URL` in `.env.local`
4. Check browser console for errors

### **No Data Displaying**

1. Verify backend database has data
2. Check browser console for API errors
3. Look for error messages in UI
4. Try clicking "Try Again" buttons

### **Build Errors**

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

---

## 📝 Version History

- **v0.4.2** (Current) - API Integration
  - Real API integration with backend
  - Loading states and error handling
  - API status monitoring
  - Comprehensive test suite

- **v0.4.1** - Initial frontend structure
  - Next.js 14 setup
  - Basic UI components
  - Dashboard layout
  - Mock data implementation

---

## 👥 Team

**Created by SolarMail Team:**
- Leanid (Архитектор)
- Dashka (Senyor Инженер)
- Claude (AI Engineer)

---

## 📄 License

Internal project - SolarMail Team

---

## 🔗 Related Documentation

- [Sprint 0.4.2 Report](./SPRINT_0.4.2_REPORT.md)
- [Testing Guide](./tests/TESTING.md)
- [API Client Documentation](./lib/api.ts)
- [Backend API Documentation](../backend/api/README.md)

---

**Last Updated:** Sprint 0.4.2 - October 26, 2025  
**Status:** ✅ API Integration Complete

frontend3