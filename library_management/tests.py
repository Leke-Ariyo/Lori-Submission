import datetime
import requests
from datetime import datetime, timedelta 


from rest_framework import status
from django.contrib import auth
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .models import *
from .serializers import *
#– Unit tests cover models, views & OpenTDB API.
client = Client()


class UserModelTests(TestCase):
    def test_create_user(self):
        last_user = len(User.objects.all())
        new_user = User.objects.create(username="testuser",email="testuser@hotmail.com")
        self.assertIs(last_user + 1, len(User.objects.all()))



class CustomerModelTests(TestCase):
    def test_create_customer_with_user(self):
        customers = len(Customer.objects.all())
        new_user = User.objects.create(username="testuser",email="testuser@hotmail.com")
        self.assertIs(customers + 1, len(Customer.objects.all()))



class BookModelTests(TestCase):
    def test_create_book(self):
        books = len(Book.objects.all())
        new_book = Book.objects.create(name="C# for entrepreneurs")
        self.assertIs(books + 1, len(Book.objects.all()))


class CalculateTotalFeeTest(TestCase):

    def setUp(self):
        self.foo = User.objects.create(username="foouser",email="foobar@hotmail.com")
        self.python_book = Book.objects.create(name="Python for entrepreneurs")
        self.go_book = Book.objects.create(name="GO for dummies")
        self.bl1 = BookLending.objects.create(book=self.python_book, customer=self.foo.customer)
        self.bl2 = BookLending.objects.create(book=self.go_book, customer=self.foo.customer)


    def test_get_total_charge(self):
        # get API response

        test_number = 13
        self.bl1.date_logged = timezone.now() - timedelta(days=13)
        self.bl1.save()
        response = client.get(reverse('rented-books-breakdown', kwargs={'pk': self.foo.pk}))
        self.assertEqual(response.json()['total_fee'], 13)
