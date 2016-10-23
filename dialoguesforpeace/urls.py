from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User, Group

from dialogues import views
import django.contrib.auth.views as auth_views
from allauth.account.views import confirm_email as allauthemailconfirmation
from django.views.generic.base import RedirectView





urlpatterns = [ 
    # Examples:
    # url(r'^$', 'dialoguesforpeace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'hv/$', views.home_visit_index, name = 'home_visit_index'),
	url(r'hv/dist/(?P<district_id>\d+)/$', views.dist_direct_home_visit_index),
	url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dialogues/', include('dialogues.urls')),
    url(r'^bb/', include('bodhibuddyapp.urls')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/$', allauthemailconfirmation, name="account_confirm_email"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect')
]
