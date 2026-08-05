"""home urls"""

from django.urls import path
from .views import (
    ExpenseListCreateView,
    ExpenseDetailView,
    ExpenseSummaryView,
    HouseTaskListCreateView,
    HouseTaskDetailView,
    HomeInventoryListCreateView,
    HomeInventoryDetailView,
)

urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("expenses/summary/", ExpenseSummaryView.as_view(), name="expense-summary"),
    path("tasks/", HouseTaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", HouseTaskDetailView.as_view(), name="task-detail"),
    path("inventory/", HomeInventoryListCreateView.as_view(), name="inventory-list"),
    path(
        "inventory/<int:pk>/",
        HomeInventoryDetailView.as_view(),
        name="inventory-detail",
    ),
]
