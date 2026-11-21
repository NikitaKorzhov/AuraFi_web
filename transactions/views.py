from datetime import date

from django.shortcuts import render
from django.http import HttpResponse

PROJECT_NAME = "AuraFi"

TRANSACTIONS = [
    {"id": 1, "amount": 30000, "type": "income", "category": "Salary", "date": "2026-11-01", "description": "November salary"},
    {"id": 2, "amount": 5000, "type": "expense", "category": "Food", "date": "2026-11-05", "description": "Groceries"},
    {"id": 3, "amount": 3000, "type": "expense", "category": "Transport", "date": "2026-11-07", "description": "Gas"},
    {"id": 4, "amount": 15000, "type": "income", "category": "Freelance", "date": "2026-11-12", "description": "Client project"},
]

BUDGETS = [
    {"category": "Food", "monthly_limit": 10000},
    {"category": "Transport", "monthly_limit": 5000},
    {"category": "Entertainment", "monthly_limit": 3000},
]

EXCHANGE_RATES = {
    "UAH": 1.0,
    "USD": 41.5,
    "EUR": 43.8,
}


def _this_months_transactions():
    month_prefix = f"-{date.today().month:02d}-"
    return [t for t in TRANSACTIONS if month_prefix in t["date"]]


def home(request):
    this_month = _this_months_transactions()
    total_income = sum(t["amount"] for t in this_month if t["type"] == "income")
    total_expense = sum(t["amount"] for t in this_month if t["type"] == "expense")
    balance = total_income - total_expense

    recent_transactions = sorted(TRANSACTIONS, key=lambda t: t["date"], reverse=True)[:5]

    context = {
        "title": "Dashboard",
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent_transactions": recent_transactions,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/home.html", context)


def transactions_list(request):
    transactions = TRANSACTIONS
    type_filter = request.GET.get("type")
    if type_filter in ("income", "expense"):
        transactions = [t for t in transactions if t["type"] == type_filter]

    context = {
        "title": "Transactions",
        "transactions": transactions,
        "type_filter": type_filter,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def transaction_detail(request, transaction_id):
    transaction = next((t for t in TRANSACTIONS if t["id"] == transaction_id), None)
    if transaction is None:
        return HttpResponse("Transaction not found", status=404)

    context = {
        "title": "Transaction details",
        "transaction": transaction,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transaction_detail.html", context)


def income_list(request):
    income_transactions = [t for t in TRANSACTIONS if t["type"] == "income"]
    total = sum(t["amount"] for t in income_transactions)

    context = {
        "title": "Income",
        "transactions": income_transactions,
        "total": total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def expense_list(request):
    expense_transactions = [t for t in TRANSACTIONS if t["type"] == "expense"]
    total = sum(t["amount"] for t in expense_transactions)

    context = {
        "title": "Expenses",
        "transactions": expense_transactions,
        "total": total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def budgets_list(request):
    budgets_with_stats = []
    for b in BUDGETS:
        spent = sum(
            t["amount"] for t in TRANSACTIONS
            if t["type"] == "expense" and t["category"].lower() == b["category"].lower()
        )
        limit = b["monthly_limit"]
        percentage = round(min(spent / limit * 100, 100), 1) if limit else 0
        budgets_with_stats.append({
            "category": b["category"],
            "limit": limit,
            "spent": spent,
            "remaining": limit - spent,
            "percentage": percentage,
            "over_limit": spent > limit,
        })

    context = {
        "title": "Budgets",
        "budgets": budgets_with_stats,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/budgets_list.html", context)


def transactions_by_category(request, category):
    filtered = [t for t in TRANSACTIONS if t["category"].lower() == category.lower()]
    total = sum(t["amount"] for t in filtered)

    context = {
        "title": f"Category: {category}",
        "transactions": filtered,
        "total": total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def monthly_report(request, month):
    if not 1 <= month <= 12:
        return HttpResponse("Invalid month number (1-12)", status=404)

    month_prefix = f"-{month:02d}-"
    monthly = [t for t in TRANSACTIONS if month_prefix in t["date"]]
    income_total = sum(t["amount"] for t in monthly if t["type"] == "income")
    expense_total = sum(t["amount"] for t in monthly if t["type"] == "expense")

    context = {
        "title": f"Monthly report — month {month}",
        "month": month,
        "month_range": range(1, 13),
        "transactions": monthly,
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": income_total - expense_total,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/report.html", context)


def reports_overview(request):
    expense_totals = {}
    for t in TRANSACTIONS:
        if t["type"] == "expense":
            expense_totals[t["category"]] = expense_totals.get(t["category"], 0) + t["amount"]

    category_rows = sorted(expense_totals.items(), key=lambda item: item[1], reverse=True)
    total_income = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "income")
    total_expense = sum(expense_totals.values())

    context = {
        "title": "Reports",
        "category_rows": category_rows,
        "total_income": total_income,
        "total_expense": total_expense,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/reports.html", context)


def top_expenses(request):
    expenses = sorted(
        (t for t in TRANSACTIONS if t["type"] == "expense"),
        key=lambda t: t["amount"],
        reverse=True,
    )[:5]

    context = {
        "title": "Top 5 expenses",
        "transactions": expenses,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/transactions_list.html", context)


def convert_currency(request):
    currencies = list(EXCHANGE_RATES.keys())
    amount_raw = request.GET.get("amount", "")
    from_currency = request.GET.get("from", "UAH")
    to_currency = request.GET.get("to", "USD")
    result = None
    error = None

    if amount_raw:
        try:
            amount_value = float(amount_raw)
            if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
                raise ValueError("unknown currency")
            amount_in_uah = amount_value * EXCHANGE_RATES[from_currency]
            result = amount_in_uah / EXCHANGE_RATES[to_currency]
        except ValueError:
            error = "Enter a valid number"

    context = {
        "title": "Currency converter",
        "currencies": currencies,
        "rates": EXCHANGE_RATES,
        "amount": amount_raw,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "result": result,
        "error": error,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/convert.html", context)


def expenses_chart(request):
    totals = {}
    for t in TRANSACTIONS:
        if t["type"] == "expense":
            totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]

    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    max_amount = ranked[0][1] if ranked else 0
    bar_width = 30

    rows = []
    for category, amount in ranked:
        bar_len = round((amount / max_amount) * bar_width) if max_amount else 0
        rows.append({
            "category": category,
            "amount": amount,
            "bar": "█" * bar_len,
        })

    context = {
        "title": "Expenses by category",
        "rows": rows,
        "project_name": PROJECT_NAME,
    }
    return render(request, "transactions/expenses_chart.html", context)
