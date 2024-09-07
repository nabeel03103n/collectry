"""
URL configuration for emitra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from user import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include("django.contrib.auth.urls")),
    path('signup/', views.signup, name='signup'),
    path('',views.index,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('services/',views.services,name="services"),
    path('applications/',views.applications,name="applications"),
    path('donations/',views.donations,name="donations"),
    path('newbranch/',views.newbranch,name="newbranch"),
    path('initiate-transaction/', views.initiate_transaction, name='initiate_transaction'),
    path('transaction-status/', views.transaction_status, name='transaction_status'),
    path('refund-transaction/', views.refund_transaction, name='refund_transaction'),
    path('send-email/', views.send_email, name='send_email'),
    path('payment-success/',views.payment_sucess,name='payment-sucess'),
    path('payment-fail/',views.payment_fail,name='payment-failed')


] 
from django.contrib import admin

# Admin Site Config
admin.sites.AdminSite.site_header = 'Emitra Admin Panel'
admin.sites.AdminSite.site_title = 'Emitra'
admin.sites.AdminSite.index_title = 'Emitra Index'