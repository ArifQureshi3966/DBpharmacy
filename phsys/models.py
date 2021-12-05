# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customer(models.Model):
    cusid = models.IntegerField(db_column='CusID', primary_key=True)  # Field name made lowercase.
    cus_name = models.CharField(db_column='Cus_Name', max_length=45)  # Field name made lowercase.
    cus_address = models.CharField(db_column='Cus_Address', max_length=45)  # Field name made lowercase.
    cus_contact = models.CharField(db_column='Cus_Contact', max_length=45)  # Field name made lowercase.
    cus_email = models.CharField(db_column='Cus_email', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GrpName(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField()
    email = models.CharField(max_length=254)
    group_id = models.IntegerField()
    first_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_name = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'grp_name'


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


class MedSale(models.Model):
    med_id = models.IntegerField(db_column='Med_ID')  # Field name made lowercase.
    g_name = models.CharField(db_column='G_name', max_length=45)  # Field name made lowercase.
    m_nature = models.CharField(db_column='M_Nature', max_length=45)  # Field name made lowercase.
    m_sprice = models.CharField(db_column='M_Sprice', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'med_sale'


class Medicine(models.Model):
    med_id = models.IntegerField(db_column='Med_ID', primary_key=True)  # Field name made lowercase.
    g_name = models.CharField(db_column='G_name', max_length=45)  # Field name made lowercase.
    m_title = models.CharField(db_column='M_Title', max_length=45)  # Field name made lowercase.
    m_make = models.CharField(db_column='M_Make', max_length=45)  # Field name made lowercase.
    m_nature = models.CharField(db_column='M_Nature', max_length=45)  # Field name made lowercase.
    m_doze = models.CharField(db_column='M_Doze', max_length=45)  # Field name made lowercase.
    m_sprice = models.CharField(db_column='M_Sprice', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medicine'


class Parties(models.Model):
    party_id = models.IntegerField(db_column='Party_ID', primary_key=True)  # Field name made lowercase.
    par_name = models.CharField(db_column='Par_Name', max_length=45)  # Field name made lowercase.
    par_address = models.CharField(db_column='Par_address', max_length=45)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parties'


class Payments(models.Model):
    p_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    p_date = models.DateField(db_column='P_Date')  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=45)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    partyid_fk = models.IntegerField(db_column='Partyid_fk')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payments'


class PurchaseDetail(models.Model):
    purch_id = models.IntegerField(db_column='Purch_ID', primary_key=True)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    med_sprice = models.FloatField(db_column='Med_sprice')  # Field name made lowercase.
    dis_pri = models.FloatField(db_column='Dis_Pri')  # Field name made lowercase.
    net_rate = models.FloatField(db_column='Net_Rate')  # Field name made lowercase.
    batch_no = models.CharField(db_column='Batch_no', max_length=45)  # Field name made lowercase.
    exp_date = models.DateField(db_column='Exp_Date')  # Field name made lowercase.
    pnofk = models.IntegerField(db_column='PnoFk')  # Field name made lowercase.
    midfk = models.IntegerField(db_column='MIDFK')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'purchase detail'


class PurchaseMaster(models.Model):
    pno = models.IntegerField(db_column='Pno', primary_key=True)  # Field name made lowercase.
    purchasedate = models.CharField(db_column='Purchasedate', max_length=45)  # Field name made lowercase.
    partyidfk = models.IntegerField(db_column='PartyIDFK')  # Field name made lowercase.
    useridfk = models.CharField(db_column='UserIDFK', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'purchase master'


class SalesDetails(models.Model):
    sale_id = models.IntegerField(db_column='Sale_ID', primary_key=True)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    m_sprice = models.FloatField(db_column='M_Sprice')  # Field name made lowercase.
    dis_per = models.FloatField(db_column='Dis_per')  # Field name made lowercase.
    net_rate = models.FloatField(db_column='Net_Rate')  # Field name made lowercase.
    s_billnofk = models.IntegerField(db_column='S_BillnoFK')  # Field name made lowercase.
    m_idfk = models.IntegerField(db_column='M_IDFK')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sales details'


class SalesMaster(models.Model):
    sbillno = models.IntegerField(db_column='SBillno', primary_key=True)  # Field name made lowercase.
    s_date = models.DateField(db_column='S_Date')  # Field name made lowercase.
    cidfk = models.IntegerField( db_column='CIDFK')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sales master'


class Users(models.Model):
    user_id = models.CharField(db_column='User_id', primary_key=True, max_length=45)  # Field name made lowercase.
    uname = models.CharField(db_column='UName', max_length=45)  # Field name made lowercase.
    userrole = models.CharField(db_column='UserRole', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
