# 🌞 SolarMail Frontend

**Sprint 0.4.1** - Frontend Structure & UI Layer

AI-powered email analysis interface built with Next.js 14, TypeScript, Tailwind CSS, and shadcn/ui.

---

## 🎯 Overview

SolarMail Frontend provides a modern, responsive user interface for managing and analyzing emails with AI-powered insights.

### **Key Features:**
- 📊 Real-time email dashboard
- 🧠 AI analysis visualization
- 📧 Email list with smart categorization
- 🎨 Beautiful, responsive UI with Tailwind CSS
- 🌓 Dark mode support (coming soon)
- 📱 Mobile-friendly design

---

## 🏗️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui + Radix UI
- **Icons:** Lucide React
- **Date Handling:** date-fns

---

## 📁 Project Structure

```
frontend/
├── app/                      # Next.js 14 App Router
│   ├── dashboard/           # Dashboard page & layout
│   │   ├── layout.tsx      # Dashboard layout with sidebar
│   │   └── page.tsx        # Main dashboard page
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page (redirects to dashboard)
│   └── globals.css         # Global styles & Tailwind
│
├── components/
│   ├── ui/                  # shadcn/ui base components
│   │   ├── button.tsx      # Button component
│   │   ├── card.tsx        # Card component
│   │   └── badge.tsx       # Badge component
│   │
│   ├── layout/              # Layout components
│   │   ├── header.tsx      # Top navigation bar
│   │   └── sidebar.tsx     # Side navigation menu
│   │
│   └── mail/                # Email-specific components
│       ├── mail-list.tsx   # Email list view
│       ├── analyzer-view.tsx  # AI analysis panel
│       └── stats-cards.tsx    # Statistics cards
│
├── lib/
│   ├── utils.ts            # Utility functions
│   └── api.ts              # API client for backend
│
├── public/                  # Static assets
├── styles/                  # Additional styles (if needed)
│
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── tailwind.config.ts      # Tailwind configuration
├── next.config.js          # Next.js configuration
├── .eslintrc.json          # ESLint rules
├── .prettierrc             # Prettier config
├── .env.example            # Environment variables template
└── README_FRONTEND.md      # This file
```

---

## 🚀 Getting Started

### **Prerequisites**
- Node.js 18.0.0 or higher
- npm 9.0.0 or higher
- Backend API running on `http://localhost:8000` (or configure in `.env`)

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

4. **Configure API URL (optional):**
   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Run development server:**
   ```bash
   npm run dev
   ```

6. **Open browser:**
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
```

---

## 🎨 UI Components

### **Layout Components**

#### **Header**
Top navigation bar with logo and action buttons.
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
Displays a list of emails with metadata and AI categories.
```tsx
import { MailList } from "@/components/mail/mail-list";
```

#### **AnalyzerView**
Shows AI analysis results for selected email.
```tsx
import { AnalyzerView } from "@/components/mail/analyzer-view";
```

#### **StatsCards**
Dashboard statistics cards showing email metrics.
```tsx
import { StatsCards } from "@/components/mail/stats-cards";
```

---

## 🔌 API Integration

### **API Client Usage**

```typescript
import { api } from "@/lib/api";

// Health check
const health = await api.healthCheck();

// Get emails
const emails = await api.getEmails(20);

// Analyze email
const analysis = await api.analyzeEmail(
  "Meeting Tomorrow",
  "Hi team, let's meet tomorrow at 10 AM..."
);

// Get sync status
const status = await api.getSyncStatus("user@example.com");

// Trigger sync
const result = await api.triggerSync();
```

### **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/emails` | GET | Get email list |
| `/api/emails/:id` | GET | Get email by ID |
| `/api/analyze` | POST | Analyze email content |
| `/api/sync/status` | GET | Get sync status |
| `/api/sync/trigger` | POST | Trigger email sync |

---

## 🎨 Styling & Theming

### **Tailwind Configuration**

Custom colors and themes defined in `tailwind.config.ts`:

```typescript
// SolarMail brand colors
solar: {
  50: '#fffbeb',
  500: '#f59e0b',
  900: '#78350f',
}
```

### **CSS Variables**

Theme colors use CSS variables for easy customization:

```css
:root {
  --primary: 38 92% 50%;
  --background: 0 0% 100%;
  /* ... more variables */
}
```

### **Custom Classes**

```css
.solar-gradient { /* Solar brand gradient */ }
.email-card { /* Email card styling */ }
.analyzer-badge { /* Analysis badge */ }
```

---

## 📱 Pages & Routes

| Route | Description |
|-------|-------------|
| `/` | Home (redirects to dashboard) |
| `/dashboard` | Main dashboard view |
| `/inbox` | Inbox view (coming soon) |
| `/sent` | Sent emails (coming soon) |
| `/archive` | Archived emails (coming soon) |
| `/trash` | Trash (coming soon) |
| `/settings` | Settings page (coming soon) |

---

## 🧪 Development Guidelines

### **Code Style**
- Use TypeScript for all components
- Follow ESLint + Prettier rules
- Use `"use client"` directive for client components
- Prefer functional components with hooks

### **Component Structure**
```tsx
"use client"; // If client component

import { ... } from "...";

interface ComponentProps {
  // Props definition
}

export function Component({ prop }: ComponentProps) {
  // Component logic
  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

### **File Naming**
- Components: `PascalCase.tsx` or `kebab-case.tsx`
- Utilities: `kebab-case.ts`
- Pages: `page.tsx` (Next.js convention)
- Layouts: `layout.tsx` (Next.js convention)

---

## 🔄 Integration with Backend

### **Current Status**
- ✅ Frontend structure complete
- ✅ Mock data implemented
- ⏳ API integration ready (awaiting backend deployment)
- ⏳ Real-time data fetching (to be implemented)

### **Next Steps (Sprint 0.4.2)**
1. Replace mock data with real API calls
2. Implement real-time updates
3. Add error handling and loading states
4. Add authentication flow
5. Implement email detail view
6. Add search and filtering

---

## 🛠️ Configuration Files

### **TypeScript (`tsconfig.json`)**
- Strict mode enabled
- Path aliases configured (`@/*`)
- Next.js plugin enabled

### **ESLint (`.eslintrc.json`)**
- Next.js recommended rules
- TypeScript support

### **Prettier (`.prettierrc`)**
- 2-space indentation
- Semicolons enabled
- Single quotes disabled

---

## 📊 Current Features

### ✅ Implemented
- [x] Project structure
- [x] Next.js 14 App Router
- [x] TypeScript configuration
- [x] Tailwind CSS + shadcn/ui
- [x] Header component
- [x] Sidebar navigation
- [x] Dashboard layout
- [x] Email list view
- [x] AI analyzer view
- [x] Statistics cards
- [x] Mock data
- [x] API client structure

### ⏳ Planned (Sprint 0.4.2+)
- [ ] Real API integration
- [ ] Authentication
- [ ] Email detail view
- [ ] Search functionality
- [ ] Filtering by category/priority
- [ ] Dark mode toggle
- [ ] Settings page
- [ ] Mobile responsive improvements

---

## 🚀 Deployment

### **Build for Production**
```bash
npm run build
npm start
```

### **Vercel (Recommended)**
1. Push to GitHub
2. Import project in Vercel
3. Configure environment variables
4. Deploy

### **Docker (Alternative)**
```dockerfile
# Dockerfile coming in Sprint 0.4.3
```

---

## 📝 Version History

- **v0.4.1** (Current) - Initial frontend structure
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

**Last Updated:** Sprint 0.4.1 - October 26, 2025

frontend