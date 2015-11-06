from django.shortcuts import render
from django.http import Http404

from website.models import Doctor

def index(request):
	# return HttpResponse('<p> In index view</p>')
	doctors=Doctor.objects.exclude(username='Sara_George@gmail.com')
   	return render(request, 'website/index.html', {
   		'doctors':doctors,
   		})
   