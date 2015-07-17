from django.conf.urls import include, url
from django.contrib import admin
from views import IndexView
from rest_framework_nested import routers
from api import views
router = routers.SimpleRouter()
#router.register(r'accounts', DetailMatchViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'dotaparty.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^api/detailmatch/(?P<match_id>[0-9]+)$', views.get_details_match),
    url('^api/profile/(?P<account_id>[0-9]+)$', views.get_profile),
    url('^.*$', IndexView.as_view(), name='index')
]
