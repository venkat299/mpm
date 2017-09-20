from django.db import models
from django.core.urlresolvers import reverse

class Area(models.Model):
    a_name = models.CharField(max_length=20)
    a_code = models.IntegerField(primary_key=True)


class Unit(models.Model):
    # status_choices = (("NOT_ACTIVE", "NOT_ACTIVE"), ("ACTIVE", "Not_in_service"))
    u_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    u_name = models.CharField(max_length=20)
    u_type = models.CharField(max_length=2)
    u_code = models.CharField(max_length=7,primary_key=True)
    u_status = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.u_area.a_name+'__'+self.u_name

class Desg(models.Model):
    cadre_choices = (("CD", "CD"), ("XCD", "XCD"))
    d_code = models.CharField(verbose_name="DSCD",max_length=7,primary_key=True)
    d_name = models.CharField(max_length=40)
    d_grade = models.CharField(max_length=10)
    d_gdesig = models.CharField(max_length=40)
    d_rank = models.IntegerField()
    d_cadre = models.CharField(choices=cadre_choices, default="CD", max_length=10)
    d_discp = models.CharField(verbose_name="Discpline", max_length=20)
    d_promo = models.CharField(max_length=2, null=True )
    def __str__(self):
        return self.d_code+'__'+self.d_name
        # return self.d_code+'__'+self.d_discp+'__'+self.d_name + '__'+ self.d_grade

appointment_choices = (("Land_oustee", "Land_oustee"), ("New_appointee", "New_appointee"), ("NA", "NA"))
termination_choices = (("Retirement", "Retirement"), ("Death", "Death"),
                      ("VRS", "VRS"), ("NA", "NA"))
status_choices = (("In_service", "In_service"), ("Not_in_service", "Not_in_service"))
gender_choices = (("Male", "Male"), ("Female", "Female"))

class Employee(models.Model):

    e_eis = models.CharField(verbose_name="EIS No",max_length=15, primary_key=True)
    e_regsno = models.CharField(verbose_name="Unit Roll No",max_length=15, null=True,  blank=True)
    e_name = models.CharField(verbose_name = "Full Name",max_length=40)
    e_dob = models.DateField(verbose_name="Date of Birth", blank=True)
    e_gender = models.CharField(verbose_name="Gender",choices=gender_choices, default="Male", max_length=10)
    e_desg = models.ForeignKey(Desg,verbose_name="Designation",related_name='desg_code', on_delete=models.CASCADE)
    e_unit_roll = models.ForeignKey(Unit,verbose_name="On-Roll Unit", on_delete=models.CASCADE, related_name='onroll_unit')
    e_unit_work = models.ForeignKey(Unit,verbose_name="Working Unit", on_delete=models.CASCADE, related_name='working_unit')

    e_doj  = models.DateField(verbose_name="Service Join Date",null=True, blank=True)
    e_dot  = models.DateField(verbose_name="Service Termination Date",null=True,  blank=True)
    e_join = models.CharField(verbose_name="Service Join Type",choices=appointment_choices, default="NA", max_length=20)
    e_termi = models.CharField(verbose_name="Service Termination Type",choices=termination_choices, default="NA", max_length=20)
    e_status = models.CharField(verbose_name="Service Status",choices=status_choices, default="In_service", max_length=20)


# trail_choices = (("Join", "Join"), ("Terminate", "Terminate"), ("Transfer_In", "Transfer_Out"),)
# class EmployeeTrail(models.Model):

#     et_employee = models.ForeignKey(Employee,verbose_name="Employee",related_name='emp', on_delete=models.CASCADE)
#     et_type     = models.CharField(verbose_name = "Type",max_length=40,choices=trail_choices, default="Join")


# class EmplAudit(models.Model):
#     ea_eis = models.ForeignKey(Employee,verbose_name="Employee", on_delete=models.CASCADE)
#     es_eis = 

    # def get_absolute_url(self):
    #     return reverse('emp_edit', kwargs={'pk': self.pk})