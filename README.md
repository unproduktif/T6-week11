# Week 11 Task — Post Manager REST API Client

A desktop app for a Visual Programming course assignment that manages posts through a REST API (`https://api.pahrul.my.id/api/posts`). It supports full CRUD — listing posts in a table, viewing post details, adding a post via a dialog, editing, and deleting with a confirmation prompt. API calls run on a background `QThread` (via `ui/worker.py`) so the UI doesn't freeze while requests are in flight.

## Tech Stack

Python, PySide6, Requests, QThread, QSS for styling.

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`
