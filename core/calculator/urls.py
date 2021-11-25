from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index),
    path("function", functions),
    path("valid_operations", valid_operations),
    path("operate", operate_function),
    path("manage", valid_operations),
]
