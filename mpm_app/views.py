from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_list_or_404, get_object_or_404, render, render_to_response
from django_tables2 import SingleTableView, RequestConfig
from django_tables2.export.views import ExportMixin

from dal import autocomplete
from django.db.models import Count, Case,Sum, When, IntegerField, CharField
from django.db.models.functions import Substr
from django.db.models.expressions import Value
from django.contrib.auth.decorators import user_passes_test

import datetime
from itertools import chain

from mpm_app.models import Employee, Desg, Unit, appointment_choices, termination_choices, status_choices, gender_choices
from mpm_app.tables.employee import EmployeeTable, EmployeeFilter, EmpSummAreaTable,  EmpSummUnitTable, EmpSummDesgTable, EmpAddRedTable, EmpSummDesgAreaTable
from mpm_app.forms.employee import EmployeeFormHelper, EmpEditForm , EmpCreateForm
from mpm_app.forms.employee import EmployeeListFormHelper, EmployeeFormHelper
# from mpm_app.utils import PagedFilteredTableView

def in_apm_group(user):
    # print(user.groups.all())
    # print(u'area_apms')
    return user.groups.filter(name='area_apms').exists()

def index(request):
    return render_to_response('base.html')

def index_403(request):
    return render_to_response('403.html')

class PagedFilteredTableView(ExportMixin, SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    exclude_column = ('x_edit','x_transfer','x_promote','x_terminate')

    def get_queryset(self, **kwargs):
      qs = super(PagedFilteredTableView, self).get_queryset()
      self.filter = self.filter_class(self.request.GET, queryset=qs)
      self.filter.form.helper = self.formhelper_class()
      return self.filter.qs

    def get_context_data(self, **kwargs):
      context = super(PagedFilteredTableView, self).get_context_data()
      context[self.context_filter_name] = self.filter
      # context['total_rows'] = 33
      # print(context['total_rows'])
      return context

class EmployeeListView(GroupRequiredMixin,PagedFilteredTableView):
    model = Employee
    template_name = 'employee_new.html'
    context_object_name = 'customer'
    ordering = ['e_name']
    group_required = u'area_apms'
    table_class = EmployeeTable
    filter_class = EmployeeFilter
    formhelper_class = EmployeeFormHelper

    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        # try:
        #   print(qs.query)
        # except Exception as e:
        #   print(e)
        
        return qs
    
    def post(self, request, *args, **kwargs):
        return PagedFilteredTableView.as_view()(request)

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['nav_customer'] = True
        search_query = self.get_queryset()
        # print(search_query.query)
        table = EmployeeTable(search_query)
        RequestConfig(self.request, paginate={'per_page': 20}).configure(table)
        context['table'] = table
        context['total_rows'] = search_query.count()
        print(context['total_rows'])
        return context

T1 = Count(Case(When(e_desg__d_code__startswith='T1',then=1),output_field=IntegerField))
TA = Count(Case(When(e_desg__d_code__startswith='TA',then=1),output_field=IntegerField))
TB = Count(Case(When(e_desg__d_code__startswith='TB',then=1),output_field=IntegerField))
TC = Count(Case(When(e_desg__d_code__startswith='TC',then=1),output_field=IntegerField))
TD = Count(Case(When(e_desg__d_code__startswith='TD',then=1),output_field=IntegerField))
TE = Count(Case(When(e_desg__d_code__startswith='TE',then=1),output_field=IntegerField))
TF = Count(Case(When(e_desg__d_code__startswith='TF',then=1),output_field=IntegerField))
TG = Count(Case(When(e_desg__d_code__startswith='TG',then=1),output_field=IntegerField))
TH = Count(Case(When(e_desg__d_code__startswith='TH',then=1),output_field=IntegerField))
GS = Count(Case(When(e_desg__d_code__startswith='GS',then=1),output_field=IntegerField))
G1 = Count(Case(When(e_desg__d_code__startswith='G1',then=1),output_field=IntegerField))
G2 = Count(Case(When(e_desg__d_code__startswith='G2',then=1),output_field=IntegerField))
G3 = Count(Case(When(e_desg__d_code__startswith='G3',then=1),output_field=IntegerField))
XS = Count(Case(When(e_desg__d_code__startswith='XS',then=1),output_field=IntegerField))
XA = Count(Case(When(e_desg__d_code__startswith='XA',then=1),output_field=IntegerField))
XB = Count(Case(When(e_desg__d_code__startswith='XB',then=1),output_field=IntegerField))
XC = Count(Case(When(e_desg__d_code__startswith='XC',then=1),output_field=IntegerField))
XD = Count(Case(When(e_desg__d_code__startswith='XD',then=1),output_field=IntegerField))
XE = Count(Case(When(e_desg__d_code__startswith='XE',then=1),output_field=IntegerField))
C6 = Count(Case(When(e_desg__d_code__startswith='C6',then=1),output_field=IntegerField))
C5 = Count(Case(When(e_desg__d_code__startswith='C5',then=1),output_field=IntegerField))
C4 = Count(Case(When(e_desg__d_code__startswith='C4',then=1),output_field=IntegerField))
C3 = Count(Case(When(e_desg__d_code__startswith='C3',then=1),output_field=IntegerField))
C2 = Count(Case(When(e_desg__d_code__startswith='C2',then=1),output_field=IntegerField))
C1 = Count(Case(When(e_desg__d_code__startswith='C1',then=1),output_field=IntegerField))
PR = Count(Case(When(e_desg__d_code__startswith='PR',then=1),output_field=IntegerField))
ZZ = Count(Case(When(e_desg__d_code__startswith='ZZ',then=1),output_field=IntegerField))
# views.py
@user_passes_test(in_apm_group)
def emp_area_summ(request):
    qs = Employee.objects.values('e_unit_roll__u_area__a_code','e_unit_roll__u_area__a_name').order_by('e_unit_roll__u_area__a_code').filter(e_status='In_service').annotate(tot=Count('e_unit_roll'),
                d2_code = Substr('e_unit_roll__u_code',2,2),
                male=Count(Case(When(e_gender__iexact='Male',then=1),output_field=IntegerField)), 
                female=Count(Case(When(e_gender__iexact='Female',then=1),output_field=IntegerField)),
                T1 =T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB, XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
                )
    # print(qs.query)
    table = EmpSummAreaTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })
