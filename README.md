# 🏘️ GramPulse — Village Panchayat Transparency App

> Transparent governance platform for Indian villages — by the Sarpanch, for the people.

---

## 📱 What is GramPulse?

GramPulse is a **mobile-first web application** that brings transparency to Indian village governance. Citizens can track government budgets, monitor ongoing works, read announcements, download official documents, and submit grievances — all from their phone!

---

## 🗂️ Project Structure

```
grampulse/
├── backend/                        ← FastAPI Python backend
│   ├── app/
│   │   ├── main.py                 ← App entry point
│   │   ├── database.py             ← PostgreSQL connection
│   │   ├── config.py               ← Environment config
│   │   ├── models/                 ← Database tables
│   │   │   ├── village.py
│   │   │   ├── user.py
│   │   │   ├── budget.py
│   │   │   ├── project.py
│   │   │   ├── announcement.py
│   │   │   ├── grievance.py
│   │   │   ├── document.py
│   │   │   └── otp.py
│   │   ├── schemas/                ← Pydantic validation
│   │   ├── routers/                ← API endpoints
│   │   │   ├── auth.py
│   │   │   ├── village.py
│   │   │   ├── budget.py
│   │   │   ├── projects.py
│   │   │   ├── announcements.py
│   │   │   ├── grievances.py
│   │   │   └── documents.py
│   │   ├── utils/
│   │   │   ├── auth.py             ← JWT + bcrypt
│   │   │   ├── otp.py              ← OTP generation
│   │   │   ├── cloudinary.py       ← File uploads
│   │   │   ├── permissions.py      ← Role checks
│   │   │   └── logger.py           ← Logging
│   │   └── middleware/
│   │       └── auth_middleware.py  ← Request logging
│   ├── alembic/                    ← DB migrations
│   │   └── versions/
│   │       ├── 001_initial_tables.py
│   │       └── 002_add_otp_table.py
│   ├── create_admin.py             ← Seed first admin
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── alembic.ini
│   └── .env
│
├── frontend/                       ← React.js frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── main.jsx                ← React entry point
│   │   ├── App.jsx                 ← Routes
│   │   ├── index.css               ← Global styles
│   │   ├── api/                    ← Axios API calls
│   │   │   ├── axios.js            ← Base axios setup + interceptors
│   │   │   ├── auth.js
│   │   │   ├── budget.js
│   │   │   ├── projects.js
│   │   │   ├── announcements.js
│   │   │   ├── grievances.js
│   │   │   └── documents.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx     ← Global auth state
│   │   ├── pages/
│   │   │   ├── Landing.jsx         ← Public home page
│   │   │   ├── Login.jsx           ← Login + Register + Forgot Password
│   │   │   ├── citizen/            ← Citizen screens
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Announcements.jsx
│   │   │   │   ├── Projects.jsx
│   │   │   │   ├── Budget.jsx
│   │   │   │   ├── Documents.jsx
│   │   │   │   ├── Grievances.jsx
│   │   │   │   ├── NewGrievance.jsx
│   │   │   │   └── Profile.jsx
│   │   │   ├── sarpanch/           ← Sarpanch screens
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── ManageBudget.jsx
│   │   │   │   ├── NewBudget.jsx
│   │   │   │   ├── NewTransaction.jsx
│   │   │   │   ├── ManageProjects.jsx
│   │   │   │   ├── NewProject.jsx
│   │   │   │   ├── ManageAnnouncements.jsx
│   │   │   │   ├── NewAnnouncement.jsx
│   │   │   │   ├── ManageGrievances.jsx
│   │   │   │   └── UploadDocument.jsx
│   │   │   └── admin/              ← Admin screens
│   │   │       ├── Dashboard.jsx
│   │   │       ├── ManageVillages.jsx
│   │   │       ├── ManageUsers.jsx
│   │   │       └── NewUser.jsx
│   │   ├── components/             ← Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── BottomNav.jsx       ← Mobile bottom navigation
│   │   │   ├── BudgetCard.jsx
│   │   │   ├── ProjectCard.jsx
│   │   │   ├── AnnouncementCard.jsx
│   │   │   ├── GrievanceCard.jsx
│   │   │   ├── DocumentCard.jsx
│   │   │   ├── StatusBadge.jsx
│   │   │   ├── Charts.jsx          ← Pie + Bar charts
│   │   │   ├── Loader.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   └── utils/
│   │       ├── helpers.js          ← Format dates, currency
│   │       └── constants.js        ← Roles, status configs
│   ├── .env
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── Dockerfile
│
├── docker-compose.yml              ← Runs everything together
└── README.md                       ← This file
```

---

## 👥 User Roles

| Role | What They Can Do |
|---|---|
| **Admin** | Create villages, register sarpanch/ward members, manage all users |
| **Sarpanch** | Publish budgets, projects, announcements, reply to grievances, upload documents |
| **Ward Member** | Create and update projects for their ward only |
| **Citizen** | View all data, submit grievances, download documents |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **PostgreSQL** | Database |
| **SQLAlchemy** | ORM |
| **Alembic** | Database migrations |
| **JWT + bcrypt** | Authentication |
| **Cloudinary** | File/image storage |

