
from epense import views
from django.urls import path, include

urlpatterns = [
     path('get-transactions/', views.get_transactions),
     path('transactions/',views.TransactionAPI.as_view())
    
]