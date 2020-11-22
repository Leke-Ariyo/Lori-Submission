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


class CategoryModelTests(TestCase):
    def test_create_category(self):
        categories = len(Category.objects.all())
        Category.objects.create(name="Regular", price=1.5)
        self.assertIs(categories + 1, len(Category.objects.all()))


class BookModelTests(TestCase):
    def test_create_book(self):
        books = len(Book.objects.all())
        cat = Category.objects.create(name="Test Regular", price=1.5)
        new_book = Book.objects.create(name="C# for entrepreneurs", category=cat)
        self.assertIs(books + 1, len(Book.objects.all()))


class CalculateTotalFeeTest(TestCase):

    def setUp(self):
        regular = Category.objects.create(name="Regular", price=1.5)
        fiction = Category.objects.create(name="Fiction", price=3.0)
        novels = Category.objects.create(name="Novel", price=1.5)
        self.foo = User.objects.create(username="foouser",email="foobar@hotmail.com")
        self.pfe = Book.objects.create(name="Python for entrepreneurs", category=regular)
        self.harry_potter = Book.objects.create(name="Harry Potter", category=fiction)
        self.sci = Book.objects.create(name="SCI", category=fiction)
        self.game_of_thrones = Book.objects.create(name="Game of thrones", category=novels)
        self.legend_of_the_seeker = Book.objects.create(name="Legend of the seeker", category=novels)
        self.bl1 = BookLending.objects.create(book=self.pfe, customer=self.foo.customer)
        self.bl2 = BookLending.objects.create(book=self.harry_potter, customer=self.foo.customer)
        self.bl3 = BookLending.objects.create(book=self.game_of_thrones, customer=self.foo.customer)
        self.bl4 = BookLending.objects.create(book=self.legend_of_the_seeker, customer=self.foo.customer)
        self.bl5 = BookLending.objects.create(book=self.sci, customer=self.foo.customer)

    def test_get_total_charge(self):
        # get API response

        self.bl1.date_logged = timezone.now() - timedelta(days=2)
        self.bl1.save()
        self.bl2.date_logged = timezone.now() - timedelta(days=2)
        self.bl2.save()
        self.bl3.date_logged = timezone.now() - timedelta(days=0)
        self.bl3.save()
        self.bl4.date_logged = timezone.now() - timedelta(days=2)
        self.bl4.save()
        self.bl5.date_logged = timezone.now() - timedelta(days=1)
        self.bl5.save()
        response = client.get(reverse('rented-books-breakdown', kwargs={'pk': self.foo.pk}))
        self.assertEqual(response.json()['total_fee'], 20.0)
