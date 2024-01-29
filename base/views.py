from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db.models import Q
from .models import Expense
from django.http import HttpResponse, HttpResponseForbidden

from .forms import ExpenseForm, RegisterForm

# Create your views here.

#<----------Registe-Page------------>
def registerPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "base/register.html", context)


#<----------Login-Page------------>
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error("email does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username & Password is incorrect")
    context = {}
    return render(request, "base/login.html", context)


#<----------Logout-Page------------>
def logoutPage(request):
    logout(request)
    return redirect("home")


#<----------Home-Page------------>
def homePage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    expenses = Expense.objects.filter(
        Q(name__icontains=q) | Q(data_of_expense__icontains=q)
    )
    context = {"expenses": expenses}
    return render(request, "base/home.html", context)


#<----------Create-Expense------------>
@login_required(login_url="login")
def createExpense(request):
    page = "create"
    form = ExpenseForm()

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.host = request.user
            expense.save()

            messages.success(request, "Expense successfully created!")

            return redirect("home")

    context = {"form": form, "page": page}
    return render(request, "base/create_expense.html", context)


#<----------Read-Expense------------>
def viewPage(request, pk):
    expense = Expense.objects.get(id=pk)

    # super user
    if request.user.is_superuser:
        context = {"expense": expense}
        return render(request, "base/view.html", context)
    # Owner
    elif expense.host == request.user:
        context = {"expense": expense}
        return render(request, "base/view.html", context)
    else:
        # admin nor the owner, return forbidden
        return HttpResponseForbidden("You don't have permission to view this expense.")


#<----------Update-Expense------------>
@login_required(login_url="login")
def updateExpense(request, pk):
    expense = Expense.objects.get(id=pk)
    form = ExpenseForm(instance=expense)

    if request.user != expense.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, '“Expense Updated successfully!”')
            return redirect("home")

    context = {"form": form}
    return render(request, "base/create_expense.html", context)


#<----------Delete-Expense------------>
@login_required(login_url="login")
def deleteExpense(request, pk):
    expense = Expense.objects.get(id=pk)

    if request.user != expense.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        expense.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": expense})
