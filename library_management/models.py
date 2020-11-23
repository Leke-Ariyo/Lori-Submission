from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

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

    def __str__(self):
        return self.name



class BookLending(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True)
    # dummy field
    days_borrowed = models.IntegerField(default=0)

    @property
    def rental_charge(self):
        days_spent = (timezone.now() - self.date_logged).days
        seconds = (timezone.now() - self.date_logged).seconds
        if seconds > 0:
            days_spent += 1
        if self.book.category.name == "Regular":
            # now cumulative charge is $2.0 for two days or less
            try:
                if days_spent <= 2:
                    return 2.0
                return ((days_spent - 2) * self.book.category.price) + 2
            except:
                return 0
        elif self.book.category.name == "Novel":
            try:
                # now cumulative charge is $4.5 for three days or less , 3 days is also $4.5
                if days_spent <= 3:
                    return 4.5
                return ((days_spent - 3) * self.book.category.price) + 4.5
            except:
                return 0
        else:
            try:
                return days_spent * self.book.category.price
            except:
                return 0


    def __str__(self):
        self.days_borrowed = (timezone.now() - self.date_logged).days 
        self.save()
        return 'Lending: Book ' + str(self.book) + ' by ' + self.customer.contact_name
    


    class Meta:
        unique_together = ["customer", "book"]  

