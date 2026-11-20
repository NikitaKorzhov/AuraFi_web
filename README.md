# AuraFi Web

The web face of **[AuraFi](../AuraFi)** — a personal finance tracker that
started as a Python console app (SQLite → PostgreSQL → SQLAlchemy ORM) and is
now growing a Django front end, lesson by lesson, following the course's
Django block (lessons 37-49).

This is a **web project**: the goal is to reimplement the full AuraFi
functionality (users, categories, transactions, budgets, reports) as a
Django web application, not just a thin UI bolted on top of the console app.

This is a **separate project on purpose**, not a folder inside AuraFi itself:
Django owns its own models and migrations, and running two different ORMs
(SQLAlchemy and Django's) against the same live tables would mean two
systems both claiming ownership of the same schema. Once the course reaches
the Django-models lesson, this project will define its own Expense Tracker
schema (users/categories/transactions/budgets) — the same domain as AuraFi,
modeled fresh through Django ORM, with its own database.

## Current state — Homework 37 only

Two static pages, each with its own route, view, and template, with data
passed in through `render()`:

| Route | View | Template |
|---|---|---|
| `/` | `core.views.home` | `core/templates/core/home.html` |
| `/about/` | `core.views.about` | `core/templates/core/about.html` |

Both extend a shared `templates/base.html` (title + simple nav) — not
required by the homework, but it's the standard Django way to avoid
repeating the same HTML shell on every page, and sets up the pattern future
lessons (forms, CRUD, admin) will keep building on.

No models, no database work, no auth yet — that starts at lesson 40.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python manage.py runserver
```

Then open:
- http://127.0.0.1:8000/ — home page
- http://127.0.0.1:8000/about/ — about page

## Project layout

```text
AuraFi_web/
├── aurafi_web/          # Django project package (settings, root urls)
├── core/                # The one app so far — home/about pages
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
├── templates/
│   └── base.html        # shared layout both page templates extend
├── manage.py
└── requirements.txt
```
