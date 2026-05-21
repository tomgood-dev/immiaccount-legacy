# ImmiAccount Legacy Mock App

A mock of Australia's ImmiAccount immigration portal, built as an ASP.NET Core 8 (Razor Pages) app. Used as the starting point for an Innovation Day workshop — it simulates the current portal so the team can redesign and rebuild it.

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

This will build the .NET image, seed the database, and start the app.

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
├── Data/               # EF Core DbContext and seed data
├── Helpers/            # Date formatting utilities
├── Models/             # Entity models (User, VisaApplication, etc.)
├── Pages/              # Razor Pages (routes + page models)
│   ├── Applications/   # Application list, detail, messages, documents
│   ├── Payments/       # Payments page
│   ├── Shared/         # Shared layouts (_Layout, _AppLayout)
│   ├── Login.cshtml
│   └── ManageAccount.cshtml
├── wwwroot/css/        # Stylesheet
├── Program.cs          # App startup and DI configuration
├── ImmiAccount.csproj
├── Dockerfile
└── docker-compose.yml
```

## Tech Stack

- **Runtime:** .NET 8 / ASP.NET Core
- **UI:** Razor Pages
- **Database:** SQLite via Entity Framework Core 8
- **Container:** Docker (multi-stage build, `mcr.microsoft.com/dotnet/aspnet:8.0`)