### Frontend
| Technology | Purpose |
|---|---|
| **React.js** | UI framework |
| **Tailwind CSS** | Styling |
| **Axios** | API calls |
| **React Router v6** | Navigation |
| **Recharts** | Budget charts |
| **React Toastify** | Notifications |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional but recommended)

---

### 🐳 Option 1 — Run with Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/yourname/grampulse.git
cd grampulse

# Copy env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit backend/.env with your credentials
# Then run everything
docker-compose up --build
```

That's it! Everything starts automatically ✅

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

---

### 🐍 Option 2 — Run Manually

#### Backend Setup

```bash
# Go to backend folder
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.example .env
# Edit .env with your DB credentials

# Run database migrations
alembic upgrade head

# Create first admin user
python create_admin.py

# Start backend server
uvicorn app.main:app --reload
```

Backend runs at → http://localhost:8000

#### Frontend Setup

```bash
# Go to frontend folder
cd frontend

# Install dependencies
npm install

# Setup .env
cp .env.example .env
# Edit VITE_API_URL if needed

# Start frontend
npm run dev
```

Frontend runs at → http://localhost:3000

---

## 🔐 Environment Variables

### Backend `.env`

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/panchayat_db
SECRET_KEY=your-super-secret-key-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Frontend `.env`

```env
VITE_API_URL=http://localhost:8000/api
```

---

## 🚀 First Time Setup Flow

```
Step 1 → Run migrations
         alembic upgrade head

Step 2 → Create admin
         python create_admin.py
         Admin phone: 9999999999
         Admin password: Admin@123

Step 3 → Login as admin at /login

Step 4 → Create village at /admin/villages

Step 5 → Register Sarpanch at /admin/users/new

Step 6 → Sarpanch logs in and starts publishing

Step 7 → Citizens register and start using the app ✅
```

---

## 📡 API Endpoints

### Auth
```
POST /api/auth/register           → Citizen register
POST /api/auth/login              → Login
POST /api/auth/forgot-password    → Request OTP
POST /api/auth/reset-password     → Reset password with OTP
GET  /api/auth/me                 → Get my profile
```

### Villages
```
GET    /api/villages/             → All villages (public)
POST   /api/villages/             → Create village (admin)
PATCH  /api/villages/{id}         → Update village (admin)
DELETE /api/villages/{id}         → Delete village (admin)
```

### Budget
```
GET  /api/budget/?village_id=1           → All budgets (public)
GET  /api/budget/{id}/summary            → Budget breakdown (public)
POST /api/budget/                        → Create budget (sarpanch)
POST /api/budget/transaction             → Add spending (sarpanch)
```

### Projects
```
GET   /api/projects/?village_id=1        → All projects (public)
POST  /api/projects/                     → Create project (sarpanch)
PATCH /api/projects/{id}/status          → Update status
POST  /api/projects/{id}/upload-photo    → Upload photo
```

### Announcements
```
GET    /api/announcements/?village_id=1  → All announcements (public)
GET    /api/announcements/latest         → Latest 5 (public)
POST   /api/announcements/               → Publish (sarpanch)
DELETE /api/announcements/{id}           → Delete (sarpanch)
```

### Grievances
```
POST  /api/grievances/              → Submit complaint (citizen)
GET   /api/grievances/my            → My complaints (citizen)
GET   /api/grievances/all           → All complaints (sarpanch)
PATCH /api/grievances/all/{id}/reply → Reply (sarpanch)
```

### Documents
```
GET  /api/documents/?village_id=1   → All documents (public)
POST /api/documents/upload           → Upload file (sarpanch)
```

Full interactive docs at → **http://localhost:8000/docs**

---

## 🎨 Design System

| Element | Value |
|---|---|
| Primary Color | `#16a34a` (Green) |
| Secondary Color | `#ea580c` (Orange) |
| Font | Poppins |
| Border Radius | `rounded-2xl` (16px) |
| Shadow | `shadow-sm` cards |
| Mobile Nav | Bottom navigation bar |

---

## 📱 Mobile Features

- Bottom navigation bar (like WhatsApp/GPay)
- Large touch-friendly buttons
- Card-based layout
- Pull to refresh ready
- Works on all screen sizes
- PWA ready (add to home screen)

---

## 🌐 Deployment

### Backend → Render.com (Free)
```
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repo → backend folder
4. Set environment variables
5. Deploy ✅
```

### Database → Supabase (Free PostgreSQL)
```
1. Create account at supabase.com
2. Create new project
3. Copy connection string to DATABASE_URL
4. Run: alembic upgrade head
```

### Frontend → Vercel (Free)
```
1. Push code to GitHub
2. Import project on vercel.com
3. Set VITE_API_URL to your Render backend URL
4. Deploy ✅
```

### Files → Cloudinary (Free 25GB)
```
1. Create account at cloudinary.com
2. Copy Cloud Name, API Key, API Secret
3. Add to backend .env
```

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open Pull Request

---

## 📄 License

MIT License — free to use for any purpose.

---

## 🙏 Made For

This app is built for the **Digital India Initiative** to bring transparency and accountability to village panchayat governance across India. 🇮🇳

> *"जब गाँव जागेगा, तब देश बदलेगा"*
> *("When the village awakens, the nation will change")*

---

**Built with ❤️ for Indian Villages**
