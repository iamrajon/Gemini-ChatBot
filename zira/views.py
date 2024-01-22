from django.shortcuts import render, redirect
from google import generativeai as genai
from GeminiChatBot import settings
from zira.forms import TextAndImageForm
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from zira.models import GeminiImage

# setting configuration for gemini api
genai.configure(api_key=settings.GEMINI_API_KEY)

# getting text response from gemini
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# getting image/text response from gemini
def get_gemini_image_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text


# view function for making call to gemini api
def gemini_view(request):
    response_text = None

    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            response_text = get_gemini_response(question)

    return render(request, 'templates/gemini_text.html', {'response_text': response_text})

# view function for making call to gemini api with image and text
def gemini_image_view(request):
    response_text = None
    image = None

    if request.method == "POST":
        form = TextAndImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get("image_field")
            text = form.cleaned_data.get("text_field")
            print(f"image: {image} text: {text}")

            # Create a new instance of the GeminiImage model and save it
            gemini_image = GeminiImage(text_field=text, image_field=image)
            gemini_image.save()

            # Convert the uploaded image file to a PIL Image
            image = Image.open(image)

            if image and text:
                response_text = get_gemini_image_response(text, image)

                # Fetch the most recent image from the database
                try:
                    # Fetch the latest GeminiImage based on the primary key (id)
                    GeminiImage_pbj = GeminiImage.objects.latest('id')
                    print(f"obj: {GeminiImage_pbj}")
                
                except GeminiImage.DoesNotExist:
                    return None

                form = TextAndImageForm()
                context = {"form": form, "response_text": response_text, "response_image": GeminiImage_pbj }
                return render(request, "templates/gemini_image.html", context)               
        else:
           pass             
    else:
        form = TextAndImageForm()

    # context = {"form": form, "response_text": response_text, "image": image}
    context = {"form": form}
    return render(request, "templates/gemini_image.html", context)


