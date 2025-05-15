# YouTube LabelBase Backend

A FastAPI backend for analyzing YouTube videos using LLMs.

## Features

- YouTube video metadata extraction
- LLM-powered video analysis
- PostgreSQL database integration
- RESTful API endpoints
- CORS support for frontend integration

## Prerequisites

- Python 3.11+
- PostgreSQL
- Gemini API key
- pipenv (install with `pip install pipenv`)

## Setup

1. Install dependencies using pipenv:
   ```bash
   pipenv install
   ```

2. Create a `.env` file in the backend directory with the following content:
   ```
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=youtube_labelbase
   GOOGLE_API_KEY=your_google_api_key
   ```

3. Initialize the database:
   ```bash
   pipenv run alembic upgrade head
   ```

4. Start the development server:
   ```bash
   pipenv run uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## Development

### Using pipenv

- Activate the virtual environment:
  ```bash
  pipenv shell
  ```

- Install a new package:
  ```bash
  pipenv install package_name
  ```

- Install a development package:
  ```bash
  pipenv install package_name --dev
  ```

- Update dependencies:
  ```bash
  pipenv update
  ```

### Database Migrations

To create a new migration:
```bash
pipenv run alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
pipenv run alembic upgrade head
```

### Running Tests

```bash
pipenv run pytest
```

### Code Formatting

```bash
# Format code
pipenv run black .

# Sort imports
pipenv run isort .

# Lint code
pipenv run flake8
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration
│   ├── crud/             # Database operations
│   ├── db/               # Database models
│   ├── schemas/          # Pydantic models
│   ├── services/         # Business logic
│   └── main.py           # FastAPI app
├── alembic/              # Database migrations
├── Pipfile              # Python dependencies
├── Pipfile.lock         # Locked dependencies
└── README.md            # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 