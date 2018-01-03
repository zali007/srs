from django.conf.urls import include,url
from . import views

urlpatterns = [
    url(r'^$',views.home,name='student_home'),
    url(r'^home/$',views.home_json,name='student_home_json'),
    url(r'^new/$', views.student_new, name='student_new'),
    url(r'^list_json/$', views.student_list_json.as_view(), name="student_list_json"),
    url(r'^(?P<pk>\d+)/$', views.student_detail, name='student_detail'),
    url(r'^(?P<pk>\d+)/edit$', views.student_edit, name='student_edit'),
]