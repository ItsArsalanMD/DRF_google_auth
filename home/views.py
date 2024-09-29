from rest_framework import generics
from home.models import Students
from home.serializers import StudentSerilizer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class StudentListView(generics.ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerilizer
    authentication_classes = [JWTAuthentication]  # Add JWT authentication
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access


