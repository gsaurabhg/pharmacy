from django.contrib import admin

from .models import Post, PatientDetail, Bill, returnBill

admin.site.register(Post)
admin.site.register(PatientDetail)
admin.site.register(Bill)
admin.site.register(returnBill)