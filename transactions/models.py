from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """Categories: food, transport, entertainment, etc. — a shared catalog,
    not scoped to any one user (mirrors AuraFi's console-app `categories`
    table, which is also a shared catalog read by every user)."""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount in hryvnias",
    )
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "-date"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} ₴ ({self.get_transaction_type_display()})"

    def clean(self):
        if self.amount is not None and self.amount <= 0:
            raise ValidationError("Amount must be greater than zero")
        if self.transaction_type == "expense" and self.amount is not None and self.amount > 100000:
            raise ValidationError("Suspiciously large expense: more than 100,000 ₴")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_monthly_stats(cls, user, month, year):
        """Income/expense/balance totals for `user` in a given month+year —
        same shape as AuraFi's console-app monthly report."""
        transactions = cls.objects.filter(user=user, date__month=month, date__year=year)
        income = transactions.filter(transaction_type="income").aggregate(
            total=models.Sum("amount")
        )["total"] or 0
        expense = transactions.filter(transaction_type="expense").aggregate(
            total=models.Sum("amount")
        )["total"] or 0
        return {"income": income, "expense": expense, "balance": income - expense}

    @classmethod
    def get_by_category(cls, user):
        """Total expenses per category for `user`, highest spend first."""
        return (
            cls.objects.filter(user=user, transaction_type="expense")
            .values("category__name")
            .annotate(total=models.Sum("amount"))
            .order_by("-total")
        )

    @classmethod
    def get_expense_stats(cls, user):
        """Average expense, the single highest-spend category, and how many
        income vs. expense transactions `user` has — one `.aggregate()` /
        `.annotate()` call each, no looping in Python."""
        avg_expense = cls.objects.filter(user=user, transaction_type="expense").aggregate(
            avg=models.Avg("amount")
        )["avg"]
        top_category = cls.get_by_category(user).first()
        counts = cls.objects.filter(user=user).aggregate(
            income_count=models.Count("id", filter=models.Q(transaction_type="income")),
            expense_count=models.Count("id", filter=models.Q(transaction_type="expense")),
        )
        return {
            "avg_expense": avg_expense,
            "top_category": top_category["category__name"] if top_category else None,
            "income_count": counts["income_count"],
            "expense_count": counts["expense_count"],
        }


class Budget(models.Model):
    """A monthly spending limit on one category, per user — mirrors AuraFi's
    console-app `budgets` table (which has no concept of an income budget;
    the same restriction isn't enforced here at the model level, same as the
    homework spec, since the admin/UI layer is responsible for only ever
    offering expense categories when creating a budget)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Maximum monthly spending limit",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ["user", "category", "month", "year"]
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.month}/{self.year}): {self.limit} ₴"

    def get_spent(self):
        """How much has already been spent this month in this category."""
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type="expense",
            date__month=self.month,
            date__year=self.year,
        ).aggregate(total=models.Sum("amount"))["total"] or 0
        return spent

    def get_remaining(self):
        """How much is left to spend before hitting the limit."""
        return self.limit - self.get_spent()

    def is_exceeded(self):
        return self.get_spent() > self.limit


class Account(models.Model):
    """A bank account or wallet, e.g. 'Card' or 'Cash'."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="UAH")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.balance} {self.currency})"
