# Finance Analytics Backend - Complete Project Structure

## File Responsibilities and Architecture

### Root Directory Files

**main.py**
- Application entry point
- FastAPI application initialization
- Lifespan management (startup/shutdown)
- Middleware registration
- Router registration
- Security headers configuration
- CORS configuration

**requirements.txt**
- Python dependencies specification
- Package version pinning for reproducibility

**.env.example**
- Environment variable template
- Configuration documentation
- Required settings for deployment

**Makefile**
- Common development operations
- Build and deployment commands
- Test execution shortcuts
- Code quality tools

**README.md**
- Complete project documentation
- Setup and installation instructions
- API usage examples
- Deployment guide

---

## AI Layer (`ai/`)

### AI Layer Root
**ai/__init__.py**
- Package initialization

### Schema Analysis (`ai/analyzers/`)
**ai/analyzers/__init__.py**
- Package initialization

**ai/analyzers/schema_analyzer.py**
- Schema summary generation from database metadata
- Table and column information extraction
- Data type analysis
- Sample data collection for AI context

### Cache Management (`ai/cache/`)
**ai/cache/__init__.py**
- Package initialization

**ai/cache/cache_manager.py**
- KPI result caching with TTL
- Cache key generation
- Cache invalidation logic
- Performance optimization for repeated queries

### SQL Execution (`ai/executors/`)
**ai/executors/__init__.py**
- Package initialization

**ai/executors/sql_executor.py**
- AI-generated SQL query execution
- Single-value result formatting for KPIs
- Error handling for AI queries
- Inherits from unified SQL executor

### KPI Generation (`ai/generators/`)
**ai/generators/__init__.py**
- Package initialization

**ai/generators/kpi_generator.py**
- AI-powered KPI generation
- Financial metric suggestion
- SQL query generation for KPIs
- KPI categorization

### LLM Integration (`ai/llm/`)
**ai/llm/__init__.py**
- Package initialization

**ai/llm/openai_client.py**
- OpenAI API client wrapper
- Chat completion handling
- Retry logic and error handling
- Lazy initialization for performance
- Model configuration (GPT-3.5-turbo)

### Response Parsing (`ai/parsers/`)
**ai/parsers/__init__.py**
- Package initialization

**ai/parsers/response_parser.py**
- LLM response parsing
- JSON extraction from AI responses
- Schema analysis result parsing
- Error handling for malformed responses

### Prompt Templates (`ai/prompts/`)
**ai/prompts/__init__.py**
- Package initialization

**ai/prompts/schema_analysis.py**
- AI prompt templates for schema analysis
- System prompts for financial context
- Few-shot examples for better results
- Prompt engineering for accuracy

---

## Configuration (`config/`)

**config/__init__.py**
- Package initialization

**config/settings.py**
- Application settings management
- Environment variable loading
- Configuration validation
- Default values and overrides

**config/logging.py**
- Logging configuration
- Log format setup
- Log level management
- Structured logging setup

**config/validation.py**
- Environment configuration validation
- Startup checks
- Required directory creation
- Configuration error handling

---

## Constants (`constants/`)

**constants/__init__.py**
- Package initialization

**constants/constants.py**
- Application-wide constants
- Error messages
- Status values
- Configuration defaults

---

## Core Utilities (`core/`)

**core/__init__.py**
- Package initialization

**core/exceptions.py**
- Centralized exception handling
- Application error to API exception mapping
- Standardized error responses
- HTTP status code mapping

**core/helpers.py**
- Reusable helper functions
- Data sanitization utilities
- Type conversion helpers
- String manipulation utilities
- Validation helpers

**core/logging.py**
- Logging utilities and decorators
- Function call logging
- Operation logging
- Context-aware logging

**core/response.py**
- Standardized API response formats
- Success response builder
- Error response builder
- Response wrapper models

---

## Database Layer (`database/`)

**database/__init__.py**
- Package initialization

**database/base.py**
- SQLAlchemy base model
- Database session configuration
- Model metadata

**database/duckdb_manager.py**
- DuckDB connection management
- Table creation from DataFrames
- Query execution
- Connection pooling and cleanup

**database/sql_executor.py**
- Unified SQL executor for all query operations
- Result formatting (single-value vs table)
- Error handling and logging
- Connection management
- Base class for specialized executors

---

## Dependency Injection (`dependencies/`)

**dependencies/__init__.py**
- Package initialization

**dependencies/container.py**
- Dependency injection container
- Service factory registration
- Singleton management
- Dependency resolution

**dependencies/database.py**
- Database session management
- SQLAlchemy session factory
- Database initialization
- Dependency functions for services

---

## Custom Exceptions (`exceptions/`)

**exceptions/__init__.py**
- Package initialization

**exceptions/exceptions.py**
- Custom exception definitions
- Base application exception
- File validation exceptions
- Database exceptions
- AI service exceptions
- Dataset exceptions

---

## Middleware (`middlewares/`)

**middlewares/__init__.py**
- Package initialization

**middlewares/error_handler.py**
- Global error handling middleware
- Exception catching and logging
- Error response formatting
- Request context preservation

**middlewares/request_logging.py**
- Request/response logging middleware
- Request metadata logging
- Response time tracking
- Request ID generation

---

## Data Models (`models/`)

**models/__init__.py**
- Package initialization

**models/dataset.py**
- Dataset SQLAlchemy model
- Table SQLAlchemy model
- Column SQLAlchemy model
- Metadata storage models

**models/ai_models.py**
- Relationship SQLAlchemy model
- KPI SQLAlchemy model
- AI-generated data storage

---

## Query Layer (`query/`)

**query/__init__.py**
- Package initialization

**query/llm_client.py**
- Query-specific LLM client
- Natural language to SQL generation
- Query prompt handling
- AI interaction for conversational queries

