# 📘 Lexmax Backend Challenge -- Contacts API

------------------------------------------------------------------------

## 1. Description

This project is an API developed for the **Lexmax Backend Challenge**.

It provides a single main resource named **`contacts`**, implemented as
a basic CRUD service. The API allows clients to create, read, update,
and delete contact records.

### Available Endpoints

| Method | Endpoint       | Description                      |
| ------ | -------------- | ---------------------------------|
| GET    | /contacts      | List all contacts                |
| GET    | /contacts/{id} | Retrieve a single contact by ID  |
| POST   | /contacts      | Create a new contact             |
| PUT    | /contacts/{id} | Update an existing contact       |
| DELETE | /contacts/{id} | Delete a contact                 |

### Additional Endpoints

-   `GET /health` → Validates that the API is running and the database
    connection is working properly.
-   `GET /swagger` → Interactive API documentation (Swagger UI).

------------------------------------------------------------------------

### Architecture

The project follows a **Clean Architecture--inspired structure**,
separating responsibilities into clear layers:

-   **Routes (Presentation Layer)** → Handle HTTP requests and
    responses.
-   **Controllers (Application Layer)** → Orchestrate business logic.
-   **Repository (Data Access Layer)** → Encapsulate database
    interactions.
-   **Models (Domain/Data Layer)** → Represent database entities.
-   **Shared Layer** → Database configuration, base models, and custom
    exceptions.
-   **Migrations** → Managed with Alembic.
-   **Tests** → Implemented using pytest.

This separation ensures maintainability, testability, and scalability.

------------------------------------------------------------------------

## 2. Development Scope

All required features for the challenge were fully implemented.

### Implemented Requirements

-   ✅ Full CRUD for `/contacts`
-   ✅ Pagination support on `GET /contacts`
-   ✅ Email filtering on `GET /contacts`
-   ✅ Health check endpoint
-   ✅ Database connection handled via environment variables
-   ✅ Alembic migrations configured and working
-   ✅ Unit and integration tests using `pytest`
-   ✅ Dockerized application
-   ✅ Production-ready WSGI server using `gunicorn`
-   ✅ Swagger documentation available at `/swagger`

### Database

-   Default database: SQLite

-   Configurable via `DATABASE_URL` environment variable

-   Default value:

        sqlite:///sqlite.db

------------------------------------------------------------------------

## 3. Instructions to Run the Application

The application can be executed using **Docker (recommended)** or
locally for running tests.

------------------------------------------------------------------------

# 🐳 Running the Application with Docker

⚠️ **Important:** Before building and running the Docker image, you must
create and execute the initial migration locally.

## 1️⃣ Create Virtual Environment

``` bash
python3 -m venv venv
source venv/bin/activate
```

## 2️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

## 3️⃣ Configure Environment Variables

``` bash
cp .env.example .env
```

Make sure `.env` contains:

    DATABASE_URL=sqlite:///lexmax.db
    FLASK_ENV=development
    FLASK_DEBUG=1

## 4️⃣ Run Initial Migration

``` bash
./start_migration.sh "initial migration"
```

This will generate and apply the initial database schema.

------------------------------------------------------------------------

## 5️⃣ Build the Docker Image

``` bash
./build_docker.sh
```

Or manually:

``` bash
docker build -t lexmax-api .
```

------------------------------------------------------------------------

## 6️⃣ Run the Container

``` bash
./run_app.sh
```

Or manually:

``` bash
docker run -p 8000:8000 -e DATABASE_URL=sqlite:///lexmax.db lexmax-api
```

The API will be available at:

    http://localhost:8000

Swagger documentation:

    http://localhost:8000/swagger

------------------------------------------------------------------------

# 🧪 Running Tests Locally (Without Docker)

## 1️⃣ Activate Virtual Environment

``` bash
source venv/bin/activate
```

## 2️⃣ Run Tests

``` bash
pytest
```

The test suite covers:

-   Controllers
-   Repositories
-   Routes

------------------------------------------------------------------------

# 🔎 API Documentation

Once the server is running, interactive API documentation is available
at:

    /swagger

This documentation is automatically generated using `flask-smorest` and
OpenAPI 3.0.

------------------------------------------------------------------------

# 🚀 Production Notes

-   Uses `gunicorn` with 4 workers
-   CORS enabled for all origins
-   Environment variables managed via `python-dotenv`
-   Database engine created using SQLAlchemy 2.0
-   Migrations handled via Alembic
-   Designed for portability and container deployment
