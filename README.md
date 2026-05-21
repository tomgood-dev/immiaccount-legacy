# ImmiAccount Legacy Mock App

A mock of Australia's ImmiAccount immigration portal, built as a Flask/Python app. Used as the starting point for an Innovation Day workshop — it simulates the current portal so the team can redesign and rebuild it.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tomgood-dev/immiaccount-legacy.git
cd immiaccount-legacy
```

### 2. Start the app

```bash
docker compose up --build
```

This will build the image, seed the database, and start the Flask server.

### 3. Open in your browser

```
http://localhost:8080
```

### 4. Log in with the test account

| Field    | Value      |
|----------|------------|
| Username | `jsmith`   |
| Password | `Password1`|

---

## Stopping the App

```bash
docker compose down
```

To also wipe the database volume (e.g. to reset seed data):

```bash
docker compose down -v
```

---

## Restarting (after first build)

The image is already built, so subsequent starts are faster:

```bash
docker compose up
```

---

## Project Structure

```
immiaccount-legacy/
├── app/
│   ├── app.py          # Flask application
│   ├── database.py     # SQLite setup
│   ├── seed.py         # Test data
│   ├── static/         # CSS
│   └── templates/      # HTML templates
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
