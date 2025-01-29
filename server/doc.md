# Planning Poker API

A simple FastAPI application for running planning poker sessions with SQLite backend.

## Features

- Create planning poker sessions
- Join existing sessions using session codes
- Submit and update estimates
- View all estimates for a session
- Persistent storage using SQLite

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install fastapi uvicorn sqlite3
```

3. Initialize the database:
```bash
python db.py
```

4. Start the server:
```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`
for swagger doc  `http://127.0.0.1:8000/docs`

## Database Schema

The application uses three main tables:

- **Users**: Stores participant information
- **Sessions**: Stores planning poker sessions
- **Votes**: Stores estimates submitted by users

## API Endpoints

### Create Session
```bash
POST /sessions/
{
    "sprint_name": "Sprint Name",
    "creator_name": "Creator Name"
}
```

### Join Session
```bash
POST /sessions/{session_code}/join
{
    "user_name": "User Name"
}
```

### Submit Estimate
```bash
POST /sessions/{session_code}/estimate?user_name=username
{
    "value": 5
}
```

### Get Estimates
```bash
GET /sessions/{session_code}/estimates
```

## Example Usage

1. Create a new session:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/sessions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sprint_name": "Sprint 1",
  "creator_name": "John"
}'
```

2. Join the session:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/sessions/[session_code]/join' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "Alice"
}'
```

3. Submit an estimate:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/sessions/[session_code]/estimate?user_name=Alice' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "value": 5
}'
```

## Project Structure

```
.
├── main.py           # FastAPI application
├── init_db.py        # Database initialization script
├── database.sqlite   # SQLite database file
└── README.md         # This file
```

## Technical Details

- Built with FastAPI and SQLite
- Uses SQLite for persistent storage without need for external database server
- Implements basic session management and voting system
- Handles concurrent votes through SQLite transactions
