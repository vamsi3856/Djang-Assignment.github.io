from rest_framework import viewsets
from . import models
from . import serializers

class studentViewset(viewsets.ModelViewSet):
    queryset=models.student.objects.all()
    serializer_class=serializers.studentSerializer