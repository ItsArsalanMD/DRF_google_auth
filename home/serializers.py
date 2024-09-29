# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers 
from home.models import Students

class StudentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'name', 'age', 'grade']