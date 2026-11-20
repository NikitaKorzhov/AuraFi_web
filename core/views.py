from django.shortcuts import render

PROJECT_NAME = "AuraFi"


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "title": "AuraFi Web",
            "text": "Веб-версія AuraFi — особистого фінансового трекера.",
            "project_name": PROJECT_NAME,
        },
    )


def about(request):
    return render(
        request,
        "core/about.html",
        {
            "title": "Про проєкт",
            "text": (
                "AuraFi почалась як консольний застосунок на Python з PostgreSQL "
                "і SQLAlchemy ORM. Цей проєкт — наступна фаза: той самий домен "
                "(користувачі, транзакції, бюджети), але з веб-інтерфейсом на Django."
            ),
            "project_name": PROJECT_NAME,
        },
    )
