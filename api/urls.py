from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameList, GameDetail, JoinGame


urlpatterns = {
    url(r'^games/$', GameList.as_view(), name='create'),
    url(r'^games/(?P<pk>[0-9]+)/$', GameDetail.as_view(), name='details'),
    url(
        r'^games/(?P<pk>[0-9]+)/join/(?P<player>[X|O])/$',
        JoinGame.as_view(), name='join'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
