
from django.conf.urls import include
from django.shortcuts import redirect
from .models import User

class LoginType():
	def __init__(self, username):
		self.user=User.objects.get(username=username)
		self.username=self.user.username
		self.type=self.user.type

	def redirectUser(self):
		if self.type == 'Patient':
			page= '/'
		elif self.type == 'Doctor':
			page= 'website.views.doctor_detail', pk=self.username   
		else:
			page= include(admin.site.urls)

		return page