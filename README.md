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

## Current state — Homework 37 + Homework 38 (Рівень 1 + Рівень 2)

Homework 37 added the `core` app (two static pages):

| Route | View | Template |
|---|---|---|
| `/` | `core.views.home` | `core/templates/core/home.html` |
| `/about/` | `core.views.about` | `core/templates/core/about.html` |

Homework 38 (lesson 38, "Маршрутизація та представлення") adds a second app,
`transactions`, following the homework's own **Project 2: Expense & Budget
Tracker** track (chosen because it's the closest match to AuraFi's own
domain) — **Рівень 1 only**, as hardcoded in-memory data, exactly as the
homework spec prescribes at this level:

| Route | View | Template |
|---|---|---|
| `/app/` | `transactions.views.home` | `transactions/templates/transactions/home.html` |
| `/app/transactions/` | `transactions.views.transactions_list` | `transactions/templates/transactions/transactions_list.html` |
| `/app/transactions/<int:transaction_id>/` | `transactions.views.transaction_detail` | `transactions/templates/transactions/transaction_detail.html` |
| `/app/income/` | `transactions.views.income_list` | `transactions/templates/transactions/transactions_list.html` |
| `/app/expenses/` | `transactions.views.expense_list` | `transactions/templates/transactions/transactions_list.html` |
| `/app/budgets/` | `transactions.views.budgets_list` | `transactions/templates/transactions/budgets_list.html` |

`transactions` is mounted under `/app/` (`aurafi_web/urls.py`) rather than at
`""`, since `core` already owns the site root from Homework 37 — the
homework's own routes (`""`, `transactions/`, `income/`, ...) are preserved
unchanged underneath that prefix. An unknown transaction id
(`/app/transactions/999/`) returns a real 404, same as the homework spec.

Both apps extend the same shared `templates/base.html`, whose nav now links
to all three areas (Головна / Про проєкт / Трекер).

Рівень 2 (просунутий) adds 3 more routes, all with typed dynamic parameters
and real 404 handling:

| Route | View | Template | Notes |
|---|---|---|---|
| `/app/transactions/category/<str:category>/` | `transactions_by_category` | `transactions_list.html` | case-insensitive match; empty list if no match |
| `/app/reports/<int:month>/` | `monthly_report` | `report.html` | income/expense/balance totals for that month; 404 if `month` not in 1-12 |
| `/app/top-expenses/` | `top_expenses` | `transactions_list.html` | top 5 expenses by amount, descending |

The budgets page links each category straight into its filtered transaction
list, and the tracker home page links to the top-expenses and a November
monthly report.

No models, no database work, no auth yet — hardcoded data is deliberate at
this level; real models start at lesson 40. Рівень 3 (bonus — CSS styling,
comments, dashboard) is not yet implemented.

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
- http://127.0.0.1:8000/app/ — expense tracker home
- http://127.0.0.1:8000/app/transactions/ — all transactions
- http://127.0.0.1:8000/app/income/ — income only
- http://127.0.0.1:8000/app/expenses/ — expenses only
- http://127.0.0.1:8000/app/budgets/ — budgets
- http://127.0.0.1:8000/app/transactions/category/Food/ — filter by category
- http://127.0.0.1:8000/app/reports/11/ — monthly report (month 1-12)
- http://127.0.0.1:8000/app/top-expenses/ — top 5 expenses

## Project layout

```text
AuraFi_web/
├── aurafi_web/          # Django project package (settings, root urls)
├── core/                # Homework 37 — home/about pages
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
├── transactions/        # Homework 38 (Рівень 1+2) — expense tracker views
│   ├── views.py
│   ├── urls.py
│   └── templates/transactions/
├── templates/
│   └── base.html        # shared layout all page templates extend
├── manage.py
└── requirements.txt
```
