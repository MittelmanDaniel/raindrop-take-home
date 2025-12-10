# Natural Language to SQL Query API

*(don't worry I didn't vibecode the whole thing)*

A FastAPI application that converts natural language queries into ClickHouse SQL using OpenAI's GPT-5.1 with Context-Free Grammar (CFG) constraints, then executes them against Tinybird.

## Project Structure

```
raindrop_take_home/
├── main.py                 # FastAPI app entry point
├── routes.py               # API route definitions
├── models.py               # Pydantic models for request/response
├── config.py               # Configuration (Tinybird, OpenAI)
├── sql_generator.py        # Natural language → SQL conversion using CFG
├── tinybird_client.py      # Tinybird API client
├── evals.py                # Evaluation tests for CFG SQL generation
├── clickhouse_sql.lark     # CFG grammar definition (Lark format)
├── index.html              # Frontend HTML interface
├── static/
│   ├── styles.css          # Frontend styles
│   └── script.js           # Frontend JavaScript
├── datasources/            # Tinybird datasource definitions
│   └── IBM_HR_Employee_Attrition.datasource
└── requirements.txt        # Python dependencies
```

## Endpoints

### `GET /`
Serves the HTML frontend interface where users can input natural language queries and see results.

**Response:** HTML page with query input form

### `POST /query`
Converts natural language to SQL and executes it.

**Request Body:**
```json
{
  "query": "How many employees are in the Sales department?"
}
```

**Response:**
```json
{
  "natural_language_query": "How many employees are in the Sales department?",
  "generated_sql": "SELECT count() AS employee_count FROM IBM_HR_Employee_Attrition WHERE department = 'Sales' FORMAT JSON",
  "results": {
    "data": [...],
    "rows": 1
  }
}
```

### `GET /run-evals`
Runs evaluation tests to validate CFG SQL generation.

**Response:**
```json
{
  "status": "success",
  "message": "Evals completed"
}
```

## How It Works

1. **Natural Language Input**: User provides a query like "Show employees by department"
2. **CFG Constrained Generation**: GPT-5.1 generates SQL constrained by the Lark grammar in `clickhouse_sql.lark`
3. **Validation**: Generated SQL is validated against the CFG grammar using Lark parser
4. **Execution**: SQL is executed against Tinybird's ClickHouse database
5. **Response**: Results are returned as JSON

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export TINYBIRD_HOST="https://api.us-east.aws.tinybird.co"
export TINYBIRD_TOKEN="your-tinybird-token"
```

Or use a `.tinyb` file for local development.

3. Run the server:
```bash
fastapi dev main.py
```

4. Access the frontend at `http://localhost:8000`

## Running Tests

Run the evaluation suite:
```bash
python evals.py
```

Or via API:
```bash
curl http://localhost:8000/run-evals
```

## Key Features

- **CFG Constrained Generation**: Ensures all generated SQL is syntactically valid
- **Grammar Validation**: Uses Lark parser to validate SQL against CFG rules
- **Comprehensive Testing**: 20 evaluation tests across 4 categories
- **Support for Advanced SQL**: String functions, date functions, aggregations, CASE expressions, HAVING clauses, etc.