**query/prompt_builder.py**
- Query prompt construction
- Schema context integration
- Relationship context inclusion
- KPI context addition
- Prompt engineering for SQL generation

**query/query_service.py**
- Conversational query orchestration
- End-to-end query processing
- Component coordination
- Error handling and fallback

**query/response_formatter.py**
- Query response formatting
- Natural language explanation generation
- Result presentation
- Error message formatting

**query/sql_executor.py**
- Query-specific SQL execution
- Table result formatting
- Inherits from unified SQL executor
- Optimized for conversational queries

**query/sql_validator.py**
- SQL security validation
- Injection prevention
- Dangerous keyword detection
- Query sanitization
- Table authorization

---

## Repository Layer (`repositories/`)

**repositories/__init__.py**
- Package initialization

**repositories/base.py**
- Base repository class
- Common CRUD operations
- Query building utilities

**repositories/dataset_repository.py**
- Dataset data access layer
- Table metadata operations
- Column metadata operations
- Dataset queries and updates

---

## API Routers (`routers/`)

**routers/__init__.py**
- Package initialization

**routers/health.py**
- Health check endpoint
- Version information endpoint
- Dependency health monitoring
- System status reporting

**routers/upload.py**
- File upload endpoint
- File validation
- Dataset creation
- Processing orchestration
- Error handling with standardized responses

**routers/dashboard.py**
- Dashboard endpoint
- Schema retrieval
- KPI presentation
- Relationship display
- AI-generated insights

**routers/query.py**
- Conversational query endpoint
- Natural language processing
- SQL generation and execution
- Result formatting
- Error handling

---

## Request/Response Schemas (`schemas/`)

**schemas/__init__.py**
- Package initialization

**schemas/dataset.py**
- Dataset request/response models
- Table metadata models
- Column metadata models
- Validation rules and constraints
- Enum definitions for file formats and status

**schemas/dashboard.py**
- Dashboard response models
- Schema presentation models
- Relationship models
- KPI models
- Financial context models

**schemas/query.py**
- Query request models
- Query response models
- Validation result models
- Execution result models

---

## Business Logic Layer (`services/`)

**services/__init__.py**
- Package initialization

**services/dataset_service.py**
- Dataset business logic
- File processing orchestration
- Metadata extraction
- DuckDB table creation
- Status management

**services/dashboard_service.py**
- Dashboard orchestration
- AI component coordination
- Schema analysis integration
- KPI generation coordination
- Response assembly

**services/dashboard_schema_analyzer.py**
- Schema analysis business logic
- AI interaction for schema understanding
- Schema object conversion
- Relationship extraction

**services/dashboard_kpi_executor.py**
- KPI execution business logic
- Cache management
- Query execution
- Result storage
- Performance optimization

---

## Test Suite (`tests/`)

**tests/__init__.py**
- Package initialization

**tests/fixtures/__init__.py**
- Package initialization

**tests/fixtures/sample_data.py**
- Sample data generators
- Test data creation
- Test configuration constants
- Fixture utilities

**tests/unit/__init__.py**
- Package initialization

**tests/integration/__init__.py**
- Package initialization

---

## Utility Functions (`utils/`)

**utils/__init__.py**
- Package initialization

**utils/file_parser.py**
- File parsing utilities
- CSV parsing
- Excel parsing
- Metadata extraction
- Data type inference

**utils/file_validator.py**
- File validation logic
- MIME type detection
- Size validation
- Content validation
- Security checks

---

## Data Directories

**uploads/**
- Temporary file storage
- Uploaded file processing
- File cleanup management

**data/**
- DuckDB database storage
- Analytical data storage
- Database file management

---

## Architecture Summary

### Layer Responsibilities

1. **API Layer** (`routers/`) - HTTP request handling, validation, response formatting
2. **Business Logic Layer** (`services/`) - Core business rules, orchestration
3. **Data Access Layer** (`repositories/`) - Database operations, queries
4. **AI Layer** (`ai/`) - AI integration, prompt engineering, response parsing
5. **Query Layer** (`query/`) - Conversational query processing
6. **Core Layer** (`core/`) - Shared utilities, exceptions, responses
7. **Database Layer** (`database/`) - Connection management, SQL execution
8. **Configuration Layer** (`config/`) - Settings, validation, logging
9. **Middleware Layer** (`middlewares/`) - Cross-cutting concerns
10. **Test Layer** (`tests/`) - Unit and integration tests

### Key Design Patterns

- **Dependency Injection**: Centralized DI container for service management
- **Repository Pattern**: Data access abstraction
- **Service Layer Pattern**: Business logic encapsulation
- **Strategy Pattern**: Multiple SQL execution strategies
- **Factory Pattern**: Service and object creation
- **Decorator Pattern**: Logging and validation decorators
- **Template Method**: Base classes with specialized implementations

### Data Flow

1. **Upload Flow**: Router → Service → Repository → Database → AI Layer
2. **Dashboard Flow**: Router → Service → AI Layer → Repository → Response
3. **Query Flow**: Router → Query Service → LLM → Validator → Executor → Formatter
4. **Error Flow**: Any Layer → Exception Handler → Standardized Response

### Security Considerations

- File validation with MIME type detection
- SQL injection prevention through validation
- Security headers on all responses
- Environment-based CORS configuration
- Size limits on file uploads
- Path traversal prevention in filenames

### Performance Optimizations

- KPI result caching with TTL
- Lazy initialization of expensive resources
- Connection pooling for databases
- Unified SQL executor to prevent duplication
- Async file operations where applicable

### Scalability Considerations

- Modular architecture for easy extension
- Service layer abstraction for testing
- Configuration-driven behavior
- Environment-specific settings
- Database abstraction for potential migration
