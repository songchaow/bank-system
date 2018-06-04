from django import forms
from django.forms.fields import DateField, CharField, DateTimeField
from django.forms import ModelChoiceField, DateInput, ModelMultipleChoiceField
from .models import SubBank, Staff, Manager, Customer, ContactInfo, StorageAccount, CheckAccount

class SubBankForm(forms.ModelForm):
    class Meta:
        model = SubBank
        fields = ['name','city']

class MyDateInput(DateInput):
    input_type = 'date'


# used for staff search
class StaffSearchForm(forms.ModelForm):

    hire_after = DateField(label='在此之后就职：',required=False, widget=MyDateInput())
    bank = ModelChoiceField(SubBank.objects.all(),label='所属支行',required=False)
    name = CharField(label='职工姓名',max_length=Staff._meta.get_field('name').max_length,required=False)
    class Meta:
        model = Staff
        fields = ['name','bank']

# used for staff details or edit process
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name','home_addr','tel_num','hire_date','bank','mgr']

# used for customer search
class CustomerSearchForm(forms.ModelForm):
    customer_id = CharField(label='身份证号包含',required=False,max_length=18)
    name = CharField(label='姓名',max_length=Customer._meta.get_field('name').max_length,required=False)
    tel_num = CharField(label='联系电话',max_length=Customer._meta.get_field('tel_num').max_length,required=False)
    home_addr = CharField(label='家庭住址',max_length=Customer._meta.get_field('home_addr').max_length,required=False)

    class Meta:
        model = Customer
        fields = ['customer_id','name','tel_num','home_addr']

# used for customer add/display
# contact is isolated
class CustomerForm(forms.ModelForm):
    prefix = 'customer'
    class Meta:
        model = Customer
        fields = ['customer_id','name','tel_num','home_addr','relation_staff']

class ContactForm(forms.ModelForm):
    prefix = 'contact'
    class Meta:
        model = ContactInfo
        fields = ['name','tel_num','email','relation']

class AccountForm(forms.Form):
    create_after = DateTimeField(label='在此之后创建：',required=False, widget=MyDateInput())
    name = CharField(label='开户人姓名',max_length=Customer._meta.get_field('name').max_length,required=False)
    bank = ModelChoiceField(SubBank.objects.all(),label='所属支行',required=False)

class SAccountCreateForm(forms.ModelForm):
    owners = ModelMultipleChoiceField(Customer.objects.all())
    class Meta:
        model = StorageAccount
        fields = '__all__'

class CAccountCreateForm(forms.ModelForm):
    owners = ModelMultipleChoiceField(Customer.objects.all())
    class Meta:
        model = StorageAccount
        fields = '__all__'

