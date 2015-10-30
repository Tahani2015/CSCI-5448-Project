from django.db import models
from django.utils import timezone

class Address(models.Model):
	state = models.CharField(max_length=20)
	city = models.CharField(max_length=30)
 	zip = models.CharField(max_length=30)
	doctor = models.ForeignKey('Doctor')

class Bio(models.Model):
	education = models.TextField()
	awards = models.TextField()
	experience = models.TextField()
	doctor = models.ForeignKey('Doctor')

class Insurance(models.Model):
	INSURANCE_CHOICES = (
		('Aetna', 'Aetna'),
		('Cigna', 'Cigna'),
		('Medicaid', 'Medicaid'),
		('Medicare', 'Medicare'),
		('Tricare', 'Tricare'),
		('Blue', 'Blue'),
		('United', 'United'),
	)
	name = models.CharField(max_length=50, choices=INSURANCE_CHOICES)
	doctor = models.ForeignKey('Doctor')

class Review(models.Model):
	rating = models.IntegerField()
	comment= models. TextField()
	doctor = models.ForeignKey('Doctor')
	patient = models.ForeignKey('RegisteredPatient')
	date = models.DateTimeField(default=timezone.now)

class User(models.Model):
	USER_CHOICES = (
		('Admin', 'Admin'),
		('Patient', 'Patient'),
		('Doctor', 'Doctor'),
	)
	username = models.EmailField()
	password = models.CharField(max_length=256)
	type= models.CharField(max_length=10, choices=USER_CHOICES)

class Doctor(models.Model):
	SPECIALITY_CHOICES = (
		('Primary Care', 'Primary Care'),
		('Dentist', 'Dentist'),
		('Dermatologist', 'Dermatologist'),
		('ENT', 'ENT'),
		('Eye Doctor', 'Eye Doctor'),
		('Psychiatrist', 'Psychiatrist'),
		('Orthopedist', 'Orthopedist'),
	)
	name = models.CharField(max_length=30)
	phoneNumber = models.CharField(max_length =15)
	officeHours = models.CharField(max_length=100)
	speciality = models.CharField(max_length=30, choices=SPECIALITY_CHOICES)
	rating = models.FloatField()
	availability = models.DateField()

class RegisteredPatient(models.Model):
	name = models.CharField(max_length=30)
	username = models.ForeignKey('User')

class FavoriteDoctors(models.Model):
	patient = models.ForeignKey('RegisteredPatient')
	doctor = models.ForeignKey('Doctor')
