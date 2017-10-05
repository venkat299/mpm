
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_list_or_404, get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import user_passes_test

import datetime as dt

from mpm_app.forms import transaction as transact_form
from mpm_app.models import Employee, TransferHistory, PromotionHistory
from mpm_app.tables.employee import EmpPromotionTable, EmpTransferTable, EmpAddRedTable

import mpm_app.query.employee_query as query 

def index_403(request):
    return render_to_response('403.html')

# check_user_permission(self.kwargs['pk'],request.user.username)
def check_user_permission(eis, username):
    emp_obj = Employee.objects.get(pk=eis)
    if emp_obj.e_unit_roll.u_code[1:3] !=username[0:2] and emp_obj.e_unit_roll.u_code[1:3]!='99' and username not in ['iedstaff','iedhq']:
        # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
        return True
    else: 
        return False

def in_apm_group(user):
    # print(user.groups.all())
    # print(u'area_apms')
    return user.groups.filter(name='area_apms').exists()

class AddEmpView(GroupRequiredMixin, CreateView):
    """A create view for Foo model"""
    template_name = "transaction/add_employee.html"
    form_class = transact_form.EmpAddForm  # the change is over here
    model = Employee
    group_required = u'area_apms'
    success_url = '.'

    def get_form_kwargs(self):
        kw = super(AddEmpView, self).get_form_kwargs()
        kw['req_username'] = self.request.user.username # the trick!
        kw['curr_user'] = self.request.user
        # import ipdb; ipdb.set_trace()
        return kw



