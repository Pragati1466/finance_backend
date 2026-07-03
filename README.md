# Finance Analytics Backend

<div align="center">

![Finance Analytics](https://img.shields.io/badge/Finance-Analytics-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-orange)

**AI-powered Financial Analytics Backend for processing and analyzing financial data with natural language query capabilities**

[Live Demo](#deployment) • [API Documentation](#api-documentation) • [Features](#features) • [Getting Started](#getting-started)

</div>

## 📋 Project Overview

Finance Analytics Backend is a production-ready API that enables users to upload financial datasets (CSV/Excel) and interact with them using natural language queries. Powered by OpenAI's GPT-3.5-turbo, it automatically analyzes data schemas, generates key performance indicators (KPIs), and converts natural language questions into SQL queries.

### 🎯 Key Capabilities

- **Zero-Configuration Analysis**: Upload your data and get instant insights
- **Natural Language Queries**: Ask questions in plain English, get SQL results
- **AI-Driven Insights**: Automatic KPI generation and schema analysis
- **Production Ready**: Comprehensive security, logging, and error handling
- **Lightweight Frontend**: Simple HTML/CSS/JS interface for immediate use

## ✨ Features

### Core Functionality
- **📤 File Upload**: Upload CSV and Excel files for analysis
- **🤖 AI-Powered Analysis**: Automatic schema analysis and KPI generation using OpenAI
- **💬 Conversational Queries**: Natural language to SQL query generation
- **📊 Dashboard**: Comprehensive financial metrics and insights
- **🎯 Demo Dataset**: Built-in sample data for immediate testing

### Security & Reliability
- **🔒 Security**: File validation, size limits, and security headers
- **🛡️ CORS Configuration**: Environment-specific CORS settings
- **🔍 SQL Injection Prevention**: Query validation and sanitization
- **📝 Structured Logging**: JSON-formatted logs for production monitoring
- **⚠️ Error Handling**: Comprehensive error responses with detailed context

### Developer Experience
- **📚 API Documentation**: Interactive Swagger UI and ReDoc
- **🧪 Testing**: Unit and integration test suite
- **🔧 Configuration**: Environment-based configuration with Pydantic
- **🚀 Deployment Ready**: Railway, Docker, and cloud deployment support

## 🏗️ Architecture

The application follows a layered architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│              (HTML/CSS/JavaScript)                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│         ┌──────────┬──────────┬──────────┬──────────┐       │
│         │ Upload   │ Dashboard│ Query    │ Health   │       │
│         └──────────┴──────────┴──────────┴──────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                             │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ Dataset      │ Dashboard    │ Query        │            │
│  │ Service      │ Service      │ Service      │            │
│  └──────────────┴──────────────┴──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI Layer                                  │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ Schema       │ KPI          │ Query        │            │
│  │ Analyzer     │ Generator    │ Engine       │            │
│  └──────────────┴──────────────┴──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                 │
│  ┌──────────────┬──────────────┐                            │
│  │ DuckDB       │ SQLite       │                            │
│  │ (Analytics)  │ (Metadata)   │                            │
│  └──────────────┴──────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Folder Structure

```
finance_backend/
├── ai/                          # AI layer components
│   ├── analyzers/               # Schema analysis
│   ├── cache/                   # KPI result caching
│   ├── executors/               # SQL execution
│   ├── generators/              # KPI generation
│   ├── llm/                     # OpenAI client wrapper
│   ├── parsers/                 # LLM response parsing
│   └── prompts/                 # AI prompt templates
├── config/                      # Configuration management
│   ├── logging.py               # Logging configuration
│   ├── settings.py              # Application settings
│   └── validation.py            # Environment validation
├── constants/                   # Application constants
├── core/                        # Core utilities
│   ├── exceptions.py            # Centralized exception handling
│   ├── helpers.py               # Reusable helper functions
│   ├── logging.py               # Logging utilities
│   └── response.py              # API response standardization
├── database/                    # Database management
│   ├── base.py                  # SQLAlchemy base
│   ├── duckdb_manager.py        # DuckDB connection
│   └── sql_executor.py          # Unified SQL executor
├── dependencies/                # Dependency injection
│   ├── container.py             # DI container
│   └── database.py              # Database dependencies
├── exceptions/                  # Custom exceptions
├── frontend/                    # Lightweight frontend
│   ├── index.html               # Main HTML file
│   ├── styles.css               # Styling
│   └── script.js                # JavaScript logic
├── middlewares/                 # FastAPI middleware
├── models/                      # SQLAlchemy models
├── query/                       # Conversational query layer
│   ├── llm_client.py            # Query LLM client
│   ├── prompt_builder.py        # Query prompt builder
│   ├── query_service.py         # Query service
│   ├── response_formatter.py    # Response formatting
│   ├── sql_executor.py          # Query SQL executor
│   └── sql_validator.py         # SQL validation
├── repositories/                # Data access layer
├── routers/                     # API route handlers
├── sample_data/                 # Sample datasets for demo
├── schemas/                     # Pydantic schemas
├── services/                    # Business logic layer
├── tests/                       # Test suite
│   ├── fixtures/                # Test fixtures
│   ├── integration/             # Integration tests
│   └── unit/                    # Unit tests
├── utils/                       # Utility functions
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── railway.json                 # Railway deployment config
├── nixpacks.toml                # Nixpacks configuration
├── Procfile                     # Process file for deployment
├── .env.example                 # Environment template
└── README.md                    # This file
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.10+
- **Data Processing**: Pandas 2.1.4
- **Excel Support**: OpenPyXL 3.1.2
- **ORM**: SQLAlchemy 2.0.25
- **Validation**: Pydantic 2.5.3

### Databases
- **Analytical**: DuckDB 0.9.2
- **Metadata**: SQLite

### AI/ML
- **LLM**: OpenAI GPT-3.5-turbo
- **Client**: OpenAI 1.3.0

### Deployment
- **Platform**: Railway
- **Containerization**: Docker support
- **Process Management**: Uvicorn

### Development
- **Testing**: Pytest
- **Code Quality**: Black, Flake8, MyPy
- **Environment**: python-dotenv

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager
- OpenAI API key (for AI features)

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/Pragati1466/finance_backend.git
cd finance_backend
```

#### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# Application Settings
APP_NAME=Finance Analytics Backend
APP_VERSION=1.0.0
DEBUG=False
ENVIRONMENT=production

# Server Settings
HOST=0.0.0.0
PORT=8000

# File Upload Settings
MAX_FILE_SIZE_MB=100
UPLOAD_DIR=./uploads
ALLOWED_FILE_TYPES=csv,xlsx,xls

# DuckDB Settings
DUCKDB_DATABASE_PATH=./data/finance.duckdb

# Logging Settings
LOG_LEVEL=INFO
LOG_FORMAT=json

# OpenAI Settings
OPENAI_API_KEY=your_openai_api_key_here

# CORS Settings (comma-separated origins, use * for development)
CORS_ORIGINS=*
```

#### 5. Create required directories

```bash
mkdir -p uploads data
```

### Running the Application

#### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

#### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Using the Frontend

Open `frontend/index.html` in your browser to access the web interface.

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

#### Health Check
```bash
GET /api/v1/health/
```
Returns the health status of the application and its dependencies.

#### Load Demo Dataset
```bash
POST /api/v1/upload/demo
```
Load a sample financial dataset for testing without uploading files.

#### File Upload
```bash
POST /api/v1/upload/
Content-Type: multipart/form-data
```
Upload a CSV or Excel file for analysis.

**Response:**
```json
{
  "message": "File uploaded and processed successfully",
  "dataset_id": "uuid",
  "status": "ready"
}
```

#### Dashboard
```bash
GET /api/v1/dashboard/{dataset_id}
```
Get comprehensive dashboard with schema, relationships, and KPIs for a dataset.

**Response:**
```json
{
  "dataset_id": "uuid",
  "schema": {"columns": [...]},
  "relationships": [...],
  "kpis": [...]
}
```

#### Conversational Query
```bash
POST /api/v1/query
Content-Type: application/json
```
Ask natural language questions about your data.

**Request:**
```json
{
  "question": "What is the total revenue?",
  "dataset_id": "uuid"
}
```

**Response:**
```json
{
  "question": "What is the total revenue?",
  "sql_query": "SELECT SUM(revenue) FROM data",
  "results": [...],
  "explanation": "This query calculates total revenue"
}
```

## 🌐 Deployment

### Railway Deployment

1. **Push your code to GitHub**
2. **Create a new Railway project**
3. **Connect your GitHub repository**
4. **Add environment variables in Railway dashboard:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ENVIRONMENT`: production
   - `CORS_ORIGINS`: Your frontend domain
5. **Deploy**

Railway will automatically detect the configuration from `railway.json`, `nixpacks.toml`, and `Procfile`.

### Docker Deployment

```bash
# Build image
docker build -t finance-analytics-backend .

# Run container
docker run -p 8000:8000 --env-file .env finance-analytics-backend
```


## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## 🔧 Development

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Key Error**
- Ensure `OPENAI_API_KEY` is set in `.env` file
- Verify API key has sufficient quota
- Check OpenAI service status

**Database Connection Error**
- Ensure DuckDB database directory exists
- Check file permissions
- Verify database path in configuration

**File Upload Error**
- Check file size limits
- Verify file type is supported
- Ensure upload directory exists and is writable

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new functionality
5. Submit a pull request

## 📊 Version

Current version: 1.0.0
Build date: July 3, 2026

---

<div align="center">

**Built with ❤️ for financial data analytics**

[⬆ Back to Top](#finance-analytics-backend)

</div>
