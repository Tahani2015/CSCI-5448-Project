from django.contrib import admin


from .models import Insurance
from .models import Review
from .models import User
from .models import Doctor
from .models import FavoriteDoctors

admin.site.register(Insurance)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(FavoriteDoctors)