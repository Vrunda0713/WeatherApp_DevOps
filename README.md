#  Nimbus — Weather Dashboard

> A DevOps mini project demonstrating a complete CI/CD pipeline with a real-world Flask application.

Course: 20PECE 601A — DevOps Fundamentals | Sem II, 2025-2026  
Institute: Cummins College of Engineering for Women, Pune.

---

##  Problem Statement

Developers and users need a simple, reliable way to check real-time weather data for any city. This project builds a lightweight weather dashboard and implements a full DevOps lifecycle around it — from version control to automated testing, containerization, and cloud deployment.

---

## Tech Stack

| Layer        | Tool                    |
|--------------|-------------------------|
| Backend      | Python 3.11 + Flask     |
| Frontend     | HTML + CSS + JavaScript |
| Weather API  | OpenWeatherMap (free)   |
| Testing      | Pytest                  |
| Linting      | Flake8                  |
| CI/CD        | GitHub Actions          |
| Container    | Docker                  |
| Deployment   | Render (Staging)        |

---

##  CI/CD Pipeline

```
Push to GitHub
     ↓
GitHub Actions Triggered
     ↓
Install Dependencies (pip)
     ↓
Static Code Analysis (flake8)
     ↓
Unit Tests (pytest)
     ↓
Docker Image Build & Verify
     ↓
Deploy to Render (on main branch)
```

---

##  Getting Started Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/weather-dashboard.git
cd weather-dashboard
```

### 2. Set up environment
```bash
cp .env .env.local
# Edit .env.local and add your OpenWeatherMap API key
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python run.py
```
Visit: http://localhost:5000

---

##  Run with Docker

```bash
docker build -t weather-dashboard .
docker run -p 5000:5000 -e OPENWEATHER_API_KEY=your_key weather-dashboard
```

Or with Docker Compose:
```bash
docker-compose up
```

---

##  Run Tests

```bash
pytest tests/ -v
```

##  Run Linter

```bash
flake8 app/ tests/ run.py --max-line-length=100
```

---

##  Deployment (Render)

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repository
3. Set environment variable: `OPENWEATHER_API_KEY`
4. Add the **Deploy Hook URL** to GitHub Secrets as `RENDER_DEPLOY_HOOK_URL`
5. Every push to `main` will auto-deploy ✅

---

## Team Members

| Member | Role |
|--------|------|
| Member 1 | Flask Backend + API Integration |
| Member 2 | Frontend (HTML/CSS/JS) |
| Member 3 | Docker + GitHub Actions CI/CD |
| Member 4 | Testing (Pytest) + Documentation |

---

##  Rubric Coverage

| Criteria | Implementation |
|----------|---------------|
| Problem Definition | Clear problem statement in README |
| Version Control | Git with branching strategy |
| Automated Build | pip + requirements.txt |
| CI & Testing | GitHub Actions + Pytest (9 tests) |
| Static Analysis | Flake8 in CI pipeline |
| Containerization | Dockerfile + docker-compose.yml |
| Deployment | Render staging via deploy hook |
