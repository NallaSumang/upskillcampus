# ⚙️ Smart Factory Dashboard — Industrial Asset Management System

A full-stack **Industrial Asset Management System** built as the final assessment project for **UpSkill Campus**. This application provides a real-time dashboard to monitor, manage, and control industrial factory machines — simulating a production-grade smart factory environment.

![Java](https://img.shields.io/badge/Java-17-orange?style=flat-square&logo=openjdk)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.3-green?style=flat-square&logo=springboot)
![React](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)
![H2](https://img.shields.io/badge/Database-H2%20In--Memory-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Performance Testing](#-performance-testing)
- [Screenshots](#-screenshots)
- [Author](#-author)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real-time Dashboard** | Live summary cards showing Total Assets, Running, Maintenance, Offline counts, and Average Uptime |
| **CRUD Operations** | Create, Read, Update, and Delete industrial machines via REST API |
| **Status Management** | Change machine status (RUNNING / MAINTENANCE / OFFLINE) via dropdown |
| **Add New Machines** | Register new factory machines with name, status, and uptime percentage |
| **Remove Machines** | Delete machines from the system with confirmation dialog |
| **Search & Filter** | Search machines by name and filter by status in real-time |
| **Performance Tested** | JUnit test proving the API handles 100+ requests under 200ms average |
| **H2 Console** | Built-in database console for direct SQL inspection |

---

## 🛠 Tech Stack

### Backend
- **Java 17** (Microsoft OpenJDK)
- **Spring Boot 3.2.3** (Spring Web, Spring Data JPA)
- **Lombok** — reduces boilerplate code
- **H2 Database** — in-memory, zero-config database
- **Maven** — build and dependency management

### Frontend
- **React 18** — functional components with hooks
- **Axios** — HTTP client for API communication
- **Tailwind CSS** — utility-first CSS framework
- **Create React App** — project scaffolding

---

## 🏗 Architecture

```
┌─────────────────┐       HTTP (Axios)       ┌─────────────────────┐       JPA/Hibernate       ┌──────────────┐
│                 │  ──────────────────────►  │                     │  ──────────────────────►  │              │
│   React.js      │   GET / POST / PUT / DEL  │   Spring Boot API   │    CRUD Operations        │  H2 Database │
│   Frontend      │  ◄──────────────────────  │   (Port 8080)       │  ◄──────────────────────  │  (In-Memory) │
│   (Port 3000)   │       JSON Response       │                     │       Entity Objects      │              │
└─────────────────┘                           └─────────────────────┘                           └──────────────┘
```

### Data Flow
1. **User interacts** with the React dashboard (click, type, select)
2. **Axios sends** an HTTP request to the Spring Boot REST API
3. **Controller** receives the request and delegates to the **Service** layer
4. **Service** executes business logic and calls the **Repository**
5. **Repository** (Spring Data JPA) performs the SQL operation on the **H2 database**
6. **Response** flows back: Database → Repository → Service → Controller → JSON → React → UI updates

---

## 📁 Project Structure

```
upskillcampus/
├── backend/                          # Spring Boot Backend
│   ├── pom.xml                       # Maven dependencies
│   ├── run.ps1                       # Quick-start script (Windows)
│   ├── mvnw / mvnw.cmd              # Maven Wrapper
│   └── src/
│       ├── main/
│       │   ├── java/com/uct/smartfactory/
│       │   │   ├── IndustrialAssetManagementSystem.java   # Main class
│       │   │   ├── model/
│       │   │   │   └── Asset.java                         # JPA Entity
│       │   │   ├── repository/
│       │   │   │   └── AssetRepository.java               # Data access
│       │   │   ├── service/
│       │   │   │   └── AssetService.java                  # Business logic
│       │   │   └── controller/
│       │   │       └── AssetController.java                # REST endpoints
│       │   └── resources/
│       │       └── application.properties                  # H2 config
│       └── test/
│           └── java/com/uct/smartfactory/controller/
│               └── AssetControllerPerformanceTest.java     # Load test
│
├── frontend/                         # React Frontend
│   ├── package.json                  # npm dependencies
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js                  # Entry point
│       ├── index.css                 # Tailwind imports
│       ├── App.jsx                   # Main dashboard
│       └── components/
│           └── AssetTable.jsx        # Machine table component
│
├── internship_report_sections.md     # Report text (Sections 5 & 6)
├── setup-commands.md                 # Scaffolding commands
└── README.md                         # This file
```

---

## 🚀 Getting Started

### Prerequisites
- **Java 17+** (JDK, not JRE)
- **Node.js 16+** and **npm**

### 1. Clone the Repository
```bash
git clone https://github.com/NallaSumang/upskillcampus.git
cd upskillcampus
```

### 2. Start the Backend
```bash
cd backend

# On Windows (recommended):
.\run.ps1

# Or manually:
# Set JAVA_HOME to your JDK 17 path first
.\mvnw spring-boot:run
```
The API will be available at **http://localhost:8080**

### 3. Start the Frontend
```bash
# Open a new terminal
cd frontend
npm install
npm start
```
The dashboard will open at **http://localhost:3000**

### 4. Access the H2 Database Console
Open **http://localhost:8080/h2-console** in your browser:
- JDBC URL: `jdbc:h2:mem:factorydb`
- Username: `sa`
- Password: `password`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/assets` | Retrieve all industrial assets |
| `GET` | `/api/assets/{id}` | Retrieve a single asset by ID |
| `POST` | `/api/assets` | Register a new machine |
| `PUT` | `/api/assets/{id}/status` | Update machine status |
| `DELETE` | `/api/assets/{id}` | Remove a machine |

### Example: Add a New Machine
```bash
curl -X POST http://localhost:8080/api/assets \
  -H "Content-Type: application/json" \
  -d '{"machineName": "3D Printer Unit C", "status": "RUNNING", "uptimePercentage": 91.2}'
```

---

## 📊 Performance Testing

A JUnit 5 test simulates **100 sequential requests** to the `GET /api/assets` endpoint and asserts the average response time is **under 200ms**.

### Run the Test
```bash
cd backend
.\mvnw test -Dtest=AssetControllerPerformanceTest
```

### Results
```
Total Time for 100 requests: 526 ms
Average Time per request:    5.26 ms  ✅ (well under 200ms threshold)

Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

---

## 📸 Screenshots

### Dashboard View
The main dashboard displays all registered factory machines with real-time status indicators, uptime progress bars, and interactive controls.

### Features Demonstrated
- ⚡ Dark-themed responsive UI
- 📊 Summary cards with live statistics
- 🔍 Search and filter functionality
- ➕ Add / 🗑 Delete machine operations
- 🔄 Status dropdown for instant updates

---

## 👤 Author

**Nalla Sumang**
- GitHub: [@NallaSumang](https://github.com/NallaSumang)
- Email: sumangsumang41@gmail.com

---

## 📄 License

This project is part of the **UpSkill Campus Industrial Internship Program** final assessment.

---

> Built with ❤️ for the UpSkill Campus Final Assessment