class EditEmpView(GroupRequiredMixin, UpdateView):
    model = Employee
    # fields = '__all__'
    group_required = u'area_apms'
    form_class = transact_form.EmpEditForm
    template_name = 'transaction/edit_employee.html'
    
    def get_success_url(self):
        print('success_url='+self.request.GET.get('next'))
        return self.request.GET.get('next') 

    def dispatch(self, request, *args, **kwargs):
        handler = super(EditEmpView, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        if self.object.e_unit_roll.u_code[1:3] != request.user.username[0:2] and self.object.e_unit_roll.u_code[1:3]!='99' and request.user.username not in ['iedstaff','iedhq']:
            # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
            return HttpResponseForbidden(index_403(request))
        return handler

    def get_context_data(self, **kwargs):
        context = super(EditEmpView, self).get_context_data(**kwargs)
        context['panel_header'] = 'Edit Employee Details'
        return context


class EditTransferView(GroupRequiredMixin, UpdateView):
    model = Employee
    # fields = '__all__'
    group_required = u'area_apms'
    form_class = transact_form.EmpTransferForm
    template_name = 'transaction/edit_employee.html'
    
    def get_success_url(self):
        print('success_url='+self.request.GET.get('next'))
        return self.request.GET.get('next') 

    def dispatch(self, request, *args, **kwargs):
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        emp_obj = Employee.objects.get(pk=self.kwargs['pk'])
        if emp_obj.e_unit_roll.u_code[1:3] != request.user.username[0:2] and emp_obj.e_unit_roll.u_code[1:3]!='99' and request.user.username not in ['iedstaff','iedhq']:
            # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
            return HttpResponseForbidden(index_403(request))

        handler = super(EditTransferView, self).dispatch(request, *args, **kwargs)
        return handler

    def get_form_kwargs(self):
        kw = super(EditTransferView, self).get_form_kwargs()
        kw['req_username'] = self.request.user.username # the trick!
        kw['curr_user'] = self.request.user
        # import ipdb; ipdb.set_trace()
        return kw

    def get_context_data(self, **kwargs):
        context = super(EditTransferView, self).get_context_data(**kwargs)
        context['panel_header'] = 'Transfer Details'
        return context

class EditPromoView(GroupRequiredMixin, UpdateView):
    model = Employee
    # fields = '__all__'
    group_required = u'area_apms'
    form_class = transact_form.EmpPromoForm
    template_name = 'transaction/edit_employee.html'
    
    def get_success_url(self):
        print('success_url='+self.request.GET.get('next'))
        return self.request.GET.get('next') 

    def dispatch(self, request, *args, **kwargs):
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        emp_obj = Employee.objects.get(pk=self.kwargs['pk'])
        if emp_obj.e_unit_roll.u_code[1:3] != request.user.username[0:2] and emp_obj.e_unit_roll.u_code[1:3]!='99' and request.user.username not in ['iedstaff','iedhq']:
            # return HttpResponseForbidden(u"You dont have permission to edit other Area records.")
            return HttpResponseForbidden(index_403(request))

        handler = super(EditPromoView, self).dispatch(request, *args, **kwargs)
        return handler
        
    def get_form_kwargs(self):
        kw = super(EditPromoView, self).get_form_kwargs()
        kw['req_username'] = self.request.user.username # the trick!
        kw['curr_user'] = self.request.user
        # import ipdb; ipdb.set_trace()
        return kw

    def get_context_data(self, **kwargs):
        context = super(EditPromoView, self).get_context_data(**kwargs)
        context['panel_header'] = 'Promotion Details'
        return context

class EditTerminateView(GroupRequiredMixin, UpdateView):
    model = Employee
    # fields = '__all__'
    group_required = u'area_apms'
    form_class = transact_form.EmpTerminateForm
    template_name = 'transaction/edit_employee.html'
    
    def get_success_url(self):
        print('success_url='+self.request.GET.get('next'))
        return self.request.GET.get('next') 

    def dispatch(self, request, *args, **kwargs):
        # Only allow editing if current user is owner
        # import ipdb; ipdb.set_trace()
        
        if check_user_permission(self.kwargs['pk'],request.user.username):
            return HttpResponseForbidden(index_403(request))

        handler = super(EditTerminateView, self).dispatch(request, *args, **kwargs)
        return handler
        
    def get_form_kwargs(self):
        kw = super(EditTerminateView, self).get_form_kwargs()
        kw['req_username'] = self.request.user.username # the trick!
        kw['curr_user'] = self.request.user
        # import ipdb; ipdb.set_trace()
        return kw

    def get_context_data(self, **kwargs):
        context = super(EditTerminateView, self).get_context_data(**kwargs)
        context['panel_header'] = 'Termination Details'
        return context

def employee_detail(request, pk):
    emp = Employee.objects.get(pk=pk)
    emp_promotion = PromotionHistory.objects.filter(p_eis=emp)
    emp_transfer = TransferHistory.objects.filter(th_eis=emp)
    promotion_table = EmpPromotionTable(emp_promotion);
    transfer_table = EmpTransferTable(emp_transfer);

    return render(request, 'transaction/employee_detail.html', {
        'panel_header': 'Employee Detail',
        'emp':emp,
        'promotion_table':promotion_table,
        'transfer_table':transfer_table
    })

present = dt.date.today()
fiscal_yr = present.year
if present.month < 4:
    fiscal_yr = present.year-1
fiscal_st = dt.date(fiscal_yr,4,1)
fiscal_end = dt.date(fiscal_yr+1,3,30)
prev_fiscal_st = dt.date(fiscal_yr-1,4,1)
prev_fiscal_end = dt.date(fiscal_yr,3,30)

@user_passes_test(in_apm_group)
def emp_unit_addi_redu(request,code):
    print('emp_add_red: code=',code)

    qs_add = Employee.objects.raw(query.ADDITION.format(curr_yr=fiscal_yr,next_yr=fiscal_yr+1,prev_yr=fiscal_yr-1, filter=code))
    # print(query.ADDITION.format(curr_yr=fiscal_yr,next_yr=fiscal_yr+1,prev_yr=fiscal_yr-1, filter=code))
    
    qs_red = Employee.objects.raw(query.REDUCTION.format(curr_yr=fiscal_yr,next_yr=fiscal_yr+1,prev_yr=fiscal_yr-1, filter=code))

    # result_list = list(chain(qs0,qs1,qs2,qs3,qs4,qs5,qs6,qs7))

    table1 = EmpAddRedTable(qs_add);
    table2 = EmpAddRedTable(qs_red);

    return render(request, 'emp_add_red.html', {
        'table1': table1, 
        'table2': table2
    })

