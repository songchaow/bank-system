from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView, View
from django.template import loader
from django.db.models.query import QuerySet
from django.db.models.deletion import ProtectedError
from django.forms import modelform_factory
from .models import SubBank, Staff, Customer, StorageAccount, CheckAccount, Loan, PayRecord
from .forms import SubBankForm, StaffForm, StaffSearchForm, CustomerSearchForm, CustomerForm, ContactForm, AccountForm, SAccountCreateForm, CAccountCreateForm
from itertools import chain


# Create your views here.

def index(request):
    return HttpResponse(render(request,'bankapp/index.html'))

def subbank(request):
    content = {'bank_list':None}
    return HttpResponse(render(request,'bankapp/subbank.html',content))

def subbank_list(request):
    subbank_name = request.GET.get('subbank_name')
    if(subbank_name is not None):
        results = SubBank.objects.filter(name__icontains=subbank_name)
    else:
        results = SubBank.objects.all()
    template = loader.get_template('bankapp/subbank.html')
    content = {'bank_list':results}
    return HttpResponse(template.render(content,request))

class SubBankDeleteView(DeleteView):
    model = SubBank
    template_name = 'bankapp/bankdelete.html'
    success_url = "/subbank"
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            return HttpResponseBadRequest('该支行存在关联信息，无法删除')
        except Exception as e:
            return HttpResponseBadRequest('出现意料之外的错误，无法删除')

def subbank_edit(request):
    if(request.method=='GET'):
        subbank_id = request.GET.get('subbank_id')
        if(subbank_id is not None):
            # render form with data
            subbank = SubBank.objects.get(id=int(subbank_id))
            if(subbank is None):
                return HttpResponseNotFound('<h1> The subbank is not found. </h1>')
            SubBankForm(request.POST, instance=subbank)
            form = SubBankForm(instance=subbank)
            context = {'page_title':'修改支行信息','form':form,'subbank_id':subbank.id}
        else:
            form = SubBankForm()
            context = {'page_title':'创建支行','form':form,'subbank_id':None}
        return HttpResponse(render(request,'bankapp/bankedit.html',context))
    elif(request.method=='POST'):
        subbank_id = request.GET.get('subbank_id')
        if(subbank_id is not None):
            subbank = SubBank.objects.get(id=int(subbank_id))
            if(subbank is None):
                return HttpResponseNotFound('<h1> The subbank is not found. </h1>')
            form = SubBankForm(request.POST, instance=subbank)
        else:
            form = SubBankForm(request.POST)
        if(form.is_valid()):
            form.save()
            if(subbank_id is not None):
                context = {'page_title':'修改支行信息成功','form':form,'subbank_id':subbank_id}
            else:
                context = {'page_title':'创建支行成功','form':form,'subbank_id':None}
            return HttpResponse(render(request,'bankapp/bankedit.html',context))
        else:
            if(subbank_id is not None):
                context = {'page_title':'修改支行信息失败','form':form,'subbank_id':subbank_id}
            else:
                context = {'page_title':'创建支行失败','form':form}
            return HttpResponse(render(request,'bankapp/bankedit.html',context))
    elif(request.method=='DELETE'):
        pass

class StaffCreateView(CreateView):
    model = Staff
    template_name = 'bankapp/staffcreate.html'
    fields = ['name', 'home_addr', 'tel_num', 'bank', 'mgr']
    success_url = "/staff"
        
class StaffEditViewnew(UpdateView):
    model = Staff
    template_name = 'bankapp/staffedit.html'
    fields = ['name', 'home_addr', 'tel_num', 'bank', 'mgr']
    success_url = "/staff"

class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'bankapp/staffdelete.html'
    success_url = "/staff"

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            return HttpResponseBadRequest('该员工存在关联信息，无法删除')
        except Exception as e:
            return HttpResponseBadRequest('出现意料之外的错误，无法删除')

class StaffIndexView(TemplateView):
    template_name = 'bankapp/staffsearch.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = StaffSearchForm()
        context['object_list'] = None
        return context

class CustomerIndexView(TemplateView):
    template_name = 'bankapp/customersearch.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = CustomerSearchForm()
        context['object_list'] = None
        return context

class StaffListView(ListView):

    model = Staff
    template_name = 'bankapp/staffsearch.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = self.form
        return context

    def get_queryset(self):
        if self.model is not None:
            self.form = StaffSearchForm(self.request.GET)
            if(not self.form.is_valid()):
                queryset = self.model.objects.none()
                return queryset
            queryset = self.model.objects.all()
            name = self.form.cleaned_data.get('name') or None
            bank = self.form.cleaned_data.get('bank') or None
            hire_after = self.form.cleaned_data.get('hire_after') or None
            if(name is not None):
                queryset = queryset.filter(name__icontains=self.form.cleaned_data.get('name'))
            if(bank is not None):
                queryset = queryset.filter(bank=bank)
            if(hire_after is not None):
                queryset = queryset.filter(hire_date__gte=hire_after)
            
        return queryset

