from django.conf.urls import url
from django.core.urlresolvers import reverse
from . import views, views_transaction
from django.views.generic import RedirectView

from mpm_app.models import Employee, Desg, Unit
from mpm_app.tables.employee import EmployeeTable, EmployeeFilter

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', RedirectView.as_view(url='emp/list/')),
    # (r'^one/$', RedirectView.as_view(url='/another/')),

    url(r'^emp/create/$', views.CreateEmpView.as_view(),name="emp_create"),
    url(r'^emp/edit/(?P<pk>\d+)/$', views.EmployeeUpdate.as_view(), name='emp_edit'),
    # url(r'^delete/(?P<pk>\d+)/$', views.bug_delete, name='bug_delete'),

    url(r'^emp/add/$', views_transaction.AddEmpView.as_view(),name="emp_add"),
    url(r'^emp/update/(?P<pk>\d+)/$', views_transaction.EditEmpView.as_view(), name='emp_update'), 
    url(r'^emp/transfer/(?P<pk>\d+)/$', views_transaction.EditTransferView.as_view(), name='emp_transfer'),   
    url(r'^emp/promote/(?P<pk>\d+)/$', views_transaction.EditPromoView.as_view(), name='emp_promote'),   
    url(r'^emp/terminate/(?P<pk>\d+)/$', views_transaction.EditTerminateView.as_view(), name='emp_terminate'), 
    url(r'^emp/detail/(?P<pk>\d+)/$', views_transaction.employee_detail, name='emp_detail'),     
    
    # url(r'^emp/addi_redu/unit/(?P<unit_code>\w+)$', views_transaction.emp_unit_addi_redu , name='emp_unit_addi_redu'),
    url(r'^emp/addi_redu/code/(?P<code>\w+)$', views_transaction.emp_unit_addi_redu , name='emp_unit_addi_redu'),



    url(r'^emp/list/$', views.EmployeeListView.as_view(
        model=Employee,
        table_class=EmployeeTable, 
        template_name='employee_new.html' , 
        filter_class = EmployeeFilter, 
    ) , name='empl_list'),
        # url(r'^delete/(?P<pk>\d+)/$', views.bug_delete, name='bug_delete'),
    
    url(r'^emp/list/area/$', views.emp_area_summ , name='emp_area_summ'),
    url(r'^emp/list/unit/(?P<area_code>\d+)$', views.emp_unit_summ , name='emp_unit_summ'),

    url(r'^emp/list/desg/$', views.emp_desg_summ , name='emp_desg_summ'),
    url(r'^emp/list/desg/(?P<area_code>\w+)$', views.emp_desg_area_summ , name='emp_desg_area_summ'),
    url(r'^emp/list/desg/unit/(?P<unit_code>\w+)$', views.emp_desg_unit_summ , name='emp_desg_unit_summ'),

    url(r'^emp/add_red/wcl/$', views.emp_add_red , name='emp_add_red'),

    url(
        r'^desg-autocomplete/$',
        views.DesgAutocomplete.as_view(),
        name='desg-autocomplete',
    ),
    url(
        r'^unit-autocomplete/$',
        views.UnitAutocomplete.as_view(),
        name='unit-autocomplete',
    ),
]

# from django.views.generic import RedirectView

# urlpatterns = patterns('',
#     (r'^one/$', RedirectView.as_view(url='/another/')),
# )