from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from applications.store.api import api_checkout
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap,ProductSitemap,CategorySitemap
from django.contrib.auth import views

sitemaps = { 'static':StaticViewSitemap,'product':ProductSitemap,'category':CategorySitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('applications.core.urls')),
    path('',include('applications.store.urls')),
    path('',include('applications.cart.urls')),
    path('',include('applications.coupon.urls')),
    path('',include('applications.userprofile.urls')),
    path('',include('applications.newsletter.urls')),
    path('',include('applications.order.urls')),

    
    path('api/checkout',api_checkout,name='api_checkout'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('login/',views.LoginView.as_view(template_name='login.html'),name='login'),


    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.views.sitemap')
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
