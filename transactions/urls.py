from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.home, name="home"),
    path("transactions/", views.transactions_list, name="transactions_list"),
    path("transactions/<int:transaction_id>/", views.transaction_detail, name="transaction_detail"),
    path("income/", views.income_list, name="income_list"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("budgets/", views.budgets_list, name="budgets_list"),
    path("transactions/category/<str:category>/", views.transactions_by_category, name="transactions_by_category"),
    path("reports/", views.reports_overview, name="reports"),
    path("reports/<int:month>/", views.monthly_report, name="monthly_report"),
    path("top-expenses/", views.top_expenses, name="top_expenses"),
    path("convert/", views.convert_currency, name="convert"),
    path("expenses-chart/", views.expenses_chart, name="expenses_chart"),
]
