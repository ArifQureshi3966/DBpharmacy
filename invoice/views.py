from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm
from phsys.decorators import allowed_users
import pdfkit
from weasyprint import HTML, CSS
from django.template.loader import get_template
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')
@allowed_users(allowed_roles=['Admin','Manager'])
def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address = form.data["billing_address"],
                    date=form.data["date"],
                    due_date=form.data["due_date"],
                    message=form.data["message"],
                    )
            # invoice.save()

        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('invoice:invoice-list')
    context = {
        "title" : "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "DB Project",
            "address" :"University of Engineering and Technology, Lahore",
            "phone": "(+92) XXX XXXX",
            "email": "contact@xyz.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,
    }
    return render(request, 'invoice/pdf_template.html', context)

def generate_PDF(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "DB Project",
            "address" :"University of Engineering and Technology, Lahore",
            "phone": "(+92) XXX XXXX",
            "email": "contact@xyz.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,
    }
    # Use False instead of output path to save pdf to a variable
    html_template = get_template('/home/Mahnoorkh/dpharmacy/invoice/templates/invoice/pdf_template.html').render(context)
    pdf_file = HTML(string=html_template).write_pdf(stylesheets=[CSS(os.path.join(BASE_DIR, 'static/css/invoice-template-1.css')),
                                                                 CSS(os.path.join(BASE_DIR, 'static/img/uetlogo.png')),
                                                                 CSS(string='@page { size: A3; margin: 1cm }')])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    return response

    return response

@allowed_users(allowed_roles=['Admin','Manager'])
def delete_invoice(request,id):
    d_inv=Invoice.objects.get(pk=id)
    d_inv.delete()
    return redirect('invoice:invoice-list')

def change_status(request):
    return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('invoice:invoice-list')