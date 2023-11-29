from django.contrib import admin
from .models import Student, AdminStudent, Hostel

admin.site.register(Student)
admin.site.register(AdminStudent)
admin.site.register(Hostel)
