from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sqlite3

database_path = "database.sqlite"

app = FastAPI()


# Models
class CreateSessionRequest(BaseModel):
	sprint_name: str
	creator_name: str


class JoinSessionRequest(BaseModel):
	user_name: str


class EstimateRequest(BaseModel):
	value: int


class SessionResponse(BaseModel):
	session_id: int
	code: str


def get_db():
	conn = sqlite3.connect(database_path)
	conn.row_factory = sqlite3.Row
	return conn


@app.post("/sessions/", response_model=SessionResponse)
def create_session(request: CreateSessionRequest):
	conn = get_db()
	try:
		cursor = conn.cursor()

		# First, create the user
		cursor.execute("""
            INSERT INTO Users (name)
            VALUES (?)
        """, (request.creator_name,))
		user_id = cursor.lastrowid

		# Create a new session
		import uuid
		session_code = str(uuid.uuid4())[:8]
		cursor.execute("""
            INSERT INTO Sessions (creator_id, code)
            VALUES (?, ?)
        """, (user_id, session_code))
		session_id = cursor.lastrowid

		# Update the user's session_id
		cursor.execute("""
            UPDATE Users
            SET session_id = ?
            WHERE id = ?
        """, (session_id, user_id))

		conn.commit()
		return {"session_id": session_id, "code": session_code}
	except sqlite3.Error as e:
		conn.rollback()
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		conn.close()


@app.post("/sessions/{session_code}/join")
def join_session(session_code: str, request: JoinSessionRequest):
	conn = get_db()
	try:
		cursor = conn.cursor()

		# Find the session
		cursor.execute("SELECT id FROM Sessions WHERE code = ?", (session_code,))
		session = cursor.fetchone()
		if not session:
			raise HTTPException(status_code=404, detail="Session not found")

		session_id = session['id']

		# Create the user and associate with session
		cursor.execute("""
            INSERT INTO Users (name, session_id)
            VALUES (?, ?)
        """, (request.user_name, session_id))

		conn.commit()
		return {"message": "Successfully joined session"}
	except sqlite3.Error as e:
		conn.rollback()
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		conn.close()


@app.post("/sessions/{session_code}/estimate")
def submit_estimate(session_code: str, request: EstimateRequest, user_name: str):
	conn = get_db()
	try:
		cursor = conn.cursor()

		# Get session and user IDs
		cursor.execute("""
            SELECT s.id as session_id, u.id as user_id 
            FROM Sessions s
            JOIN Users u ON u.name = ? AND u.session_id = s.id
            WHERE s.code = ?
        """, (user_name, session_code))
		result = cursor.fetchone()

		if not result:
			raise HTTPException(status_code=404, detail="Session or user not found")

		# Check if vote exists
		cursor.execute("""
            SELECT id FROM Votes 
            WHERE session_id = ? AND user_id = ?
        """, (result['session_id'], result['user_id']))
		existing_vote = cursor.fetchone()

		if existing_vote:
			# Update existing vote
			cursor.execute("""
                UPDATE Votes 
                SET value = ?
                WHERE session_id = ? AND user_id = ?
            """, (request.value, result['session_id'], result['user_id']))
		else:
			# Insert new vote
			cursor.execute("""
                INSERT INTO Votes (session_id, user_id, value)
                VALUES (?, ?, ?)
            """, (result['session_id'], result['user_id'], request.value))

		conn.commit()
		return {"message": "Estimate submitted successfully"}
	except sqlite3.Error as e:
		conn.rollback()
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		conn.close()


@app.get("/sessions/{session_code}/estimates")
def get_estimates(session_code: str):
	conn = get_db()
	try:
		cursor = conn.cursor()

		cursor.execute("""
            SELECT u.name, v.value
            FROM Votes v
            JOIN Sessions s ON s.id = v.session_id
            JOIN Users u ON u.id = v.user_id
            WHERE s.code = ?
        """, (session_code,))

		estimates = [{"user": row['name'], "estimate": row['value']}
		             for row in cursor.fetchall()]

		return {"estimates": estimates}
	except sqlite3.Error as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		conn.close()