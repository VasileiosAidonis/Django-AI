from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .forms import ImageForm
from .models import Images
import json, os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
# MODEL
import tensorflow as tf
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
import skimage
from keras.models import load_model
import efficientnet.tfkeras as efn



# Create your views here.
global my_counter
my_counter = 0

def home(request):

    context = {}
    context['form'] = ImageForm()

    # Set default variables for the Home Page
    global my_counter
    if my_counter == 0:
        request.session['image'] = 'custom/default.png'  # json.dumps(str(the_image.image)).replace('"','')
        request.session['gender'] = 'Your gender'
        request.session['anatomic_site'] = 'Lesion\'s anatomic site'
        request.session['group_age'] = 'Group age'
        request.session['result_binary'] = ''
        request.session['result_multiclass'] = ''
        request.session['pred_list'] = []
        request.session['submitted'] = False
        my_counter += 1

    if request.method == 'POST':
        new_image = ImageForm(request.POST, request.FILES)

        if new_image.is_valid():
            the_image = Images(image = new_image.cleaned_data.get('image'),
                               gender = new_image.cleaned_data.get('gender'),
                               anatomic_site = new_image.cleaned_data.get('anatomic_site'),
                               group_age = new_image.cleaned_data.get('group_age'))

            valid_extension = ['jpg', 'jpeg', 'png']
            str_image = str(the_image.image)
            img_extension = os.path.splitext(str_image)[1][1:]
            if img_extension not in valid_extension:
                messages.warning(request, 'Invalid image format')
                return HttpResponseRedirect(reverse('home'))

            the_image.save()
            print(the_image.image)
            print(the_image.pred_list)
            jsonDec = json.decoder.JSONDecoder()
            the_image.pred_list = jsonDec.decode(the_image.pred_list)
            context['my_image'] = the_image

            request.session['image'] = json.dumps(str(the_image.image)).replace('"','')
            request.session['gender'] = the_image.gender
            request.session['anatomic_site'] = the_image.anatomic_site
            request.session['group_age'] = the_image.group_age
            request.session['result_binary'] = the_image.result_binary
            request.session['result_multiclass'] = the_image.result_multiclass
            request.session['pred_list'] = the_image.pred_list
            request.session['submitted'] = True

            return HttpResponseRedirect(reverse('home'))

    return render(request,'home.html', context)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    # Return the Chart to fetch in Home Page
    def get(self, request, format=None):
        return Response()

def aboutus(request):
    return render(request, 'aboutUs.html')

def license(request):
    return render(request, 'license.html')




