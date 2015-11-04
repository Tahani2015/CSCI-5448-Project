from django.contrib import admin
from .models import Insurance, Review, User, Doctor, FavoriteDoctors

admin.site.register(Insurance)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(FavoriteDoctors)

