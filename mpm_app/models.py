from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings

class Area(models.Model):
    a_name = models.CharField(max_length=20)
    a_code = models.IntegerField(primary_key=True)
    a_abbr = models.CharField(max_length=4,default='',null=True)
    def __str__(self):
        return self.a_name+'__'+str(self.a_code)


class Unit(models.Model):
    # status_choices = (("NOT_ACTIVE", "NOT_ACTIVE"), ("ACTIVE", "Not_in_service"))
    u_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    u_name = models.CharField(max_length=20)
    u_type = models.CharField(max_length=2)
    u_code = models.CharField(max_length=7,primary_key=True)
    u_status = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.u_area.a_abbr+'__'+self.u_code+'__'+self.u_name

class Desg(models.Model):
    cadre_choices = (("CD", "CD"), ("XCD", "XCD"))
    d_code = models.CharField(verbose_name="DSCD",max_length=7,primary_key=True)
    d_name = models.CharField(max_length=40)
    d_grade = models.CharField(max_length=10)
    d_gdesig = models.CharField(max_length=40)
    d_gcode = models.CharField(max_length=5)
    d_rank = models.IntegerField()
    d_cadre = models.CharField(choices=cadre_choices, default="CD", max_length=10)
    d_discp = models.CharField(verbose_name="Discpline", max_length=20)
    d_promo = models.CharField(max_length=2, null=True )
    def __str__(self):
        return self.d_code+'__'+self.d_name
        # return self.d_code+'__'+self.d_discp+'__'+self.d_name + '__'+ self.d_grade

appointment_choices = (("A_NA", "NA"),
    ("A_Land_Losers","Appt of Land Losers"),
    ("A_Fresh_Recruitment", "Fresh Recruitment"),
    ("A_Death", "In lieu of Death"),
    ("A_Disability","In lieu of perm Disability"),
    ("A_Female_VRS", "Female VRS"),
    ("A_Reinstt_Rejoin", "Reinstt/Rejoin"),
    ("A_Other_tranfer", "Other reason(Inter Co transfer)"))
termination_choices = (("T_NA", "NA"),
    ("T_Retirement", "Retirement"),
    ("T_Resignation","Resignation"),
    ("T_Unfit", "Medically Unfit"),
    ("T_Death", "Death"),
    ("T_Female_VRS", "Female VRS"),
    ("T_VRS_BPE", "VRS BPE"),
    ("T_Dismissal", "Dismissal/Termination"),
    ("T_Other_reason", "Other reason(Inter Co transfer)"))
status_choices = (("In_service", "In_service"), ("Not_in_service", "Not_in_service"))
gender_choices = (("Male", "Male"), ("Female", "Female"))


class Employee(models.Model):

    e_eis = models.CharField(verbose_name="EIS No",max_length=15, primary_key=True)
    e_regsno = models.CharField(verbose_name="Token No",max_length=15, null=True,  blank=True)
    e_name = models.CharField(verbose_name = "Full Name",max_length=40)
    e_dob = models.DateField(verbose_name="Date of Birth", blank=True)
    e_gender = models.CharField(verbose_name="Gender",choices=gender_choices, default="Male", max_length=10)
    e_desg = models.ForeignKey(Desg,verbose_name="Designation",related_name='desg_code', on_delete=models.CASCADE)
    e_unit_roll = models.ForeignKey(Unit,verbose_name="On-Roll Unit", on_delete=models.CASCADE, related_name='e_unit_roll')
    e_unit_work = models.ForeignKey(Unit,verbose_name="Working Unit", on_delete=models.CASCADE, related_name='e_unit_work')

    e_doj  = models.DateField(verbose_name="Service Join Date",null=True, blank=True)
    e_dot  = models.DateField(verbose_name="Service Termination Date",null=True,  blank=True)
    e_join = models.CharField(verbose_name="Service Join Type",choices=appointment_choices, default="NA", max_length=20)
    e_termi = models.CharField(verbose_name="Service Termination Type",choices=termination_choices, default="NA", max_length=20)
    e_status = models.CharField(verbose_name="Service Status",choices=status_choices, default="In_service", max_length=20)
    e_dop  = models.DateField(verbose_name="Last promo. Date",null=True, blank=True) # date of last promotion

    def clean(self):
        if self.e_doj is not None and self.e_dot is not None and self.e_dot < self.e_doj:
            raise ValidationError(_('Termination Date is earlier than Join Date'))

        if self.e_doj is not None and self.e_dob is not None and self.e_doj < self.e_dob:
            raise ValidationError(_('Join Date is earlier than Birth Date'))

        if self.e_dot is not None and self.e_dob is not None and self.e_dot < self.e_dob:
            raise ValidationError(_('Termination Date is earlier than Birth Date'))
        
        # import ipdb; ipdb.set_trace()
        if self.e_unit_roll_id is not None and self.e_unit_work_id is not None and self.e_unit_roll.u_code[1:3] != self.e_unit_work.u_code[1:3]:
            raise ValidationError(_('Working Unit should match area of On-roll unit'))

        # import ipdb; ipdb.set_trace()

