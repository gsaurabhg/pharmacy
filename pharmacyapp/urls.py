from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^list$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/report/sales/$', views.report_sales, name='report_sales'),
    url(r'^post/report/returns/$', views.report_returns, name='report_returns'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^patient/details/$', views.patient_details, name='patient_details'),
    url(r'^Patient/details/(?P<pk>\d+)/$', views.bill_details, name='bill_details'),
    url(r'^Patient/details/(?P<pk>\d+)/order/$', views.medicine_order, name='medicine_order'),
    url(r'^Patient/details/(?P<pk>\d+)/checkout/$', views.medicine_checkout, name='medicine_checkout'),
    url(r'^Patient/details/(?P<pk>\d+)/Previouscheckout/$', views.medicine_last_checkout, name='medicine_last_checkout'),
    url(r'^medicineName/details/(?P<pk>\d+)/remove/$', views.medicine_remove, name='medicine_remove'),
    url(r'^patient/details/(?P<pk>\d+)/allremove/$', views.medicine_allremove, name='medicine_allremove'),
    url(r'^medicineName/(?P<medName>[-\w]+)/get_batch_no/$', views.get_batch_no,name='get_batch_no'),
    url(r'^medicineName/(?P<medName>[^"]*)/get_batch_no/$', views.get_batch_no,name='get_batch_no'),
    url(r'^bill/details/(?P<pk>\d+)/$', views.meds_edit, name='meds_edit'),
    url(r'^list/(?P<pk>\d+)/$', views.meds_trf, name='meds_trf'),
]