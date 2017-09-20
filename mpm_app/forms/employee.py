from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Row, Div
from crispy_forms.bootstrap import InlineField, FormActions , StrictButton
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.forms.widgets import SelectDateWidget


from mpm_app.forms.bootstrap import SubmitCancelFormHelper, ModelFormWithHelper

from mpm_app.models import Employee, Desg, Unit

appointment_choices = (("Land_oustee", "Land_oustee"), ("New_appointee", "New_appointee"), ("NA", "NA"))
termination_choices = (("Retirement", "Retirement"), ("Death", "Death"),
                      ("VRS", "VRS"), ("NA", "NA"))
status_choices = (("In_Service", "In_Service"), ("Not_in_service", "Not_in_service"))
gender_choices = (("Male", "Male"), ("Female", "Female"))

class EmployeeListFormHelper(FormHelper):    
    form_id = 'customer-search-form'
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    field_class = 'col-xs-3'
    label_class = 'col-xs-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True

    layout = Layout(
                Fieldset(
                    '<i class="fa fa-search"></i> Search Employee Records',       
                    InlineField('e_gender'),
                    InlineField('e_desg__d_discp'),
                    InlineField('e_desg__d_code'),
                ),
                FormActions(
                    StrictButton(
                        '<i class="fa fa-search"></i> Search', 
                        type='submit',
                        css_class='btn-primary',
                        style='margin-top:10px;')
                )
    )

class EmployeeFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
            Div(
                Div('e_desg__d_discp' , css_class='col-md-3'),
                Div('e_desg__d_code', css_class='col-md-3'),
                Div('e_unit_roll__u_code', css_class='col-md-3'),
                Div('e_unit_work__u_code', css_class='col-md-3'), css_class='row'
            ),  
            Div(
                Div('e_regsno' , css_class='col-md-3'),
                Div('e_eis' , css_class='col-md-3'),
                Div('e_name' , css_class='col-md-3'),
                Div('e_gender' , css_class='col-md-3'), css_class='row'
            ),
            Div(
                Div('e_status' , css_class='col-md-3'),
                Div('e_dob' , css_class='col-md-3'),
                Div('e_join' , css_class='col-md-3'),
                Div('e_termi' , css_class='col-md-2'),
                Div(Submit('submit', 'Apply Filter'), css_class='col-md-1'), css_class='row'
            ),

            # Div(
            #     Div(Submit('submit', 'Apply Filter'), css_class='col-md-12'), css_class='row'
            # )
        )

class EmpEditForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",disabled=True)
    # e_name = forms.CharField()
    e_regsno = forms.CharField(label = "Unit Roll No:",required=False)
    # e_status = forms.CharField(label = "Service Status:")
    e_termi = forms.ChoiceField(label = "Service Termination Type:",required=False, choices=termination_choices)
    e_join = forms.ChoiceField(label = "Service Join Type:",required=False, choices=appointment_choices)
    e_doj = forms.DateField(label = "Service Join Date:",required=False,
        widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
    ),)
    e_dot = forms.DateField(label = "Service Termination Date:", required=False,  widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
    ),)
    e_dob = forms.DateField(label = "Date of Birth:", widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
    ),)
    # e_gender = forms.CharField(label = "Gender:",)
    form_action = './?next={{ redirect_to }}'
    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),widget=autocomplete.ModelSelect2(url='desg-autocomplete'))
    e_unit_roll =  forms.ModelChoiceField(label = "On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        widget=autocomplete.ModelSelect2(url='unit-autocomplete',
            # attrs={'data-minimum-input-length': 3,}
            ))
    e_unit_work =  forms.ModelChoiceField(label = "Working Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),widget=autocomplete.ModelSelect2(url='unit-autocomplete'))
    
    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno',  'e_status', 'e_termi',
            'e_gender','e_desg','e_unit_roll','e_unit_work','e_doj',
            'e_dot','e_join','e_dob','e_gender']
 
    def __init__(self, *args, **kwargs):
        super(EmpEditForm, self).__init__(*args, **kwargs)
 
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

 
class EmpCreateForm(forms.ModelForm):
    empty_dt_label = ("Year", "Month", "Day"),
    e_eis = forms.CharField(label = "EIS/NEIS:",)
    # e_name = forms.CharField()
    e_regsno = forms.CharField(label = "Unit Roll No:",required=False)
    # e_status = forms.CharField(label = "Service Status:")
    e_termi = forms.ChoiceField(label = "Service Termination Type:",required=False, choices=termination_choices)
    e_join = forms.ChoiceField(label = "Service Join Type:",required=False, choices=appointment_choices)
    e_doj = forms.DateField(label = "Service Join Date:",required=False,
        widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
    ),)
    e_dot = forms.DateField(label = "Service Termination Date:", required=False,  widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
    ),)
    e_dob = forms.DateField(label = "Date of Birth:", widget=SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
    ),)
    # e_gender = forms.CharField(label = "Gender:",)

    e_desg =  forms.ModelChoiceField(label = "Designation:", queryset=Desg.objects.all().order_by('d_discp','d_gdesig','d_rank'),widget=autocomplete.ModelSelect2(url='desg-autocomplete'))
    e_unit_roll =  forms.ModelChoiceField(label = "On-Roll Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),
        widget=autocomplete.ModelSelect2(url='unit-autocomplete',
            # attrs={'data-minimum-input-length': 3,}
            ))
    e_unit_work =  forms.ModelChoiceField(label = "Working Unit:", queryset=Unit.objects.filter(u_status__isnull=True).order_by('u_area','u_type','u_name'),widget=autocomplete.ModelSelect2(url='unit-autocomplete'))
    
    class Meta:
        model = Employee
        fields = ['e_eis', 'e_name', 'e_regsno',  'e_status', 'e_termi',
            'e_gender','e_desg','e_unit_roll','e_unit_work','e_doj',
            'e_dot','e_join','e_dob','e_gender']
 
    def __init__(self, *args, **kwargs):
        super(EmpCreateForm, self).__init__(*args, **kwargs)
 
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
    def save(self, *args, **kw):
        print(kw)
        instance = super(EmpCreateForm,self).save(commit=False)
        instance.save()
        return instance
        # redirect('.')