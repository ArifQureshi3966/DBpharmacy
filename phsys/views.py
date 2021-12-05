from django.shortcuts import render,redirect,get_list_or_404, get_object_or_404, reverse
from django.contrib import messages
from phsys.models import GrpName, Users, Payments, AuthUser, AuthGroup, Medicine, Customer, AuthUserGroups, PurchaseMaster, SalesDetails, PurchaseDetail, Parties, SalesMaster,Parties
from invoice.models import Invoice
from django.contrib.auth.models import User, auth, Group
from .forms import *
from .filters import MedicineFilter,CustomerFilter
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.forms import inlineformset_factory
from collections import ChainMap
from django.views import View
from django.db import connection
import pdfkit
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import logout
from django.template import Context, Template
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from pyvirtualdisplay import Display
from weasyprint import HTML, CSS
from django.template.loader import get_template
from pathlib import Path
from django.conf import settings
import os
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.

#Home
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager','Sales Person'])
def index(request):
    purch=PurchaseMaster.objects.all().count()
    sale=SalesMaster.objects.all().count()
    user=User.objects.all().count()
    cus=Customer.objects.all().count()
    med=Medicine.objects.all()
    context = {'purchcount':purch,
                'salecount':sale,
                'usercount':user,
                'cuscount':cus,
                'medicine':med}

    return render(request,'indexan.html',context)

def index2(request):
    return render(request,'index2.html')

def index3(request):
    return render(request,'index3.html')
#Register

