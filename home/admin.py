from django.contrib import admin
from home.models import Students

# Register your models here.
@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'grade')
    search_fields = ('name', 'age', 'grade')
    list_filter = ('name', 'age')
    ordering = ('name', 'grade')
    
    fields = ('name', 'age', 'grade')  # Customize form fields
