
from django.conf.urls import include, url
from django.contrib import admin

from website import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^searchResults', views.search_results, name='search_results'),
    url(r'^signup', views.sign_up, name='sign_up'),
    url(r'^login', views.login, name='login'),
    url(r'^doctor/(?P<pk>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.doctor_detail, name='doctor_detail'),
    url(r'^addReview/(?P<pk>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.add_review, name='add_review'),
    url(r'^doc/(?P<pk>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.add_favorite, name='add_favorite'),
]
