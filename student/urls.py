from django.conf.urls import include,url
from . import views

urlpatterns = [
    url(r'^$',views.home,name='student_home'),
    url(r'^home/$',views.home_json,name='student_home_json'),
    url(r'^list_json/$', views.student_list_json.as_view(), name="student_list_json"),
]