# views.py
def emp_unit_summ(request, area_code):
    qs = Employee.objects.values('e_unit_roll','e_unit_roll__u_name').filter(e_unit_roll__u_area__a_code=area_code,e_status='In_service').annotate(tot=Count('e_unit_roll'),
                male=Count(Case(When(e_gender__iexact='Male',then=1),output_field=IntegerField)), 
                female=Count(Case(When(e_gender__iexact='Female',then=1),output_field=IntegerField)),
                T1 =T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB, XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
                )
    # print(qs.query)
    table = EmpSummUnitTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })        

def emp_desg_unit_summ(request, unit_code):
    qs = Employee.objects.values('e_unit_roll','e_desg__d_gdesig').filter(e_unit_roll=unit_code,e_status='In_service').order_by('e_desg__d_gcode').annotate(
                d5_code = Substr('e_desg__d_code',3,5),
                # unit = '',
                tot=Count('e_unit_roll'),
                male=Count(Case(When(e_gender__iexact='Male',then=1),output_field=IntegerField)), 
                female=Count(Case(When(e_gender__iexact='Female',then=1),output_field=IntegerField)),
                T1 =T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB, XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
                )
    # print(qs.query)
    table = EmpSummDesgTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })

def emp_desg_area_summ(request, area_code):
    qs = Employee.objects.values('e_desg__d_gcode','e_unit_roll__u_area__a_code','e_desg__d_gdesig').filter(e_unit_roll__u_area__a_code=area_code,e_status='In_service').annotate(
                # d2_code = Substr('e_desg__d_code',3,2),
                # unit = '',
                tot=Count('e_unit_roll'),
                male=Count(Case(When(e_gender__iexact='Male',then=1),output_field=IntegerField)), 
                female=Count(Case(When(e_gender__iexact='Female',then=1),output_field=IntegerField)),
                T1 =T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB, XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
                )
    # print(qs.query)
    table = EmpSummDesgAreaTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })

def emp_desg_summ(request):
    qs = Employee.objects.values('e_unit_roll','e_desg__d_gdesig').filter(e_status='In_service').order_by('e_desg__d_gcode').annotate(
                d5_code = Substr('e_desg__d_code',3,5),
                # unit = '',
                tot=Count('e_unit_roll'),
                male=Count(Case(When(e_gender__iexact='Male',then=1),output_field=IntegerField)), 
                female=Count(Case(When(e_gender__iexact='Female',then=1),output_field=IntegerField)),
                T1 =T1, TA=TA, TB=TB, TC=TC, TD=TD, TE=TE, TF=TF, TG=TG, TH=TH, GS=GS, G1=G1, G2=G2, G3=G3, XS=XS, XA=XA, XB=XB, XC=XC, XD=XD, XE=XE, C6=C6, C5=C5, C4=C4, C3=C3, C2=C2, C1=C1, PR=PR, ZZ=ZZ,
                )
    # print(qs.query)
    table = EmpSummDesgTable(qs)

    return render(request, 'emp_summ.html', {
        'table': table
    })


present = datetime.date.today()
fiscal_yr = present.year
if present.month < 4:
    fiscal_yr = present.year-1
fiscal_st = datetime.date(fiscal_yr,4,1)
fiscal_end = datetime.date(fiscal_yr+1,3,30)
prev_fiscal_st = datetime.date(fiscal_yr-1,4,1)
prev_fiscal_end = datetime.date(fiscal_yr,3,30)


class CreateEmpView(GroupRequiredMixin, CreateView):
    """A create view for Foo model"""
    template_name = "emp_create.html"
    form_class = EmpCreateForm  # the change is over here
    model = Employee
    group_required = u'area_apms'
    success_url = '.'

    def get_form_kwargs(self):
        kw = super(CreateEmpView, self).get_form_kwargs()
        kw['req_username'] = self.request.user.username # the trick!
        # import ipdb; ipdb.set_trace()
        return kw



class EmployeeUpdate(GroupRequiredMixin, UpdateView):
    model = Employee
    # fields = '__all__'
    group_required = u'area_apms'
    form_class = EmpEditForm
    template_name = 'emp_update.html'
    
    def get_success_url(self):
        print('success_url='+self.request.GET.get('next'))
        return self.request.GET.get('next') 

    def dispatch(self, request, *args, **kwargs):
        handler = super(EmployeeUpdate, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        if self.object.e_unit_roll.u_code[1:3] != request.user.username[0:2] and self.object.e_unit_roll.u_code[1:3]!='99' and request.user.username not in ['iedstaff','iedhq']:
            # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
            return HttpResponseForbidden(index_403(request))
        return handler



class DesgAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Desg.objects.none()

        qs = Desg.objects.order_by('d_discp','d_gdesig','d_rank').all()

        if self.q:
            qs = qs.filter(d_code__icontains=self.q)

        return qs

class UnitAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Unit.objects.none()

        qs = Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name').all()

        if self.q:
            qs = qs.filter(u_code__icontains=self.q)

        return qs
