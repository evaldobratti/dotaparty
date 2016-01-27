from django.conf.urls import include, url
from django.contrib import admin
from views import IndexView
from api import views
from api.cviews import reports

urlpatterns = [
    # Examples:
    # url(r'^$', 'dotaparty.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url('^api/matches/(?P<match_id>[0-9]+)$', views.get_details_match),
    url('^api/matches/accounts/(?P<comma_accounts_ids>([0-9]+)(,[0-9]+)*)$', views.get_accounts_matches),

    url('^api/profiles/(?P<account_id>[0-9]+)$', views.get_profile),
    url('^api/profiles/(?P<account_id>[0-9]+)/download$', views.download_games),
    url('^api/profiles/(?P<account_id>[0-9]+)/reports/created$', reports.ReportsCreated.as_view()),
    url('^api/profiles/(?P<account_id>[0-9]+)/reports/received$', reports.ReportsReceived.as_view()),

    url('^api/find$', views.find),
    url('^api/logout/$', views.logout),
    url('^api/user/', views.get_authenticated_user),
    url('^api/community/report/$', views.new_report),

    url('^api/statistics/', views.get_statistics),
    url('^.*$', IndexView.as_view(), name='index')
]