class CustomerListView(ListView):
    model = Customer
    template_name = 'bankapp/customersearch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = self.form
        return context

    def get_queryset(self):
        self.form = CustomerSearchForm(self.request.GET)
        if(not self.form.is_valid()):
            queryset = self.model.objects.none()
            return queryset
        queryset = self.model.objects.all()
        customer_id = self.form.cleaned_data.get('customer_id') or None
        name = self.form.cleaned_data.get('name') or None
        tel_num = self.form.cleaned_data.get('tel_num') or None
        home_addr = self.form.cleaned_data.get('home_addr') or None
        if(customer_id is not None):
            queryset = queryset.filter(customer_id__icontains=customer_id)
        if(name is not None):
            queryset = queryset.filter(name__icontains=name)
        if(tel_num is not None):
            queryset = queryset.filter(tel_num__icontains=tel_num)
        if(home_addr is not None):
            queryset = queryset.filter(home_addr__icontains=home_addr)
        return queryset

class CustomerUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk'] or kwargs['id'] or None
        if(pk is None):
            return HttpResponseBadRequest('未指明要更新的客户')
        try:
            customer = Customer.objects.get(pk=pk)
        except Exception as e:
            return HttpResponseBadRequest('未找到要更新的客户')
        custom_form = CustomerForm(instance=customer)
        contact_form = ContactForm(instance=customer.contact)
        context={'custom_form':custom_form,'contact_form':contact_form,'object':customer,'title':'修改客户信息'}
        return HttpResponse(render(request,'bankapp/customeredit.html',context))
        
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk'] or kwargs['id'] or None
        if(pk is None):
            return HttpResponseBadRequest('未指明要更新的客户')
        try:
            customer = Customer.objects.get(pk=pk)
        except Exception as e:
            return HttpResponseBadRequest('未找到要更新的客户')
        custom_form = CustomerForm(self.request.POST,instance=customer)
        contact_form = ContactForm(self.request.POST,instance=customer.contact)
        custom_form.save()
        contact_form.save()
        context={'custom_form':custom_form,'contact_form':contact_form,'object':customer,'title':'修改客户信息成功！'}
        return HttpResponse(render(request,'bankapp/customeredit.html',context))
            
class CustomerCreateView(View):
    def get(self, request, *args, **kwargs):
        custom_form = CustomerForm()
        contact_form = ContactForm()
        context={'custom_form':custom_form,'contact_form':contact_form,'title':'创建新客户'}
        return HttpResponse(render(request,'bankapp/customeredit.html',context))
        
    def post(self, request, *args, **kwargs):
        custom_form = CustomerForm(self.request.POST)
        contact_form = ContactForm(self.request.POST)
        if(custom_form.is_valid() and contact_form.is_valid()):
            contact = contact_form.save()
            customer = custom_form.save(commit=False)
            customer.contact = contact
            customer.save()
        else:
            return HttpResponseBadRequest('所填信息不合法')
        context={'custom_form':custom_form,'contact_form':contact_form,'object':customer,'title':'创建新客户成功！'}
        # return HttpResponse(render(request,'bankapp/customeredit.html',context))
        return HttpResponseRedirect('/customer')
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'bankapp/customerdelete.html'
    success_url = "/customer"
    # additional check
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        a =self.object.loans.count
        b = self.object.loans.count()
        if(self.object.loans.count()>0):
            return HttpResponseBadRequest('该用户已存在贷款，不得注销！')
        if(self.object.storage_accounts.count()>0):
            return HttpResponseBadRequest('该用户存在关联的储蓄账户，不得注销！')
        if(self.object.check_accounts.count()>0):
            return HttpResponseBadRequest('该用户存在关联的支票账户，不得注销！')
        self.object.delete()
        return HttpResponseRedirect(success_url)

# accounts
class AccountIndexView(TemplateView):
    template_name = 'bankapp/accountindex.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AccountForm
        context['object_list'] = None
        s_sum = 0
        c_sum = 0
        for s_account in StorageAccount.objects.all():
            s_sum += s_account.money_left
        for c_account in CheckAccount.objects.all():
            c_sum += c_account.money_left
        context['s_money_sum'] = s_sum
        context['c_money_sum'] = c_sum
        return context

class AccountSearchView(ListView):
    model = StorageAccount
    template_name ='bankapp/accountindex.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = self.form
        s_sum = 0
        c_sum = 0
        for s_account in StorageAccount.objects.all():
            s_sum += s_account.money_left
        for c_account in CheckAccount.objects.all():
            c_sum += c_account.money_left
        context['s_money_sum'] = s_sum
        context['c_money_sum'] = c_sum
        return context
    def get_queryset(self):
        self.form = AccountForm(self.request.GET)
        if(self.request.GET['search']=='搜索储蓄账户'):
            self.model = StorageAccount
        elif(self.request.GET['search']=='搜索支票账户'):
            self.model = CheckAccount
        if(not self.form.is_valid()):
            queryset = self.model.objects.none()
            return queryset
        queryset = self.model.objects.all()
        create_after = self.form.cleaned_data.get('create_after') or None
        name = self.form.cleaned_data.get('name') or None
        if(name is None):
            customers = None
        else:
            customers = Customer.objects.filter(name__icontains=name)
        bank = self.form.cleaned_data.get('bank') or None
        if(customers is not None):
            queryset = queryset.filter(owners__in=customers)
        if(bank is not None):
            queryset = queryset.filter(bank=bank)
        if(create_after is not None):
            queryset = queryset.filter(open_date__gte=create_after)
        for account in queryset:
            account.owner_str = ' '.join([owner.name for owner in account.owners.all()])
            account.account_type = '储蓄账户' if isinstance(account,StorageAccount) else '支票账户'
        return queryset