def register(request):
    if request.method == 'POST':
        if 'agree-term' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    return redirect('phsys:register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'An account on this email already exists')
                    return redirect('phsys:register')
                else:
                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user.save();
                    messages.info(request,'User Created. Please Log-in')
                    return redirect('login')
            else:
                messages.info(request,'Password not matching')
                return redirect('phsys:register')
            return redirect('phsys:register')
        else:
            messages.info(request,'You cannot proceed without agreeing to our terms')
            return redirect('phsys:register')
        return redirect('phsys:register')
    else:
        return render(request,'register.html')

#Add forms
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def addmed(request):
    if request.method == 'POST':
        medid = request.POST['med_id']
        g_name = request.POST['g_name']
        title = request.POST['title']
        manuf = request.POST['manuf']
        nature = request.POST['nature']
        dose = request.POST['dose']
        price = request.POST['price']

        if Medicine.objects.filter(med_id=medid).exists():
                messages.info(request,'Medicine already exists')
                return redirect('phsys:addmed')

        med = Medicine(med_id=medid, g_name=g_name, m_title=title, m_make=manuf, m_nature=nature, m_doze=dose, m_sprice=price)
        med.save();
        messages.info(request,'Medicine Added')
        return redirect('phsys:addmed')

    else:
        return render(request,'addmed.html')
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def addcus(request):
    if request.method == 'POST':
        cus_id = request.POST['cus_id']
        cus_name = request.POST['cus_name']
        cus_address = request.POST['cus_address']
        cus_cont = request.POST['cus_contact']
        cus_email = request.POST['cus_email']

        if Customer.objects.filter(cusid=cus_id).exists():
                messages.info(request,'Customer already exists')
                return redirect('phsys:customer')

        cus = Customer(cusid=cus_id,cus_name=cus_name,cus_address=cus_address,cus_contact=cus_cont,cus_email=cus_email)
        cus.save();
        messages.info(request,'Customer Added')
        return redirect('phsys:addcus')

    else:
        return render(request,'addcus.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def adduser(request):
        if request.method == 'POST':
            status = request.POST['status']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    return redirect('phsys:register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'An account on this email already exists')
                    return redirect('phsys:register')
                else:
                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user.save();
                    usid = User.objects.get(username=username)
                    us_id=AuthUser.objects.get(id=usid.id)

                    if status == '1':
                        us_id.is_active = True
                        us_id.is_staff = True
                        us_id.is_superuser = True
                        us_id.save()
                    elif status == '2':
                        us_id.is_active = True
                        us_id.is_staff = True
                        us_id.is_superuser = False
                        us_id.save()
                    else:
                        us_id.is_active = True
                        us_id.is_staff = False
                        us_id.is_superuser = False
                        us_id.save()

                    grp_id=AuthGroup.objects.get(id=status)
                    us = AuthUserGroups(user=us_id, group= grp_id)
                    us.save();
                    messages.info(request,'User Added')
                    return redirect('phsys:adduser')
            else:
                messages.info(request,'Password not matching')
                return redirect('phsys:adduser')
            return redirect('phsys:adduser')
        else:
            return render(request,'adduser.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def addpurchase(request):
    d2 = Users.objects.all()
    d1 = Parties.objects.all()
    d = Medicine.objects.all()
    if request.method == 'POST':
        pno_id = request.POST['pno_id']
        make_id = request.POST['make_id']
        user_id = request.POST['user_id']
        p_date = request.POST['p_date']
        purch_id = request.POST['purch_id']
        med_id = request.POST['med_id']
        batchno = request.POST['batchno']
        ex_date = request.POST['ex_date']
        med_pri = request.POST['med_pri']
        qty = request.POST['qty']
        dis_pri = request.POST['dis_pri']
        net_rate = request.POST['net_rate']

        if PurchaseMaster.objects.filter(pno=pno_id).exists():
                messages.info(request,'A purchase with same ID already exists')
                return redirect('phsys:addpurchase')

        #partyid=form.cleaned_data['make_id']

        purm = PurchaseMaster(pno=pno_id,purchasedate=p_date,partyidfk= make_id,useridfk=user_id)
        purm.save();
        purd = PurchaseDetail(purch_id=purch_id,qty=qty,med_sprice=med_pri,dis_pri=dis_pri,net_rate=net_rate,batch_no=batchno,exp_date=ex_date,pnofk=pno_id,midfk=med_id)
        purd.save();

        messages.info(request,'Purchase Added')
        return redirect('phsys:addpurchase')

    else:
        return render(request,'addpurchase.html',  {'data1':d1, 'data':d, 'data2':d2})
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def addsale(request):
    d = Medicine.objects.all()
    d1 = Customer.objects.all()
    if request.method == 'POST':
        sale_id = request.POST['sale_id']
        cus_id = request.POST['cus_id']
        s_date = request.POST['s_date']
        v_no = request.POST['v_no']
        med_id = request.POST['med_id']
        qty = request.POST['qty']
        med_pri = request.POST['med_pri']
        dis_rate = request.POST['dis_rate']
        net_rate = request.POST['net_rate']

        if SalesMaster.objects.filter(sbillno=sale_id).exists():
                messages.info(request,'A sale with same ID already exists')
                return redirect('phsys:addsale')

        #partyid=form.cleaned_data['make_id']

        salem = SalesMaster(sbillno=sale_id, s_date=s_date,cidfk=cus_id)
        salem.save();
        saled = SalesDetails(sale_id=v_no, qty=qty, m_sprice=med_pri,dis_per=dis_rate, net_rate=net_rate, s_billnofk=sale_id, m_idfk=med_id)
        saled.save();

        messages.info(request,'Sale Added')
        return redirect('phsys:addsale')

    else:
        return render(request,'addsale.html', {'data':d, 'data1':d1})
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def addmanu(request):
    if request.method == 'POST':
        party_id = request.POST['party_id']
        par_name = request.POST['par_name']
        par_address = request.POST['par_address']
        contact = request.POST['contact']

        if Parties.objects.filter(party_id=party_id).exists():
                messages.info(request,'Manufacturer already exists')
                return redirect('Manufacturer')

        manu = Parties(party_id=party_id,par_name=par_name,par_address=par_address,contact=contact)
        manu.save();
        messages.info(request,'Manufacturer Added')
        return redirect('addmanu')

    else:
        return render(request,'addmanu.html')

#Update forms
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def update_med(request,pk):
    med = Medicine.objects.get(med_id=pk)
    if request.method == 'POST':
        medid = request.POST['med_id']
        g_name = request.POST['g_name']
        title = request.POST['title']
        manuf = request.POST['manuf']
        nature = request.POST['nature']
        dose = request.POST['dose']
        price = request.POST['price']

        med.med_id =medid
        med.g_name =g_name
        med.m_title =title
        med.m_make =manuf
        med.m_nature =nature
        med.m_doze =dose
        med.m_sprice =price

        med.save()

        return redirect("phsys:medicine")

    return render(request, 'updatemed.html', {'med': med})
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def update_cus(request,pk):
    cus = Customer.objects.get(cusid=pk)
    form = CustomerForm(request.POST,instance=cus)
    if request.method == 'POST':
        cus_id = request.POST['cus_id']
        cus_name = request.POST['cus_name']
        cus_address = request.POST['cus_address']
        cus_cont = request.POST['cus_contact']
        cus_email = request.POST['cus_email']

        cus.cusid =cus_id
        cus.cus_name =cus_name
        cus.cus_address =cus_address
        cus.cus_cont  =cus_cont
        cus.cus_email =cus_email

        cus.save()

        return redirect("phsys:customer")

    return render(request, 'updatecus.html', {'cus': cus})
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def update_manu(request,pk):
    manu = Parties.objects.get(party_id=pk)
    form = PartiesForm(request.POST,instance=manu)
    if request.method == 'POST':
        party_id = request.POST['party_id']
        par_name = request.POST['par_name']
        par_address = request.POST['par_address']
        contact = request.POST['contact']

        manu.party_id =party_id
        manu.par_name =par_name
        manu.par_address =par_address
        manu.contact  =contact

        manu.save()

        return redirect("phsys:manufacturer")

    return render(request, 'updatemanu.html', {'manu': manu})

#Delete forms
@allowed_users(allowed_roles=['Admin','Manager'])
def delete_med(request,med_id):
    d_med=Medicine.objects.get(pk=med_id)
    d_med.delete()

    return redirect('phsys:medicine')
@allowed_users(allowed_roles=['Admin','Manager'])
def delete_cus(request,cus_id):
    d_cus=Customer.objects.get(pk=cus_id)
    d_cus.delete()

    return redirect('phsys:customer')
@allowed_users(allowed_roles=['Admin','Manager'])
def delete_manu(request,party_id):
    d_manu=Parties.objects.get(pk=party_id)
    d_manu.delete()

    return redirect('phsys:manufacturer')
@allowed_users(allowed_roles=['Admin','Manager'])
def delete_purchase(request,purchase_id):
    d_pur=PurchaseMaster.objects.get(pk=purchase_id)
    d_pur.delete()

    return redirect('phsys:purchase')
@allowed_users(allowed_roles=['Admin','Manager'])
def delete_sale(request,sale_id):
    d_sale=SalesMaster.objects.get(pk=sale_id)
    d_sale.delete()

    return redirect('phsys:sale')
@allowed_users(allowed_roles=['Admin','Manager'])
def delete_user(request,usname):
    d_user=User.objects.get(username=usname)
    d_user.delete()

    return redirect('phsys:users')


#Lists
def medicine(request):

    medicine = Medicine.objects.all()

    return render(request,'medicine.html',{'medicine' : medicine})

@login_required(login_url='login')
def customer(request):

    customer = Customer.objects.all()
    return render(request,'customer.html',{'customer' : customer})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def users(request):

    user = GrpName.objects.all()

    if request.method == 'POST':
        user_ids = request.POST.getlist("user_id")
        user_ids = list(map(int, user_ids))
        status_id = (request.POST['status'])
        usid = User.objects.get(id__in=user_ids)
        us_id=AuthUser.objects.get(id=usid.id)

        if status_id =='null' :
           d_user=AuthUserGroups.objects.get(user=us_id)
           d_user.delete()
           return redirect('phsys:users')

        else:
            grp_id=AuthGroup.objects.get(id=status_id)
            if status_id == '1':
                us_id.is_active = True
                us_id.is_staff = True
                us_id.is_superuser = True
                us_id.save()
            elif status_id == '2':
                us_id.is_active = True
                us_id.is_staff = True
                us_id.is_superuser = False
                us_id.save()
            else:
                us_id.is_active = True
                us_id.is_staff = False
                us_id.is_superuser = False
                us_id.save()

            if AuthUserGroups.objects.filter(user=us_id).exists():
                aug=AuthUserGroups.objects.get(user=us_id)
                aug.group=grp_id
                aug.save()
                return redirect('phsys:users')
            else:
                us = AuthUserGroups(user=us_id, group= grp_id)
                us.save();
                return redirect('phsys:users')


    return render(request,'users.html',{'user' : user})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Manager'])
def purchase(request):
    pur = PurchaseMaster.objects.all()

    context = { 'data': pur}
    return render(request, 'purchase.html', context)

@login_required(login_url='login')
def sale(request):
    sal = SalesMaster.objects.all()
    cusid = Customer.objects.all()

    context = { 'data': sal, 'data2':cusid}
    return render(request, 'sale.html', context)

@login_required(login_url='login')
def search_med(request):

    medi = Medicine.objects.all()
    myFilter = MedicineFilter(request.GET, queryset=medi)


    return render(request,'searchmed.html',{'myFilter':myFilter})

@login_required(login_url='login')
def search_cus(request):

    cus = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=cus)


    return render(request,'searchcus.html',{'myFilter':myFilter})

def purchasedetail_trial(request, id=None):
    #purch = PurchaseDetail.objects.get(pnofk=id)
    showdetail = PurchaseDetail.objects.get(pnofk=id)
    purch = PurchaseMaster.objects.get(pno=id)
    #form = PurchaseDetailForm(instance=showdetail)
    #purch = get_object_or_404(PurchaseMaster, pno=id)
    #showdetail = purch.purchasedetail_set.all()
    context = {
        "company": {
            "name": "Purchase Detail",
            "address" :"University of Engineering and Technology, Lahore",
            "phone": "(+92) XXX XXXX",
            "email": "contact@xyz.com",
        },

        "purch_pno": showdetail.pnofk,
        "purch_party" :purch.partyidfk,
        "showdetail_no": showdetail.purch_id,
        "purchasedate" : purch.purchasedate,
        "showdetail" : showdetail,
        "showdetail_total" : showdetail.net_rate,
        "showdetail_midfk":showdetail.midfk,
        "showdetail_batch_no":showdetail.batch_no,
        "showdetail_exp_date":showdetail.exp_date,
        "showdetail_med_sprice":showdetail.med_sprice,
        "showdetail_dis_pri":showdetail.dis_pri,
        "showdetail_qty":showdetail.qty,
    }
    return render(request, 'purchase-template.html', context)

def saledetail_trial(request, id):
            global s
            #purch = PurchaseDetail.objects.get(pnofk=id)
            showdetail = SalesDetails.objects.get(s_billnofk=id)
            sale = SalesMaster.objects.get(sbillno=id)
            #form = PurchaseDetailForm(instance=showdetail)
            #purch = get_object_or_404(PurchaseMaster, pno=id)
            #showdetail = purch.purchasedetail_set.all()
            s=sale.sbillno
            context = {
                "company": {
                    "name": "Sales Detail",
                    "address" :"University of Engineering and Technology, Lahore",
                    "phone": "(+92) XXX XXXX",
                    "email": "contact@xyz.com",
                },

                "purch_pno": showdetail.s_billnofk,
                "purch_party" :sale.cidfk,
                "showdetail_no": showdetail.sale_id,
                "purchasedate" : sale.s_date,
                "showdetail" : showdetail,
                "showdetail_total" : showdetail.net_rate,
                "showdetail_m_idfk":showdetail.m_idfk,
                "showdetail_m_sprice":showdetail.m_sprice,
                "showdetail_dis_per":showdetail.dis_per,
                "showdetail_qty":showdetail.qty,
            }
            return render(request, 'sale-template.html', context)

@login_required(login_url='login')
def generate_PDF_purchase(request, id):
    # Use False instead of output path to save pdf to a variable
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('phsys:purchase-detail', args=[id])), False,  configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="purchase.pdf"'

    return response

@login_required(login_url='login')
def generate_PDF_sale(request, id):
    # Use False instead of output path to save pdf to a variable
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('phsys:sale-detail', args=[id])), False,  configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sale.pdf"'

    return response


def generate_PDF_med(request):
    # Use False instead of output path to save pdf to a variable
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('phsys:medicine')), False,  configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="medicine_list.pdf"'

    return response

