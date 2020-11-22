from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.urls import include
from django.conf import settings
from django.views.generic.base import TemplateView

from library_management.views import *

urlpatterns = [
    path('api/admin/', admin.site.urls),

    # AUTH ROUTES
    path('api/login/', LoginView.as_view(), name="login-view"),
    path('api/change-password/', ChangePasswordView.as_view()),

    # CUSTOMER ROUTES
    path('api/customer/', CustomerView.as_view()),
    path('api/customer/<int:pk>/', CustomerView.as_view()),

    # CATEGORY ROUTES
    path('api/category/', CategoryView.as_view()),

    # BOOK ROUTES
    path('api/book/', BookView.as_view()),
    path('api/book/<int:pk>/', BookView.as_view()),

    # BOOK LENDING ROUTES
    path('api/lend-book/', BookLendingView.as_view()),
    path('api/lend-book/<int:pk>/', BookLendingView.as_view()),

    # RENTED BOOKS BREAKDOWN
    path('api/rented-books/<int:pk>/', CustomerRentalChargeView.as_view(), name="rented-books-breakdown"),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]