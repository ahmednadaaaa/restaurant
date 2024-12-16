from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


# admin.site.register(CashPayment)
@admin.register(CashPayment)
class CashPaymentImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(Payment)
class PaymentImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(ContactUs)
class ContactUsImoprtExport(ImportExportModelAdmin):
    pass

#admin.site.register(Book)
@admin.register(BookTable)
class BookTableImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(OrderDetail)
class OrderDetailImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(Order)
class OrderImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(Employe)
class EmployeImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(Meal)
class MealImoprtExport(ImportExportModelAdmin):
    pass