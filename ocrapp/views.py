from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OCRData
from .serializers import OCRDataSerializer
from .utils import extract_text_from_image
import base64
from django.core.files.base import ContentFile
import os

class OCRView(APIView):
    def get(self,request):
        ocr_data=OCRData.objects.all()
        serializer=OCRDataSerializer(ocr_data,many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        print(image_file, 20)

        # Ensure /tmp directory exists
        temp_dir = '/tmp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Save the image temporarily to process
        temp_image_path = f"/tmp/{image_file.name}"
        with open(temp_image_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Extract text and bold words
        extracted_text, bold_words = extract_text_from_image(temp_image_path)

        # Convert image to base64
        with open(temp_image_path, "rb") as image_temp_file:
            image_base64 = base64.b64encode(image_temp_file.read()).decode('utf-8')

        # Create and save OCRData instance
        with open(temp_image_path, "rb") as image_temp_file:
            image_content = image_temp_file.read()
            content_file = ContentFile(image_content, name=image_file.name)
        
        ocr_data = OCRData(
            image=content_file,
            extracted_text=extracted_text,
            bold_words=", ".join(bold_words),
            image_base64=image_base64
        )
        ocr_data.save()

        serializer = OCRDataSerializer(ocr_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
