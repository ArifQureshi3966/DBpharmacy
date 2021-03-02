from django import forms
from .models import Medicine, Customer, PurchaseDetail,Parties

class MedicineForm(forms.ModelForm):
	class Meta:
		model = Medicine
		fields = "__all__"  

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"  

class PurchaseDetailForm(forms.ModelForm):
	class Meta:
		model = PurchaseDetail
		fields = "__all__"  
class PartiesForm(forms.ModelForm):
	class Meta:
		model = Parties
		fields = "__all__"  