class AdditionCat(models.Model):
    ac_value= models.CharField(verbose_name="value",max_length=15, primary_key=True)
    ac_name = models.CharField(verbose_name="name",max_length=40)

class TerminationCat(models.Model):
    tc_value= models.CharField(verbose_name="value",max_length=15, primary_key=True)
    tc_name = models.CharField(verbose_name="name",max_length=40)

class Addition(models.Model):
    a_eis = models.ForeignKey(Employee,verbose_name="Employee", on_delete=models.CASCADE)
    a_reason = models.ForeignKey(AdditionCat,verbose_name="Category", on_delete=models.CASCADE)
    a_date = models.DateField(verbose_name="Addition Date")
    a_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
    a_edit_on = models.DateTimeField(verbose_name="Edit time")

class Termination(models.Model):
    t_eis = models.ForeignKey(Employee,verbose_name="Employee", on_delete=models.CASCADE)
    t_reason = models.ForeignKey(TerminationCat,verbose_name="Category", on_delete=models.CASCADE)
    t_date = models.DateField(verbose_name="Termination Date")
    t_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
    t_edit_on = models.DateTimeField(verbose_name="Edit time")

transfer_choices = (("Transfer_In", "Transfer In"), ("Transfer_Out", "Transfer Out"))
class TransferHistory(models.Model):
    th_eis = models.ForeignKey(Employee,verbose_name="Employee", on_delete=models.CASCADE)
    th_unit = models.ForeignKey(Unit,verbose_name="On-Roll Unit", on_delete=models.CASCADE)
    th_category = models.CharField(verbose_name="Category",choices=transfer_choices, default="Transfer_In", max_length=20)
    th_date = models.DateField(verbose_name="Tranfer Date")
    th_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
    th_edit_on = models.DateTimeField(verbose_name="Edit time")

class PromotionHistory(models.Model):
    p_eis = models.ForeignKey(Employee,verbose_name="Employee", on_delete=models.CASCADE)
    p_desg = models.ForeignKey(Desg,verbose_name="Designation", on_delete=models.CASCADE)
    p_date = models.DateField(verbose_name="Promote Date")
    p_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Edited by")
    p_edit_on = models.DateTimeField(verbose_name="Edit time")

class Choices(models.Model):
    c_value= models.CharField(verbose_name="value",max_length=15, primary_key=True)
    c_name = models.CharField(verbose_name="name",max_length=40)
    c_category = models.CharField(verbose_name="category",max_length=40)

# trail_choices = (("Join", "Join"), ("Terminate", "Terminate"), ("Transfer_In", "Transfer_Out"),)
# class EmployeeTrail(models.Model):

#     et_employee = models.ForeignKey(Employee,verbose_name="Employee",related_name='emp', on_delete=models.CASCADE)
#     et_type     = models.CharField(verbose_name = "Type",max_length=40,choices=trail_choices, default="Join")


# class EmplAudit(models.Model):
#     ea_eis = models.ForeignKey(Employee,verbose_name="Employee", on_delete=models.CASCADE)
#     es_eis = 

    # def get_absolute_url(self):
    #     return reverse('emp_edit', kwargs={'pk': self.pk})
