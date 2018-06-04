from django.db import models
import datetime
from django.utils import timezone

class SubBank(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Account(models.Model):
    # is_storage = models.BooleanField(default=True)
    money_left = models.DecimalField(verbose_name='余额',max_digits=30,decimal_places=8)
    open_date = models.DateTimeField(verbose_name='开户日期',auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='最近访问',auto_now=True)
    
    class Meta:
        abstract = True

class StorageAccount(Account):
    interest_rate = models.DecimalField(verbose_name='利率',max_digits=6,decimal_places=5)
    money_type = models.CharField(verbose_name='货币类型',max_length=30)
    bank = models.ForeignKey(SubBank,null=True,on_delete=models.PROTECT,related_name='storage_accounts',verbose_name='所属支行')

class CheckAccount(Account):
    overdraft = models.DecimalField(verbose_name='透支额',max_digits=30,decimal_places=8)
    bank = models.ForeignKey(SubBank,null=True,on_delete=models.PROTECT,related_name='check_accounts',verbose_name='所属支行')

class ContactInfo(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=50)
    tel_num = models.CharField(verbose_name='联系电话',max_length=30)
    email = models.EmailField(verbose_name='邮箱')
    relation = models.CharField(verbose_name='联系人关系',max_length=20)
    def __str__(self):
        return self.name
    
class Staff(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=50)
    home_addr = models.CharField(verbose_name='家庭住址',max_length=100)
    tel_num = models.CharField(verbose_name='联系电话',max_length=30)
    hire_date = models.DateField(verbose_name='雇佣日期',default=datetime.date.today)
    bank = models.ForeignKey(SubBank,on_delete=models.PROTECT,related_name='staffs',verbose_name='工作支行')
    mgr = models.ForeignKey('self',on_delete=models.PROTECT,related_name='sub_staffs',verbose_name='上级经理',null=True,blank=True)
    def __str__(self):
        return self.name

class Manager(Staff):
    staff_id = models.CharField(verbose_name='身份证ID',max_length=18,primary_key=True)




class Customer(models.Model):
    storage_accounts = models.ManyToManyField(StorageAccount,related_name='owners',null=True,blank=True)
    check_accounts = models.ManyToManyField(CheckAccount,related_name='owners',null=True,blank=True)
    customer_id = models.CharField(verbose_name='身份证ID',max_length=18,primary_key=True)
    name = models.CharField(verbose_name='姓名',max_length=50)
    tel_num = models.CharField(verbose_name='联系电话',max_length=30)
    home_addr = models.CharField(verbose_name='家庭住址',max_length=100)
    contact = models.OneToOneField(ContactInfo,models.PROTECT,related_name='+',verbose_name='联系人信息')
    relation_staff = models.ForeignKey(Staff,null=True,on_delete=models.PROTECT,verbose_name='联系员工',related_name='related_customers')
    #loans = models.ManyToManyField(Loan,'owners','owners',verbose_name='拥有贷款',null=True,blank=True)
    def __str__(self):
        return self.name

class Loan(models.Model):
    money = models.DecimalField(verbose_name='贷款金额',max_digits=25,decimal_places=5)
    money_returned = models.DecimalField(verbose_name='已还金额',default=0.0,max_digits=25,decimal_places=5)
    owners = models.ManyToManyField(Customer,'owners','owners',verbose_name='所属用户',blank=True)
    def __str__(self):
        return self.pk

class PayRecord(models.Model):
    money = models.DecimalField(verbose_name='支付金额',max_digits=25,decimal_places=5)
    paydate = models.DateTimeField(default=timezone.now)
    related_loan = models.ForeignKey(Loan,models.CASCADE,related_name='pay_records')

