from django.contrib import admin
from django.urls import path, include
from payment.views import stripe_webhook 

urlpatterns = [
    path('api/stripe/', include('payment.urls')),
    path('Transcation/webhook/', stripe_webhook, name='stripe-webhook'),
]