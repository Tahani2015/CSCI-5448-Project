from django.contrib import admin
from .models import Address, Bio, Insurance, Review, User, Doctor, RegisteredPatient, FavoriteDoctors

admin.site.register(Address)
admin.site.register(Bio)
admin.site.register(Insurance)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(RegisteredPatient)
admin.site.register(FavoriteDoctors)

