from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'$^',),
    url(r'auth/$',views.AuthView.as_view()),
    url(r'auth/order/$',views.OrderView.as_view()),
]