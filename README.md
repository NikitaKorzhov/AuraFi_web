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

## Current state — Homework 37 + Homework 38 (all levels) + Homework 39

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

Рівень 3 (бонус) adds:

| Route | View | Template | Notes |
|---|---|---|---|
| `/app/convert/` | `convert_currency` | `convert.html` | GET form, UAH ↔ USD ↔ EUR, hardcoded rates; sticky inputs, inline error on bad input |
| `/app/expenses-chart/` | `expenses_chart` | `expenses_chart.html` | ASCII-art bar chart (`█`) of expenses by category, sorted descending |

Plus a general UX/usability pass across the whole site (both apps, not just
`transactions`):
- **Light/dark theme toggle** — a button in the header, persisted in
  `localStorage`, defaulting to the OS's `prefers-color-scheme` on first
  visit; implemented with CSS custom properties in `templates/base.html` so
  every page (including `core`'s) picks it up automatically, no per-page
  work needed.
- A persistent **sub-navigation bar** (`transactions/_subnav.html`, included
  on every tracker page) to every tracker route, with the current page
  highlighted — no more "back to home to get anywhere else".
- Active-link highlighting in the main header nav too
  (`request.resolver_match`), so you always know which app/page you're on.
- Numbers formatted with thousands separators (`django.contrib.humanize`'s
  `intcomma`) instead of raw digit strings.
- A month-picker (1-12) on the report page instead of hand-editing the URL.
- Responsive layout (viewport meta tag, wrapping nav, horizontally
  scrollable tables on narrow screens) — usable on a phone, not just desktop.

No models, no database work, no auth yet — hardcoded data is deliberate at
this level; real models start at lesson 40.

Homework 39 (lesson 39, "Шаблони та статичні файли") is done on top of the
same `transactions` app — still **Project 2: Expense & Budget Tracker**, now
with templates driven by actual CSS/JS static files instead of an inline
`<style>` block, plus the dashboard/budget features the homework calls for:

- **Static files**: `static/css/style.css` and `static/js/main.js`
  (project-level `STATICFILES_DIRS`), loaded via `{% load static %}` /
  `{% static %}` in `templates/base.html`. The one exception is the few
  lines that pick light/dark theme before first paint — that has to run
  inline in `<head>` before the stylesheet applies, or the page flashes the
  wrong theme; everything else (the CSS, the click handler) lives in the
  static files.
- **Dashboard** (`/app/`) — reworked into the homework's shape: income /
  expense / balance cards for the current month, plus a "recent
  transactions" table (last 5, newest first). The underlying totals and
  sorting reuse the same filtering AuraFi's console app already does by
  month, not a new calculation.
- **Transaction filtering** on `/app/transactions/?type=income|expense` —
  filter buttons on the same page, alongside the existing dedicated
  `/app/income/` and `/app/expenses/` routes.
- **Budgets** (`/app/budgets/`) — now computes real `spent` / `remaining` /
  `percentage` per category from the transaction list (the same spent/
  remaining/utilization logic AuraFi's console `Budget` class uses) and
  renders it as a progress bar, instead of just listing the limit.
- **Reports overview** (`/app/reports/`, new) — expenses grouped by
  category plus overall income/expense totals, complementing the existing
  per-month report and the ASCII chart.
- Money values use `{{ value|intcomma }}` for thousands separators, dates
  are shown as-is (`YYYY-MM-DD`) since the mock data has no time component.

Deliberately **not** implemented at this level: Add/Edit/Delete links for
transactions and budgets (the homework's own template examples link to
`add-transaction`, `edit-budget`, etc.) — those require real create/update/
delete views, which is lesson 41 (CRUD). Linking to pages that don't exist
yet would just be broken links, so they're left out until CRUD lands. Date-
range filtering, a balance-history line chart, and a budget "days left at
this rate" forecast (the homework's optional bonus items) are also skipped
for now.

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
- http://127.0.0.1:8000/app/convert/?amount=1000&from=UAH&to=USD — currency converter
- http://127.0.0.1:8000/app/expenses-chart/ — ASCII expenses chart
- http://127.0.0.1:8000/app/transactions/?type=income — transactions filtered by type
- http://127.0.0.1:8000/app/reports/ — expenses-by-category overview + totals

## Project layout

```text
AuraFi_web/
├── aurafi_web/          # Django project package (settings, root urls)
├── core/                # Homework 37 — home/about pages
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
├── transactions/        # Homework 38 (all levels) + Homework 39
│   ├── views.py
│   ├── urls.py
│   └── templates/transactions/
│       └── _subnav.html  # shared sub-nav included on every tracker page
├── templates/
│   └── base.html        # shared layout all page templates extend
├── static/              # Homework 39 — project-level static files
│   ├── css/style.css
│   └── js/main.js
├── manage.py
└── requirements.txt
```
