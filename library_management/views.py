from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *





class CustomerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.last()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk=None):
        if pk:
            try:
                result = Customer.objects.get(pk=pk)
            except:
                return Response("No Customer matches query", status=status.HTTP_400_BAD_REQUEST)
            serializer = CustomerSerializer(result)
        ref = request.GET.get("search")
        if ref:
            user = Customer.objects.filter(Q(last_name__startswith=ref) or Q(first_name__startswith=ref))
            serializer = CustomerSerializer(user, many=True)
            return Response(serializer.data)
        result = Customer.objects.all()
        serializer = CustomerSerializer(result, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ChangePasswordView(APIView):
        """
        An endpoint for changing password.
        """
        model = User
        permission_classes = (IsAuthenticated,)
        
        def get_object(self, pk, queryset=None):
            #obj = self.request.user
            obj = User.objects.get(pk=pk)
            return obj

        def patch(self, request, *args, **kwargs):
            pk = request.data['pk']
            self.object = self.get_object(pk)
            serializer = ChangePasswordSerializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': serializer.data.get("new_password")
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Logout(APIView):
    def get(self, request, format=None):
        request.user.tokens == None
        request.user.save()
        return Response('Token deleted', status=status.HTTP_200_OK)




class BookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk=None):
        ref = request.GET.get("search")
        if pk:
            try:
                result = Book.objects.get(pk=pk)
            except:
                return Response("No book matches query", status=status.HTTP_400_BAD_REQUEST)
            serializer = BookSerializer(result)
            return Response(serializer.data)
        if ref:
            user = Book.objects.filter(Q(name__startswith=ref))
            serializer = BookSerializer(user, many=True)
            return Response(serializer.data)
        result = Book.objects.all()
        serializer = BookSerializer(result, many=True)
        return Response(serializer.data)



class BookLendingView(APIView):
    def post(self, request):
        serializer = BookLendingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk=None):
        customer = request.GET.get("customer")
        book = request.GET.get("book")
        if pk:
            try:
                result = BookLending.objects.get(pk=pk)
            except:
                return Response("No book lending matches query", status=status.HTTP_400_BAD_REQUEST)
            serializer = GetBookLendingSerializer(result)
        if customer and book:
            result = BookLending.objects.filter(customer=customer, book=book)
            serializer = GetBookLendingSerializer(result, many=True)
            return Response(serializer.data)     
        if customer:
            result = BookLending.objects.filter(customer=customer)
            serializer = GetBookLendingSerializer(result, many=True)
            return Response(serializer.data)    
        if book:
            result = BookLending.objects.filter(book=book)
            serializer = GetBookLendingSerializer(result, many=True)
            return Response(serializer.data)       
        result = BookLending.objects.all()
        serializer = GetBookLendingSerializer(result, many=True)
        return Response(serializer.data)


class CategoryView(APIView):
    def get(self, request):
        result = Category.objects.all()
        serializer = CategorySerializer(result, many=True)
        return Response(serializer.data)     

class CustomerRentalChargeView(APIView):
    def get(self, request, pk):
        if pk:
            try:
                result = customer_instance = Customer.objects.get(pk=pk)
            except:
                return Response("No customer matches query", status=status.HTTP_400_BAD_REQUEST)
        result = BookLending.objects.filter(customer=customer_instance)
        total = sum([each.rental_charge for each in result])
        serializer = GetBookLendingSerializer(result, many=True)
        return Response({"total_fee":total, "rented_books":serializer.data})     
