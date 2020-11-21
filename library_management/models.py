from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from rest_framework_simplejwt.tokens import RefreshToken


today = timezone.now()

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User should have a username')
        if email is None:
            raise TypeError('User should have a email')
        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('User should have a password')
        print("email is "+email)
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def refresh_tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")    

    @property
    def contact_name(self):
        if self.user.first_name or self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return f' User {self.user.id}'

    @property
    def amount_due(self):
        value = BookLending.objects.filter(customer=self).aggregate(total_fee=models.Sum(models.F('days_borrowed') * models.F('book__category__price'), output_field=models.FloatField()))['total_fee']
        if value == None:
            return 0
        return value


    def __str__(self):
        return self.contact_name



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="book_category")




class BookLending(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True)
    days_borrowed = models.IntegerField(default=0)


    def __str__(self):
        self.days_borrowed = (timezone.now() - self.date_logged).days 
        self.save()
        return 'Lending: Book ' + str(self.book) + ' by ' + self.customer.contact_name

    @property
    def rental_charge(self):
        try:
            return ((timezone.now() - self.date_logged).days) * self.book.category.price
        except:
            return 0
    


    class Meta:
        unique_together = ["customer", "book"]  

