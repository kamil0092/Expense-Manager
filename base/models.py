from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Expense(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=140)
    description = models.CharField(null=True, blank=True, max_length=140)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    data_of_expense = models.DateField()
    amount = models.PositiveIntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.host:
            self.host = User.objects.get(username=self.request.user.username)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name
