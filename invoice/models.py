from django.db import models
import datetime
# Create your models here.
class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "this is a default message.")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.customer)
    
    def get_status(self):
        return self.status

    # def save(self, *args, **kwargs):
        # if not self.id:             
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)

class LineItem(models.Model):
    customer = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)
   
class InvoiceInvoice(models.Model):
    customer = models.CharField(max_length=100)
    date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    message = models.TextField()
    billing_address = models.TextField(blank=True, null=True)
    customer_email = models.CharField(max_length=254, blank=True, null=True)
    status = models.IntegerField()
    total_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_invoice'


class InvoiceLineitem(models.Model):
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    customer = models.ForeignKey(InvoiceInvoice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invoice_lineitem'