class SAccountCreateView(CreateView):
    model = StorageAccount
    template_name = 'bankapp/accountcreate.html'
    #fields = '__all__'
    form_class = SAccountCreateForm
    success_url = "/account"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_type'] = '储蓄账户'
        return context
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        for owner in form.cleaned_data['owners']:
            self.object.owners.add(owner)
        return super().form_valid(form)

class SAccountUpdateView(UpdateView):
    model = StorageAccount
    template_name = 'bankapp/accountedit.html'
    form_class = SAccountCreateForm
    success_url = "/account"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_type'] = '储蓄账户'
        return context
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.owners.clear()
        for owner in form.cleaned_data['owners']:
            self.object.owners.add(owner)
        return super().form_valid(form)

class CAccountUpdateView(UpdateView):
    model = CheckAccount
    template_name = 'bankapp/accountedit.html'
    form_class = CAccountCreateForm
    success_url = "/account"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_type'] = '支票账户'
        return context
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.owners.clear()
        for owner in form.cleaned_data['owners']:
            self.object.owners.add(owner)
        return super().form_valid(form)

class CAccountCreateView(CreateView):
    model = CheckAccount
    template_name = 'bankapp/accountcreate.html'
    #fields = '__all__'
    form_class = CAccountCreateForm
    success_url = "/account"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_type'] = '支票账户'
        return context
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        for owner in form.cleaned_data['owners']:
            self.object.owners.add(owner)
        return super().form_valid(form)


class SAccountDeleteView(DeleteView):
    model = StorageAccount
    template_name = 'bankapp/accountdelete.html'
    success_url = '/account'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     form_class = modelform_factory(self.model,fields=['money_left','open_date','last_modified','interest_rate','money_type','bank'])
    #     form = form_class(instance = self.object)
    #     for field in form.Meta.fields:
    #         form.Meta.fields[field].widget.attrs['readonly'] = True
    #     context['form'] = form
    #     return context

class LoanIndexView(TemplateView):
    # displlays all loans
    template_name = 'bankapp/loanindex.html'
    def get_context_data(self, **kwargs):
        loans = Loan.objects.all()
        sum_all = 0
        sum_ret = 0
        for loan in loans:
            loan.owner_str = ' '.join([owner.name for owner in loan.owners.all()])
            sum_all +=loan.money
            sum_ret += loan.money_returned
        context = super().get_context_data(**kwargs)
        context['object_list'] = loans
        context['money_all'] = sum_all
        context['money_returned'] = sum_ret
        return context

class PayRecordListView(ListView):
    # displays all payrecords subordinate to one particular Loan
    model = PayRecord
    template_name = 'bankapp/payrecordlist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_id'] = self.kwargs.get('pk')
        return context
    def get_queryset(self):
        pk = self.kwargs.get('pk') or None
        if pk is None:
            return PayRecord.objects.none()
        loan = Loan.objects.get(pk=pk) or None
        if(loan is None):
            return PayRecord.objects.none()
        return loan.pay_records.all()

class PayRecordCreateView(CreateView):
    model = PayRecord
    template_name = 'bankapp/payrecordcreate.html'
    form_class = modelform_factory(PayRecord,fields=['money','paydate'])
    success_url = '/loan'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_id'] = self.kwargs.get('pk')
        return context
    def form_valid(self, form):
        loan_pk = self.kwargs.get('pk') or None
        if(loan_pk is None):
            return HttpResponseBadRequest('pk of Loan must be provided.')
        loan = Loan.objects.get(pk=loan_pk) or None
        if(loan is None):
            return HttpResponseBadRequest('The loan required is not found')
        payrecord = form.save(commit=False)
        if(payrecord.money == 0):
            return HttpResponseBadRequest('妈的你根本就没有还钱！')
        sumafter = loan.money_returned + payrecord.money
        if(sumafter>loan.money):
            return HttpResponseBadRequest('还多了哦！请重新选择金额')
        loan.money_returned = sumafter
        loan.save()
        payrecord.related_loan = loan
        payrecord.save()
        return super().form_valid(form)



class LoanCreateView(CreateView):
    model = Loan
    template_name = 'bankapp/loancreate.html'
    fields = '__all__'
    success_url = "/loan"

class LoanDeleteView(DeleteView):
    model = Loan
    template_name = 'bankapp/loandelete.html'
    success_url = '/loan'
    def delete(self, request, *args, **kwargs):
        # examine whether this loan is paid off
        self.object = self.get_object()
        success_url = self.get_success_url()
        if(self.object.money_returned>0 and self.object.money_returned<self.object.money):
            return HttpResponseBadRequest('贷款未还清')
        self.object.delete()
        return HttpResponseRedirect(success_url)