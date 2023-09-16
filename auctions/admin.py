from django.contrib import admin
from .models import User, Listing, bid, Comment, Catagory

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(bid)
admin.site.register(Comment)
admin.site.register(Catagory)
