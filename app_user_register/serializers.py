
from rest_framework import serializers # type: ignore
from .models import FormEntry

class FormEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEntry
        fields = '__all__' 
