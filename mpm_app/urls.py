from django.conf.urls import url
from django.core.urlresolvers import reverse
from . import views
from django.views.generic import RedirectView

from mpm_app.models import Employee, Desg, Unit
from mpm_app.tables.employee import EmployeeTable, EmployeeFilter

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', RedirectView.as_view(url='emp/list/')),
    # (r'^one/$', RedirectView.as_view(url='/another/')),

    url(r'^emp/create/$', views.CreateEmpView.as_view(),name="emp_create"),
    url(r'^emp/edit/(?P<pk>\d+)/$', views.EmployeeUpdate.as_view(), name='emp_edit'),
    url(r'^emp/edit/$', views.EmployeeUpdate.as_view(), name='emp_edit'),
    # url(r'^delete/(?P<pk>\d+)/$', views.bug_delete, name='bug_delete'),
    url(r'^emp/list/$', views.EmployeeListView.as_view(
        model=Employee,
        table_class=EmployeeTable, 
        template_name='employee_new.html' , 
        filter_class = EmployeeFilter, 
    ) , name='empl_list'),
        # url(r'^delete/(?P<pk>\d+)/$', views.bug_delete, name='bug_delete'),
    
    url(r'^emp/list/area/$', views.emp_area_summ , name='emp_area_summ'),
    url(r'^emp/list/unit/(?P<area_code>\d+)$', views.emp_unit_summ , name='emp_unit_summ'),
    url(r'^emp/list/desg/(?P<unit_code>\w+)$', views.emp_desg_summ , name='emp_desg_summ'),

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