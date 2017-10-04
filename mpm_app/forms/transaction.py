from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Row, Div
from crispy_forms.bootstrap import InlineField, FormActions , StrictButton
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.forms.widgets import SelectDateWidget
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime as dt
from django.utils import timezone

from mpm_app.forms.bootstrap import SubmitCancelFormHelper, ModelFormWithHelper
from mpm_app.models import Employee, Desg, Unit, Addition, Termination, TransferHistory, PromotionHistory, TerminationCat


class MySelectDateWidget(SelectDateWidget):
    def create_select(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        result = super(MySelectDateWidget, self).create_select(*args, **kwargs)
        self.is_required = old_state
        return result


class EmpAddForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",)
    e_regsno = forms.CharField(label = "Token no:",required=False)
    # e_status = forms.CharField(label = "Service Status:",disabled=True)
    # e_join = forms.ChoiceField(label = "Service Join Type:",required=True, choices=appointment_choices)
    e_doj = forms.DateField(label = "Service Join Date:",required=True,
        widget=MySelectDateWidget(
            years=range(dt.date.today().year-65, dt.date.today().year+1),
            empty_label=("Year", "Month", "Day"),
    ),)
    e_dob = forms.DateField(label = "Date of Birth:", widget=MySelectDateWidget(
            years=range(dt.date.today().year-65, dt.date.today().year+1),
            empty_label=("Year", "Month", "Day"),
    ),)
    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        )
    e_unit_roll = forms.ModelChoiceField(label = "On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
        )
    e_unit_work = forms.ModelChoiceField(label = "Working Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete')
        )

    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno',  
        # 'e_status',
            'e_gender','e_desg','e_unit_roll','e_unit_work','e_doj','e_join','e_dob','e_gender']

    def clean(self):
        cleaned_data = super(EmpAddForm, self).clean()
        if cleaned_data.get("e_unit_roll"):
            e_unit_roll = cleaned_data.get("e_unit_roll").u_code
            if e_unit_roll[1:3] != self.req_username[0:2] and e_unit_roll[1:3]!='99' and self.req_username not in ['iedstaff','iedhq']:
                raise ValidationError("You dont have permission to edit other Area records.")
        
    def __init__(self, *args, **kwargs):
        self.req_username = kwargs.pop('req_username', None)
        self.curr_user = kwargs.pop('curr_user', None)
        super(EmpAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        # InlineRadios('e_status'),
        self.helper.layout = Layout(
            Div(
                Div('e_eis', 'e_desg','e_unit_roll','e_unit_work', css_class='col-md-4'),
                Div('e_name', 'e_dob',InlineRadios('e_gender'), css_class='col-md-4'),
                Div('e_regsno','e_join','e_doj', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )
    def save(self, *args, **kw):
        print(kw)
        # import ipdb; ipdb.set_trace()
        instance = super(EmpAddForm,self).save(commit=False)
        instance.save()
        dt = self.cleaned_data
        Addition.objects.create(a_eis=instance, a_unit=instance.e_unit_roll,a_reason=dt['e_join'], a_date=dt['e_doj'], a_edit_by= self.curr_user, a_edit_on=timezone.now() )
        return instance
        # redirect('.')

class EmpEditForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",disabled=True)
    # e_name = forms.CharField()
    e_regsno = forms.CharField(label = "Token no:",required=False)
    e_status = forms.CharField(label = "Service Status:",disabled=True)
    e_termi = forms.CharField(disabled=True,label = "Service Termination Type:",required=False, )
    e_join = forms.CharField(disabled=True,label = "Service Join Type:",required=False, )
    e_doj = forms.DateField(label = "Service Join Date:",required=False,disabled=True)
    e_dot = forms.DateField(label = "Service Termination Date:", required=False,disabled=True)
    e_dob = forms.DateField(label = "Date of Birth:", widget=SelectDateWidget(
            years=range(1950, dt.date.today().year+1),
            empty_label=("Year", "Month", "Day"),
    ),)
    # e_gender = forms.CharField(label = "Gender:",)
    form_action = './?next={{ redirect_to }}'
    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        disabled=True)
    e_unit_roll = forms.ModelChoiceField(label = "On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
        disabled=True)
    e_unit_work = forms.ModelChoiceField(label = "Working Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete')
        )
    
    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno',  'e_status', 'e_termi',
            'e_gender','e_desg','e_unit_roll','e_unit_work','e_doj',
            'e_dot','e_join','e_dob','e_gender']
 
    def __init__(self, *args, **kwargs):
        super(EmpEditForm, self).__init__(*args, **kwargs)
        
        # import ipdb; ipdb.set_trace()
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('e_eis', 'e_desg','e_unit_roll','e_unit_work', css_class='col-md-4'),
                Div('e_name', 'e_dob',InlineRadios('e_gender'),InlineRadios('e_status'), css_class='col-md-4'),
                Div('e_regsno','e_join','e_doj','e_termi','e_dot', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

class EmpTransferForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",disabled=True)
    e_name = forms.CharField(disabled=True)
    e_regsno = forms.CharField(label = "Token no:",disabled=True,required=False)
    # e_gender = forms.CharField(label = "Gender:",)
    form_action = './?next={{ redirect_to }}'
    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        disabled=True)
    e_unit_roll = forms.ModelChoiceField(label = "Current On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
        disabled=True)
    th_unit = forms.ModelChoiceField(label = "Transfer To Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,}),
        disabled=False)
    th_date = forms.DateField(label = "Date of Transfer:", widget=SelectDateWidget(
            years=range(1990, dt.date.today().year+1),
            empty_label=("Year", "Month", "Day"),
    ),)
    
    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno','e_desg','e_unit_roll',
            'th_unit', 'th_date']
 
    def __init__(self, *args, **kwargs):
        self.req_username = kwargs.pop('req_username', None)
        self.curr_user = kwargs.pop('curr_user', None)
        super(EmpTransferForm, self).__init__(*args, **kwargs)
        
        # import ipdb; ipdb.set_trace()
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('th_unit','th_date',  css_class='col-md-4'),
                Div('e_eis','e_name', 'e_regsno', css_class='col-md-4'),
                Div('e_desg','e_unit_roll', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

    def clean(self):
        cleaned_data = super(EmpTransferForm, self).clean()
        th_unit = cleaned_data.get("th_unit").u_code
        e_unit_roll = cleaned_data.get("e_unit_roll").u_code
        if  e_unit_roll[1:3] != self.req_username[0:2]  and th_unit[1:3]!='99' and self.req_username not in ['iedstaff','iedhq']:
            raise ValidationError("You dont have permission to tranfer record other Area. Transfer to Floating/Temp unit instead")
        
        if th_unit == e_unit_roll :
             raise ValidationError("Current Unit and Transfer unit are same")
        
    def save(self, *args, **kw):
        print(kw)
        dt = self.cleaned_data
        # import ipdb; ipdb.set_trace()
        instance = super(EmpTransferForm,self).save(commit=False)
        prev_unit = instance.e_unit_roll
        instance.e_unit_roll = dt['th_unit']
        instance.e_unit_work = dt['th_unit']
        instance.save()
        TransferHistory.objects.create(th_eis=instance, th_date=dt['th_date'],th_unit=dt['th_unit'], th_prev_unit=prev_unit, th_edit_by= self.curr_user, th_edit_on=timezone.now() )
        return instance


class EmpPromoForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",disabled=True)
    e_name = forms.CharField(disabled=True)
    e_regsno = forms.CharField(label = "Token no:",disabled=True,required=False)
    # e_gender = forms.CharField(label = "Gender:",)
    form_action = './?next={{ redirect_to }}'
    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        disabled=True)
    e_unit_roll = forms.ModelChoiceField(label = "Current On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
        disabled=True)
    p_desg =  forms.ModelChoiceField(label = "Promote to:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        disabled=False)
    p_date = forms.DateField(label = "Date of Transfer:", widget=SelectDateWidget(
            years=range(1990, dt.date.today().year+1),
            empty_label=("Year", "Month", "Day"),
    ),)
    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno','e_desg','e_unit_roll',
            'p_desg', 'p_date']
 
    def __init__(self, *args, **kwargs):
        self.req_username = kwargs.pop('req_username', None)
        self.curr_user = kwargs.pop('curr_user', None)
        super(EmpPromoForm, self).__init__(*args, **kwargs)
        
        # import ipdb; ipdb.set_trace()
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('p_desg','p_date',  css_class='col-md-4'),
                Div('e_eis','e_name', 'e_regsno', css_class='col-md-4'),
                Div('e_desg','e_unit_roll', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

    def clean(self):
        cleaned_data = super(EmpPromoForm, self).clean()
        p_desg = cleaned_data.get("p_desg").d_code
        e_desg = cleaned_data.get("e_desg").d_code
        
        if p_desg == e_desg :
             raise ValidationError("Current desg is same as prev desg")
        
    def save(self, *args, **kw):
        print(kw)
        dt = self.cleaned_data
        # import ipdb; ipdb.set_trace()
        instance = super(EmpPromoForm,self).save(commit=False)
        instance.e_desg = dt['p_desg']
        instance.save()
        PromotionHistory.objects.create(p_eis=instance,p_unit=instance.e_unit_roll, p_date=dt['p_date'], p_desg=dt['p_desg'], p_edit_by= self.curr_user, p_edit_on=timezone.now() )
        return instance
 

class EmpTerminateForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",disabled=True)
    e_name = forms.CharField(disabled=True)
    e_regsno = forms.CharField(label = "Token no:",disabled=True,required=False)
    # e_gender = forms.CharField(label = "Gender:",)
    form_action = './?next={{ redirect_to }}'
    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        disabled=True)
    e_unit_roll = forms.ModelChoiceField(label = "Current On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        # widget=autocomplete.ModelSelect2(url='unit-autocomplete',attrs={'data-minimum-input-length': 3,})
        disabled=True)
    t_reason =  forms.ModelChoiceField(label = "Reason/Category:", queryset=TerminationCat.objects.all(),
        # widget=autocomplete.ModelSelect2(url='desg-autocomplete')
        disabled=False)
    t_date = forms.DateField(label = "Date of Transfer:", widget=SelectDateWidget(
            years=range(1990, dt.date.today().year+1),
            empty_label=("Year", "Month", "Day"),
    ),)
    
    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno','e_desg','e_unit_roll',
            't_reason', 't_date']
 
    def __init__(self, *args, **kwargs):
        self.req_username = kwargs.pop('req_username', None)
        self.curr_user = kwargs.pop('curr_user', None)
        super(EmpTerminateForm, self).__init__(*args, **kwargs)
        
        # import ipdb; ipdb.set_trace()
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        # self.helper.form_action = '.'
        self.helper.layout = Layout(
            Div(
                Div('t_reason','t_date',  css_class='col-md-4'),
                Div('e_eis','e_name', 'e_regsno', css_class='col-md-4'),
                Div('e_desg','e_unit_roll', css_class='col-md-4'), css_class='row'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            )
        )

    def clean(self):
        cleaned_data = super(EmpTerminateForm, self).clean()

        if cleaned_data.get("e_termi"):
            t_reason = cleaned_data.get("t_reason").tc_value
            e_termi = cleaned_data.get("e_termi").tc_value   
            if t_reason == e_termi :
                raise ValidationError("Current Reason is same as prev reason")
        
    def save(self, *args, **kw):
        print(kw)
        dt = self.cleaned_data
        # import ipdb; ipdb.set_trace()
        instance = super(EmpTerminateForm,self).save(commit=False)
        instance.e_termi = dt['t_reason']
        instance.e_dot = dt['t_date']
        instance.e_status = 'Not_in_service'
        instance.save()
        Termination.objects.create(t_eis=instance,t_unit=instance.e_unit_roll, t_date=dt['t_date'], t_reason=dt['t_reason'], t_edit_by= self.curr_user, t_edit_on=timezone.now() )
        return instance
 