# Finance Analytics Backend

AI-powered Financial Analytics Backend for processing and analyzing financial data with natural language query capabilities.

## Features

- **File Upload**: Upload CSV and Excel files for analysis
- **AI-Powered Analysis**: Automatic schema analysis and KPI generation using OpenAI
- **Conversational Queries**: Natural language to SQL query generation
- **Dashboard**: Comprehensive financial metrics and insights
- **Security**: File validation, size limits, and security headers
- **Production Ready**: Environment validation, structured logging, and comprehensive error handling

## Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **Database**: DuckDB (analytical), SQLite (metadata)
- **AI**: OpenAI GPT-3.5-turbo
- **Data Processing**: Pandas, OpenPyXL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Prerequisites

- Python 3.10 or higher
- pip package manager
- OpenAI API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Pragati1466/finance_backend.git
cd finance_backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# Application Settings
APP_NAME=Finance Analytics Backend
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

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
```

### 5. Create required directories

```bash
mkdir -p uploads data
```

## Running the Application

### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check

```bash
GET /api/v1/health/
```

Returns the health status of the application and its dependencies.

### Version Information

```bash
GET /api/v1/health/version
```

Returns the current version and build information.

### File Upload

```bash
POST /api/v1/upload/
Content-Type: multipart/form-data
```

Upload a CSV or Excel file for analysis.

**Request:**
```json
{
  "file": <binary file>
}
```

**Response:**
```json
{
  "dataset_id": "uuid",
  "status": "uploading",
  "message": "File uploaded successfully"
}
```

### Dashboard

```bash
GET /api/v1/dashboard/{dataset_id}
```

Get comprehensive dashboard with schema, relationships, and KPIs for a dataset.

**Response:**
```json
{
  "dataset_id": "uuid",
  "schema": [...],
  "relationships": [...],
  "financial_context": "...",
  "kpis": [...],
  "execution_status": "success",
  "generated_at": "2024-01-01T00:00:00Z"
}
```

### Conversational Query

```bash
POST /api/v1/query
Content-Type: application/json
```

Ask natural language questions about your data.

**Request:**
```json
{
  "question": "Show me the trend of our top 3 expenses over time",
  "dataset_id": "uuid"
}
```

**Response:**
```json
{
  "question": "...",
  "generated_sql": "SELECT ...",
  "query_result": {
    "success": true,
    "row_count": 10,
    "data": [...]
  },
  "validation": {
    "passed": true,
    "message": "Validation passed"
  },
  "explanation": "The query returned 10 results..."
}
```

## Project Structure

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
├── schemas/                     # Pydantic schemas
├── services/                    # Business logic layer
├── tests/                       # Test suite
│   ├── fixtures/                # Test fixtures
│   ├── integration/             # Integration tests
│   └── unit/                    # Unit tests
├── utils/                       # Utility functions
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Security Features

- **File Validation**: MIME type detection and content validation
- **Size Limits**: Configurable file size limits per type
- **Security Headers**: XSS protection, content security policy
- **CORS Configuration**: Environment-specific CORS settings
- **SQL Injection Prevention**: Query validation and sanitization
- **Environment Validation**: Startup environment checks

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_NAME` | Application name | Finance Analytics Backend | No |
| `APP_VERSION` | Application version | 1.0.0 | No |
| `DEBUG` | Debug mode | False | No |
| `ENVIRONMENT` | Environment (development/staging/production) | development | No |
| `HOST` | Server host | 0.0.0.0 | No |
| `PORT` | Server port | 8000 | No |
| `MAX_FILE_SIZE_MB` | Maximum file size in MB | 100 | No |
| `UPLOAD_DIR` | Upload directory | ./uploads | No |
| `ALLOWED_FILE_TYPES` | Allowed file extensions | csv,xlsx,xls | No |
| `DUCKDB_DATABASE_PATH` | DuckDB database path | ./data/finance.duckdb | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `OPENAI_API_KEY` | OpenAI API key | None | Yes (for AI features) |

## Development

### Running Tests

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

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t finance-analytics-backend .

# Run container
docker run -p 8000:8000 --env-file .env finance-analytics-backend
```

### Production Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Configure allowed CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up database backups
- [ ] Configure OpenAI API key
- [ ] Review and update security headers
- [ ] Set up CI/CD pipeline

## Troubleshooting

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, email support@finance-analytics.com or open an issue on GitHub.

## Version

Current version: 1.0.0
Build date: July 3, 2026 at 7:14 PM
