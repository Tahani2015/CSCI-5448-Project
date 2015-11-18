from __future__ import division
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django import forms
from gmapi import maps

from .forms import *
from .search import *
from .sort import *
from .login import *
from .models import *

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = Search(form.cleaned_data['speciality'],
                            form.cleaned_data['city'],
                            form.cleaned_data['state'],
                            form.cleaned_data['zip'],
                            form.cleaned_data['insurance'],)
            
            search.setSort(RatingSort())
            search.doSearch()
            if search.results== [] : print "No results! " # Alert msg
            else:
                #store search objects into our session information for use in search results
                request.session['search'] = search
                return redirect('website.views.search_results')
    else:
        form = SearchForm()
    return render(request, 'website/index.html', {'form': form})

def search_results(request):
    doctors= request.session['search']
    if request.method == 'POST':
        form = SetSortForm(request.POST)
        if form.is_valid():
            sort_type = form.cleaned_data['choice_field']
            doctors.reSort(sort_type)
    else:
        form = SetSortForm()
    return render(request, 'website/search_results.html', {'doctors':doctors, 'form':form})
   
def doctor_detail(request, pk):
    doctor=get_object_or_404(Doctor, username=pk)
    insurances=Insurance.objects.filter(doctor=pk)
    reviews=Review.objects.filter(doctor=pk)
    username=request.session.get('user', None)
    if username is not None:
        user=User.objects.get(username=username)
    else:
        user=None
    address = doctor.street + ' ' + doctor.city + ', ' + doctor.state + ' ' + doctor.zip
    gmap=get_map(address)
    return render(request, 'website/doctor_detail.html', {'doctor': doctor, 'insurances': insurances, 'reviews': reviews, 'user': user, 'form': MapForm(initial={'map': gmap})})

def get_map(address):
    geo = maps.Geocoder()
    res, status = geo.geocode({'address': address})
    gmap = maps.Map(opts = {
        'center': res[0].get('geometry').get('location'),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 15,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker = maps.Marker(opts= {
        'position': res[0].get('geometry').get('location'),
        'map': gmap
        })
    return gmap

def add_review(request, pk):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor_id = pk
            review.patient_id = request.session['user']  # The user currently logged in 
            review.save()
        # update doctor's rating    
            newRating=calculate_rating(pk)
            doctor=Doctor.objects.get(username=pk)
            doctor.rating=newRating
            doctor.save()
            return redirect('website.views.doctor_detail', pk=pk)
    else:
        form = ReviewForm();
    return render(request, 'website/review_add.html', {'form': form})

def calculate_rating(pk):
    reviews=Review.objects.filter(doctor=pk)
    ratingSum=0
    for review in reviews:
        ratingSum+=review.rating
    newRating=ratingSum/len(reviews)
    return newRating

def add_favorite(request, pk):
    favorite=FavoriteDoctors(patient_id=request.session['user'], doctor_id=pk)
    favorite.save()
    return redirect('website.views.doctor_detail', pk=pk)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.type = User.USER_CHOICES[1][1]
            new.save()
            return redirect('website.views.login')
    else:
        form = SignUpForm()
    return render(request, 'website/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.cleaned_data['username']
            userPage=LoginType(request.session['user']).redirectUser()
            return userPage
    else:
        form = LoginForm();
    return render(request, 'website/login.html', {'form': form})
   
def my_profile(request):
    user=User.objects.get(username=request.session['user'])
    if user.type == "Patient":
        patient=User.objects.get(username=request.session['user'])
        favourites=FavoriteDoctors.objects.filter(patient_id=request.session['user'])
        docList=[favourite.doctor_id for favourite in favourites]
        doctors=[]
        for doc in docList: 
            doctors.append(Doctor.objects.get(username=doc))
        return render(request, 'website/patient_profile.html', {'patient' : patient, 'doctors': doctors})
    else:
        return redirect('website.views.doctor_detail', pk=request.session['user'])

def remove_favdoc(request, pk):
    favourite_doc=FavoriteDoctors.objects.get(doctor_id=pk, patient_id=request.session['user'])
    favourite_doc.delete()
    return redirect('website.views.my_profile')

def edit_patprofile(request):
    patient = User.objects.get(username=request.session['user'])
    if request.method == 'POST':
        form = EditPatProForm(request.POST, instance=patient)
        if form.is_valid():
            new = form.save(commit=False)
            new.type = User.USER_CHOICES[1][1]
            new.save()
            return redirect('website.views.my_profile')
    else:
        form = EditPatProForm(instance=patient)
    return render(request, 'website/edit_patient_profile.html', {'form': form})

def edit_docprofile(request, pk):
    doctor = Doctor.objects.get(username=pk)
    if request.method == 'POST':
        form = EditDocProForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('website.views.doctor_detail', pk=pk)
    else:
        #make model data appear in form by default
        form = EditDocProForm(instance=doctor)
    return render(request, 'website/edit_doctor_profile.html', {'form': form})
