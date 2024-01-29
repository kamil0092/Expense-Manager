from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),

    path("newExpense/", views.createExpense, name="newExpense"),
    path("view/<str:pk>/", views.viewPage, name="view"),
    path("updateExpense/<str:pk>/", views.updateExpense, name="updateExpense"),
    path("deleteExpense/<str:pk>/", views.deleteExpense, name="deleteExpense"),
    
]
