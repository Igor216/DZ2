import datetime
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return 'User: {} {} {}'.format(self.id, self.name, self.phone)


class BankModel(models.Model):
    idbank = models.IntegerField(primary_key=True)
    director = models.CharField(max_length=30)
    address = models.CharField(max_length=255)

    def __str__(self):
        return str(self.address)


class TransactionModel(models.Model):
    idtran = models.IntegerField(primary_key=True)
    sum = models.IntegerField()
    type = models.CharField(max_length=50)
    user = models.ForeignKey('User', None)
    bank = models.ForeignKey('BankModel', None)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, verbose_name='Изображение')

    def __str__(self):
        return str(self.sum)

@admin.register(BankModel)
class BankAdmin(admin.ModelAdmin):
    list_display = ('idbank', 'address')
    search_fields = ('idbank', 'address')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('lastname',)

    def get_ordering(self, request):
        return ['name']


@admin.register(TransactionModel)
class TranAdmin(admin.ModelAdmin):
    list_display = ('idtran', 'sum', 'type', 'user', 'bank', 'date')
    list_filter = ['sum']
    search_fields = ('id', 'user')

    def get_ordering(self, request):
        return ['-idtran']

    def get_list_filter(self, request):
        return ['sum']
