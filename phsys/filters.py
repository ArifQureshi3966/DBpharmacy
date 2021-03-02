import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class MedicineFilter(django_filters.FilterSet):

	g_name = CharFilter(field_name='g_name', lookup_expr='icontains')
	m_title = CharFilter(field_name='m_title', lookup_expr='icontains')
	m_make = CharFilter(field_name='m_make', lookup_expr='icontains')
	m_nature = CharFilter(field_name='m_nature', lookup_expr='icontains')
	m_doze = CharFilter(field_name='m_doze', lookup_expr='icontains')



	class Meta:
		model = Medicine
		fields = '__all__'
	#	exclude = ['customer', 'date_created']
class CustomerFilter(django_filters.FilterSet):
	cus_name = CharFilter(field_name='cus_name', lookup_expr='icontains')
	cus_address = CharFilter(field_name='cus_address', lookup_expr='icontains')
	cus_contact = CharFilter(field_name='cus_contact', lookup_expr='icontains')
	cus_email = CharFilter(field_name='cus_email', lookup_expr='icontains')



	class Meta:
		model = Customer
		fields = '__all__'