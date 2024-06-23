from rest_framework import serializers
from .models import OCRData

class OCRDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRData
        fields = ['id', 'image', 'extracted_text', 'bold_words', 'image_base64', 'created_at']
