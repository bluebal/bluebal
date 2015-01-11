from django.conf.urls import patterns, include, url
from django.contrib import admin
from .hammer.views import HammerView, ShareView, HammerItemView, LoginOrRegisterView, RegisterView, LoginView, UserPreferenceView


urlpatterns = patterns('',
    url(r'^$', HammerView.as_view(), name="home" ),
    url(r'^h/$', HammerView.as_view(), name="hammer"),
    url(r'^h/item/$', HammerItemView.as_view(), name="item"),
    url(r'^h/share/$', ShareView.as_view(), name="share"),
    url(r'^h/user/$', UserPreferenceView.as_view(), name="user"),
    url(r'^h/item/(?P<pk>\d+)/$', HammerItemView.as_view(), name="item_update"),
    url(r'^h/share/(?P<pk>\d+)/$', ShareView.as_view(), name="share_update"),
    url(r'^h/(?P<pk>\d+)/$', HammerView.as_view(), name="hammer_update"),
    url(r'^auth/$', LoginOrRegisterView.as_view(), name="auth"),
    url(r'^share/$', ShareView.as_view(), name="share"),
    url(r'^item/$', HammerItemView.as_view(), name="item"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', { "next_page": "/" }, name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^admin/', include(admin.site.urls)),
)
