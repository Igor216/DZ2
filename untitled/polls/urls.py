from django.conf.urls import url, include
from polls import views
from .views import create_transaction, CreateTransactionForm

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about$', views.about, name='about'),
    url(r'^banks/(?P<idbank>[0-9]+)/$', views.show_bank, name='bank'),
    url(r'^signup$',  views.signup, name='signup'),
    url(r'^signin$',  views.signin, name='signin'),
    url(r'^logout$',  views.logout, name='logout'),
    url(r'^success$',  views.login_success, name='success'),
    url(r'^userauth/(?P<id>\d+)$',  views.UserView.as_view(), name='user'),
    url(r'^main/$', views.main, name='main'),

    url(r'^transaction/$', create_transaction, name='create_transaction'),
]
