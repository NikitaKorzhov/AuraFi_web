from django.shortcuts import render

PROJECT_NAME = "AuraFi"

FEATURES = [
    {
        "title": "Track every transaction",
        "description": "Record income and expenses with a category, date, and note, and see them all in one place.",
    },
    {
        "title": "Stay within budget",
        "description": "Set a monthly spending limit per category, and jump straight to the transactions behind it.",
    },
    {
        "title": "Monthly reports",
        "description": "See income, expenses, and balance for any month at a glance.",
    },
    {
        "title": "Spot your biggest expenses",
        "description": "A ranked list and a visual breakdown show exactly where your money is going.",
    },
    {
        "title": "Convert currencies instantly",
        "description": "Quickly estimate an amount in USD or EUR without leaving the app.",
    },
]


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "title": "AuraFi",
            "text": (
                "AuraFi helps you see where your money actually goes. Track income "
                "and expenses, set budgets by category, and get a clear picture of "
                "your finances in one place."
            ),
            "features": FEATURES,
            "project_name": PROJECT_NAME,
        },
    )


STORY = [
    {
        "title": "A simple idea",
        "description": "AuraFi started as a lightweight way to log income and expenses without spreadsheets.",
    },
    {
        "title": "Built to last",
        "description": "The way AuraFi stores your data was rebuilt on a sturdier foundation, so your numbers stay accurate as your history grows.",
    },
    {
        "title": "Ready to grow",
        "description": "The core logic was refined so new features can be added quickly, without putting what already works at risk.",
    },
    {
        "title": "A home on the web",
        "description": "AuraFi is getting a full web experience, so you can check your finances from any browser.",
    },
]


def about(request):
    return render(
        request,
        "core/about.html",
        {
            "title": "About AuraFi",
            "text": (
                "AuraFi started as a simple way to keep track of personal spending, "
                "and has grown into a more complete tool for everyday budgeting."
            ),
            "story": STORY,
            "why_separate": (
                "AuraFi's web experience is developed as its own product, so new "
                "features can ship on their own schedule without putting the parts "
                "that already work at risk."
            ),
            "project_name": PROJECT_NAME,
        },
    )
