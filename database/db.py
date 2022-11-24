import sqlite3
import json


db_path = "database/db.sqlite"


def create_db(path=db_path):
    with sqlite3.connect(path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS program_codes(
                          program_code TEXT,
                          program_name TEXT
                       )''')
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS polls(
                          channel_id INTEGER,
                          poll_id INTEGER,
                          data TEXT
                       )''')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS qotd(
                            data TEXT,
                            used INTEGER
                        )''')
        db.commit()


# PROGRAM SELECTION
def add_program(program_code, program_name):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       INSERT INTO program_codes(program_code, program_name)
                       VALUES(?, ?)
                       ''', (program_code, program_name))
        db.commit()


def get_programs():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       SELECT * FROM program_codes
                       ''')
        return cursor.fetchall()


def remove_program(program_code):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       DELETE FROM program_codes WHERE program_code = ?
                       ''', (program_code,))
        db.commit()


# POLLS
def add_poll(poll_id: str, poll):
    option_data = {item.name: 0 for item in poll.options}
    data = {"title": poll.title, "description": poll.description, "options": option_data, "voted": []}
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       INSERT INTO polls(poll_id, data)
                       VALUES(?, ?)
                       ''', (poll_id, json.dumps(data)))
        db.commit()


def get_poll(poll_id: str):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       SELECT data FROM polls WHERE poll_id = ?
                       ''', (poll_id,))
        return cursor.fetchone()


def get_polls():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       SELECT * FROM polls
                       ''')
        return cursor.fetchall()


def update_poll(poll_id: str, data: dict):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       UPDATE polls SET data = ? WHERE poll_id = ?
                       ''', (json.dumps(data), poll_id))
        db.commit()


def remove_poll(poll_id: str):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       DELETE FROM polls WHERE poll_id = ?
                       ''', (poll_id,))
        db.commit()


# QUESTION OF THE DAY
def add_qotd(data: str, used: int):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       INSERT INTO qotd(data, used)
                       VALUES(?, ?)
                       ''', (data, used))
        db.commit()


def get_random_qotd():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       SELECT data FROM qotd WHERE used = 0 ORDER BY RANDOM() LIMIT 1
                       ''')
        return cursor.fetchone()


def reset_qotd():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute('''
                       UPDATE qotd SET used = 0
                       ''')
        db.commit()


if __name__ == "__main__":
    create_db("db.sqlite")