def generate_PDF_receipt(request,id):
    # Use False instead of output path to save pdf to a variable
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('phsys:receipt_pdf')), False,  configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    return response



@login_required(login_url='login')
def manufacturer(request):

    parties = Parties.objects.all()

    return render(request,'manufacturer.html',{'parties' : parties})

@login_required(login_url='login')
def payment(request):
    global d,p,trd
    par = Parties.objects.all()
    if request.method == 'POST':
        p_date = request.POST['p_date']
        p_type = request.POST['p_type']
        amount = request.POST['amount']
        make = request.POST['make']
        trd = request.POST['trdetail']
        pay = Payments(p_date=p_date, remarks=p_type, amount=amount, partyid_fk=make)
        pay.save();
        context = {'bar': pay.partyid_fk}
        d=pay.partyid_fk
        p=pay.p_id
        return redirect('phsys:receipt')


    return render(request,'payment.html',{'pay' : payment, 'data' : par})

def receipt(request):
    global d,p,trd
    pay = Payments.objects.get(p_id=p)
    par = Parties.objects.get(party_id=d)
    context = {
        'all':pay,
        'data':par.par_name,
        'address':par.par_address,
        'cont': par.contact,
        'p_id':pay.p_id,
        'ptype':pay.remarks,
        'amount':pay.amount,
        'trdetail':trd
    }
    return render(request, 'receiptpage.html', context)

def receipt_pdf(request):
    global d,p,trd
    pay = Payments.objects.get(p_id=p)
    par = Parties.objects.get(party_id=d)
    context = {
        'all':pay,
        'data':par.par_name,
        'address':par.par_address,
        'cont': par.contact,
        'p_id':pay.p_id,
        'ptype':pay.remarks,
        'amount':pay.amount,
        'trdetail':trd
    }
    return render(request, 'receipt.html',context)

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
