from django.contrib import admin

# Register your models here.
from .models import SubBank, StorageAccount, CheckAccount, ContactInfo, Loan, PayRecord, Staff, Customer, Manager
admin.site.register(SubBank)
admin.site.register(StorageAccount)
admin.site.register(CheckAccount)
admin.site.register(ContactInfo)
admin.site.register(Loan)
admin.site.register(PayRecord)
admin.site.register(Staff)
admin.site.register(Manager)
admin.site.register(Customer)