from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreate.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDestroy.as_view()),
    path('products/', ProductListCreate.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroy.as_view()),
    path('deposit/', deposit),
    path('buy/', buy),
    path('reset/', reset_deposit),
]
