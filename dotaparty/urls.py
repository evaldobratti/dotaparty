from django.conf.urls import include, url
from django.contrib import admin
from views import IndexView
from api import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'dotaparty.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url('^api/matches/(?P<match_id>[0-9]+)$', views.get_details_match),
    url('^api/profiles/(?P<account_id>[0-9]+)$', views.get_profile),
    url('^api/profiles/(?P<account_id>[0-9]+)/download$', views.download_games),
    url('^api/matches/accounts/(?P<comma_accounts_ids>([0-9]+)(,[0-9]+)*)$', views.get_accounts_matches),
    #url('^api/detailmatches/account/(?P<account_id>[0-9]+)$', views.get_matches),
    url('^api/find/(?P<search>\w+)$', views.find),
    url('^api/logout/$', views.logout),
    url('^api/user/', views.get_authenticated_user),
    url('^api/community/report/$', views.new_report),


    url('^.*$', IndexView.as_view(), name='index')
]
