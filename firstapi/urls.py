from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'$^',),
    url(r'auth/$',views.AuthView.as_view(),name="auth"),
    url(r'auth/order/$',views.OrderView.as_view()),
    url(r'auth/login/$',views.UserLogin.as_view()),
    url(r'auth/test/$',views.TestView.as_view()),
    url(r'auth/role/$',views.RoleView.as_view()),
    url(r'auth/userinfo/$',views.UserInfoView.as_view()),
    url(r'auth/group/(?P<xxx>\d+)$', views.GroupInfoView.as_view(),name='group_link'),
    url(r'auth/usergroup/$',views.UserGroupView.as_view()),
]