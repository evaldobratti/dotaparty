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
    url('^api/matches/(?P<match_id>[0-9]+)$', views.get_details_match),
    url('^api/profiles/(?P<account_id>[0-9]+)$', views.get_profile),
    url('^api/matches/accounts/(?P<accounts_ids>([0-9]+)(,[0-9]+)*)$', views.get_accounts_matches),
    url('^api/accounts/(?P<account_id>[0-9]+)$', views.get_account),
    url('^api/accounts/(?P<account_id>[0-9]+)/download$', views.download_games),
    #url('^api/detailmatches/account/(?P<account_id>[0-9]+)$', views.get_matches),
    url('^api/find/(?P<search>\w+)$', views.find),

    url('^.*$', IndexView.as_view(), name='index')
]
