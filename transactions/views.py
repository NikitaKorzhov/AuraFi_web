from django.shortcuts import render
from django.http import HttpResponse

PROJECT_NAME = "AuraFi"

# Homework 38, Рівень 1: тимчасові дані на місці БД.
# Django-моделі для цього домену з'являться на лекції 40.
TRANSACTIONS = [
    {"id": 1, "amount": 30000, "type": "income", "category": "Salary", "date": "2026-11-01", "description": "Зарплата за листопад"},
    {"id": 2, "amount": 5000, "type": "expense", "category": "Food", "date": "2026-11-05", "description": "Продукти"},
    {"id": 3, "amount": 3000, "type": "expense", "category": "Transport", "date": "2026-11-07", "description": "Бензин"},
    {"id": 4, "amount": 15000, "type": "income", "category": "Freelance", "date": "2026-11-12", "description": "Проєкт для клієнта"},
]

BUDGETS = [
    {"category": "Food", "monthly_limit": 10000},
    {"category": "Transport", "monthly_limit": 5000},
    {"category": "Entertainment", "monthly_limit": 3000},
]


def home(request):
    total_income = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "income")
    total_expense = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "expense")
    balance = total_income - total_expense

    context = {
        "title": "Expense Tracker",
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/home.html", context)


def transactions_list(request):
    context = {
        "title": "Мої транзакції",
        "transactions": TRANSACTIONS,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def transaction_detail(request, transaction_id):
    transaction = next((t for t in TRANSACTIONS if t["id"] == transaction_id), None)
    if transaction is None:
        return HttpResponse("Транзакція не знайдена", status=404)

    context = {
        "title": "Деталі транзакції",
        "transaction": transaction,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transaction_detail.html", context)


def income_list(request):
    income_transactions = [t for t in TRANSACTIONS if t["type"] == "income"]
    total = sum(t["amount"] for t in income_transactions)

    context = {
        "title": "Доходи",
        "transactions": income_transactions,
        "total": total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def expense_list(request):
    expense_transactions = [t for t in TRANSACTIONS if t["type"] == "expense"]
    total = sum(t["amount"] for t in expense_transactions)

    context = {
        "title": "Витрати",
        "transactions": expense_transactions,
        "total": total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def budgets_list(request):
    context = {
        "title": "Бюджети",
        "budgets": BUDGETS,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/budgets_list.html", context)


# --- Рівень 2: Розширена функціональність ---

def transactions_by_category(request, category):
    filtered = [t for t in TRANSACTIONS if t["category"].lower() == category.lower()]
    total = sum(t["amount"] for t in filtered)

    context = {
        "title": f"Категорія: {category}",
        "transactions": filtered,
        "total": total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def monthly_report(request, month):
    if not 1 <= month <= 12:
        return HttpResponse("Невірний номер місяця (1-12)", status=404)

    month_prefix = f"-{month:02d}-"
    monthly = [t for t in TRANSACTIONS if month_prefix in t["date"]]
    income_total = sum(t["amount"] for t in monthly if t["type"] == "income")
    expense_total = sum(t["amount"] for t in monthly if t["type"] == "expense")

    context = {
        "title": f"Звіт за місяць №{month}",
        "month": month,
        "transactions": monthly,
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": income_total - expense_total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/report.html", context)


def top_expenses(request):
    expenses = sorted(
        (t for t in TRANSACTIONS if t["type"] == "expense"),
        key=lambda t: t["amount"],
        reverse=True,
    )[:5]

    context = {
        "title": "Топ-5 витрат",
        "transactions": expenses,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)
