from django.urls import path
from . import views

urlpatterns = [
    path("", views.RequestCounterAPIView.as_view(), name="request-counter"),
    path(
        "reset/",
        views.ResetRequestCounterAPIView.as_view(),
        name="reset-request-counter",
    ),
]
