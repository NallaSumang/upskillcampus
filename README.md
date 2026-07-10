<div align="center">

# ⚙️ Smart Factory Dashboard

### Industrial Asset Management System

A production-grade full-stack application for real-time monitoring, management, and control of industrial factory machines — built with **Python/FastAPI** and **React**.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Testing](#-testing)

</div>

---

## 🎯 Why This Project

This project demonstrates **advanced full-stack engineering** with a focus on:

- **Clean Architecture** — Separation of concerns with dedicated routers, services, and data layers
- **Production Patterns** — Environment-based configuration, custom exception handling, structured error responses
- **API Design** — RESTful endpoints with pagination, filtering, sorting, bulk operations, and Swagger documentation
- **Testing** — Comprehensive pytest suite with isolated test databases and fixtures
- **DevOps** — Docker containerization, docker-compose orchestration, and GitHub Actions CI/CD

---

## ✨ Features

| Category | Feature | Description |
|----------|---------|-------------|
| **Dashboard** | Real-time Statistics | Live cards showing Total Assets, Running, Maintenance, Offline, Avg Uptime |
| **CRUD** | Full Asset Management | Create, Read, Update, Delete factory machines via REST API |
| **Operations** | Bulk Operations | Delete multiple machines in a single request |
| **Filtering** | Search & Filter | Real-time search by name + status filter (RUNNING / MAINTENANCE / OFFLINE) |
| **API** | Pagination & Sorting | Server-side pagination with configurable sort fields and order |
| **Monitoring** | Health Check | `/api/health` endpoint for uptime monitoring and DB connectivity |
| **Docs** | Swagger UI | Interactive API explorer at `/docs` |
| **DevOps** | Docker & CI/CD | One-command deployment + automated testing pipeline |

---

## 🏗 Architecture

```
┌─────────────────┐         HTTP (Axios)         ┌───────────────────────────────────┐
│                 │  ─────────────────────────►   │  FastAPI Application              │
│   React 18      │   GET / POST / PUT / DELETE   │                                   │
│   Frontend      │  ◄─────────────────────────   │  ┌───────────┐  ┌─────────────┐  │     ┌──────────┐
│   (Port 3000)   │         JSON Response         │  │  Routers  │→ │  Services   │──│────►│  SQLite  │
│                 │                               │  └───────────┘  └─────────────┘  │     │    DB    │
└─────────────────┘                               │  ┌───────────┐  ┌─────────────┐  │     └──────────┘
                                                  │  │  Schemas  │  │  Exceptions │  │
                                                  │  └───────────┘  └─────────────┘  │
                                                  └───────────────────────────────────┘
```

### Layered Design

| Layer | Responsibility | Files |
|-------|---------------|-------|
| **Routers** | HTTP request/response handling, input validation | `app/routers/` |
| **Services** | Business logic, data aggregation, query composition | `app/services/` |
| **Models** | Database schema definition (SQLAlchemy ORM) | `app/models.py` |
| **Schemas** | Request/response validation (Pydantic v2) | `app/schemas.py` |
| **Config** | Environment-based settings | `app/config.py` |
| **Exceptions** | Custom error types + structured JSON error handlers | `app/exceptions.py` |

---

## 📁 Project Structure

```
smart-factory-dashboard/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI pipeline
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                 # Pydantic BaseSettings (env-based)
│   │   ├── database.py               # SQLAlchemy engine + session
│   │   ├── models.py                 # ORM models
│   │   ├── schemas.py                # Pydantic request/response schemas
│   │   ├── exceptions.py             # Custom exceptions + handlers
│   │   ├── routers/
│   │   │   ├── assets.py             # Asset CRUD + stats endpoints
│   │   │   └── health.py             # Health check endpoint
│   │   └── services/
│   │       └── asset_service.py      # Business logic layer
│   ├── tests/
│   │   ├── conftest.py               # Test fixtures + isolated DB
│   │   └── test_assets.py            # 24 pytest test cases
│   ├── main.py                       # FastAPI application entrypoint
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Backend container
│   └── .env.example                  # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main dashboard
│   │   └── components/
│   │       └── AssetTable.jsx        # Machine table component
│   ├── package.json
│   └── Dockerfile                    # Frontend container
├── docker-compose.yml                # Full-stack orchestration
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/NallaSumang/Smart-Factory-Dashboard.git
cd Smart-Factory-Dashboard
docker-compose up --build
```

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Start the server
uvicorn main:app --reload
```

> API at **http://localhost:8000** · Swagger at **http://localhost:8000/docs**

#### Frontend

```bash
cd frontend
npm install
npm start
```

> Dashboard at **http://localhost:3000**

---

## 🔌 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/assets` | List all assets (supports `?status=`, `?search=`, `?page=`, `?sort_by=`, `?sort_order=`) |
| `GET` | `/api/assets/stats` | Dashboard statistics (counts + avg uptime) |
| `GET` | `/api/assets/{id}` | Get single asset |
| `POST` | `/api/assets` | Create new machine |
| `PUT` | `/api/assets/{id}/status` | Update machine status |
| `DELETE` | `/api/assets/{id}` | Remove a machine |
| `POST` | `/api/assets/bulk-delete` | Bulk delete by IDs |
| `GET` | `/api/health` | System health check |

### Request Examples

**Create a machine:**
```bash
curl -X POST http://localhost:8000/api/assets \
  -H "Content-Type: application/json" \
  -d '{"machineName": "3D Printer Unit C", "status": "RUNNING", "uptimePercentage": 91.2}'
```

**Filter by status with search:**
```bash
curl "http://localhost:8000/api/assets?status=RUNNING&search=CNC&sort_by=uptime_percentage&sort_order=desc"
```

**Bulk delete:**
```bash
curl -X POST http://localhost:8000/api/assets/bulk-delete \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 3, 5]}'
```

### Error Responses

All errors return structured JSON:

```json
{
  "error": "not_found",
  "message": "Asset with id 999 not found",
  "asset_id": 999
}
```

---

## 🧪 Testing

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

### Test Coverage

| Test Class | Tests | What's Covered |
|-----------|-------|----------------|
| `TestListAssets` | 5 | Empty list, populated list, filter by status, search, no-match |
| `TestGetAsset` | 2 | Existing asset, 404 for missing |
| `TestCreateAsset` | 6 | Success, defaults, empty name, invalid uptime, negative uptime, invalid status |
| `TestUpdateStatus` | 3 | Success, 404, invalid status value |
| `TestDeleteAsset` | 2 | Success + verification, 404 |
| `TestBulkDelete` | 1 | Multi-delete with remaining verification |
| `TestDashboardStats` | 2 | Correct aggregation, empty state |
| `TestHealthCheck` | 1 | Healthy status + DB connectivity |

**Total: 22 test cases**

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI 0.115 | High-performance async Python web framework |
| **ORM** | SQLAlchemy 2.0 | Database abstraction with modern declarative mapping |
| **Validation** | Pydantic v2 | Type-safe request/response serialization |
| **Database** | SQLite | Zero-configuration persistent storage |
| **Server** | Uvicorn | Lightning-fast ASGI server |
| **Frontend** | React 18 | Component-based UI with hooks |
| **HTTP Client** | Axios | Promise-based API communication |
| **Styling** | Tailwind CSS | Utility-first responsive design |
| **Testing** | pytest + httpx | Isolated test suite with fixtures |
| **CI/CD** | GitHub Actions | Automated test + build pipeline |
| **Containers** | Docker + Compose | One-command full-stack deployment |

---

## 👤 Author

**Nalla Sumang**
- GitHub: [@NallaSumang](https://github.com/NallaSumang)
- Email: sumangsumang41@gmail.com

---

## 📄 License

This project is licensed under the MIT License.
