from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_payment, name='payments'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]